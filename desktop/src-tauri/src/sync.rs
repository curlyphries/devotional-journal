use anyhow::{anyhow, Result};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::collections::HashMap;

use crate::db::Database;

#[derive(Clone)]
pub struct SyncEngine {
    db: Database,
    http_client: reqwest::Client,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct VectorClock {
    clocks: HashMap<String, u64>,
}

impl Default for VectorClock {
    fn default() -> Self {
        Self {
            clocks: HashMap::new(),
        }
    }
}

impl SyncEngine {
    pub async fn new(db: Database) -> Result<Self> {
        let http_client = reqwest::Client::builder()
            .timeout(std::time::Duration::from_secs(30))
            .build()?;
        
        Ok(Self { db, http_client })
    }
    
    pub async fn initiate_auth(&self, email: String, api_url: String) -> Result<String> {
        // Save API URL to settings
        self.db.save_setting("api_url", &api_url).await?;
        
        let response = self
            .http_client
            .post(format!("{}/api/v1/auth/magic-link/request/", api_url))
            .json(&json!({ "email": email }))
            .send()
            .await?;
        
        if response.status().is_success() {
            Ok("Magic link sent".to_string())
        } else {
            Err(anyhow!("Failed to request magic link: {}", response.status()))
        }
    }
    
    pub async fn verify_magic_link(&self, token: String) -> Result<Value> {
        let api_url = self.db.get_setting("api_url").await?.unwrap_or_default();
        
        let response = self
            .http_client
            .post(format!("{}/api/v1/auth/magic-link/verify/", api_url))
            .json(&json!({ "token": token }))
            .send()
            .await?;
        
        if !response.status().is_success() {
            return Err(anyhow!("Invalid or expired magic link"));
        }
        
        let auth_data: Value = response.json().await?;
        
        // Save auth token
        if let Some(access_token) = auth_data.get("access").and_then(|v| v.as_str()) {
            self.db.save_setting("auth_token", access_token).await?;
        }
        
        // Register this device
        self.register_device(&api_url).await?;
        
        Ok(auth_data)
    }
    
    async fn register_device(&self, api_url: &str) -> Result<()> {
        let auth_token = self.db.get_setting("auth_token").await?.ok_or_else(|| anyhow!("Not authenticated"))?;
        
        // Generate device keypair (simplified - in production use proper ECDH)
        let device_name = format!("Desktop - {}", whoami::devicename());
        let public_key = "placeholder_public_key"; // Would be generated
        
        let response = self
            .http_client
            .post(format!("{}/api/v1/devices/register", api_url))
            .bearer_auth(&auth_token)
            .json(&json!({
                "name": device_name,
                "public_key": public_key,
            }))
            .send()
            .await?;
        
        if response.status().is_success() {
            let device_data: Value = response.json().await?;
            if let Some(device_id) = device_data.get("device_id").and_then(|v| v.as_str()) {
                self.db.save_setting("device_id", device_id).await?;
            }
            
            // Store encrypted root key if provided
            if let Some(encrypted_key) = device_data.get("encrypted_root_key").and_then(|v| v.as_str()) {
                // Decrypt and store in keychain
                // For now, we'll use the local keychain approach from crypto.rs
            }
        }
        
        Ok(())
    }
    
    pub async fn perform_sync(&self) -> Result<Value> {
        let api_url = match self.db.get_setting("api_url").await? {
            Some(url) => url,
            None => return Err(anyhow!("No API URL configured")),
        };
        
        let auth_token = match self.db.get_setting("auth_token").await? {
            Some(token) => token,
            None => return Err(anyhow!("Not authenticated")),
        };
        
        // Get local sync state
        let sync_state = self.db.get_sync_state().await?;
        let last_token = sync_state.get("last_sync_token").and_then(|v| v.as_str()).unwrap_or("");
        let vector_clock = sync_state.get("vector_clock").cloned().unwrap_or_else(|| json!({}));
        
        // Get pending outbox items
        let outbox = self.db.get_outbox_items(100).await?;
        
        // Build sync request
        let sync_request = json!({
            "since": {
                "token": last_token,
                "vector_clock": vector_clock,
            },
            "client_changes": outbox,
        });
        
        let response = self
            .http_client
            .post(format!("{}/api/v1/sync/journal/delta", api_url))
            .bearer_auth(&auth_token)
            .json(&sync_request)
            .send()
            .await?;
        
        if !response.status().is_success() {
            return Err(anyhow!("Sync failed: {}", response.status()));
        }
        
        let sync_response: Value = response.json().await?;
        
        // Process server changes
        if let Some(server_changes) = sync_response.get("server_changes").and_then(|v| v.as_array()) {
            for change in server_changes {
                self.apply_server_change(change).await?;
            }
        }
        
        // Update sync state
        let new_token = sync_response
            .get("sync_token")
            .and_then(|v| v.as_str())
            .unwrap_or(last_token);
        let new_vector_clock = sync_response
            .get("new_vector_clock")
            .map(|v| v.to_string())
            .unwrap_or_else(|| vector_clock.to_string());
        
        self.db.update_sync_state(new_token, &new_vector_clock).await?;
        
        // Clear processed outbox items
        for item in outbox {
            if let Some(id) = item.get("id").and_then(|v| v.as_i64()) {
                self.db.clear_outbox_item(id).await?;
            }
        }
        
        Ok(json!({
            "success": true,
            "server_changes_count": sync_response
                .get("server_changes")
                .and_then(|v| v.as_array())
                .map(|a| a.len())
                .unwrap_or(0),
            "pending_cleared": outbox.len(),
        }))
    }
    
    async fn apply_server_change(&self, change: &Value) -> Result<()> {
        let entry_id = change
            .get("entry_id")
            .and_then(|v| v.as_str())
            .ok_or_else(|| anyhow!("Missing entry_id in server change"))?;
        
        let automerge_changes = change
            .get("automerge_changes")
            .and_then(|v| v.as_str())
            .ok_or_else(|| anyhow!("Missing automerge_changes"))?;
        
        let changes_bytes = base64::decode(automerge_changes)?;
        
        // Load existing doc or create new
        let existing = sqlx::query("SELECT automerge_data FROM journal_entries WHERE id = ?")
            .bind(entry_id)
            .fetch_optional(&self.db.pool)
            .await?;
        
        let mut doc = if let Some(row) = existing {
            let encrypted: Vec<u8> = row.get("automerge_data");
            let decrypted = crate::crypto::decrypt_with_root(&encrypted)?;
            automerge::Automerge::load(&decrypted)
                .map_err(|e| anyhow!("Failed to load doc: {}", e))?
        } else {
            automerge::Automerge::new()
        };
        
        // Apply changes
        doc.apply_changes(automerge::Change::from_bytes(&changes_bytes)?)
            .map_err(|e| anyhow!("Failed to apply changes: {}", e))?;
        
        // Save back
        let new_bytes = doc.save();
        let encrypted = crate::crypto::encrypt_with_root(&new_bytes)?;
        let now = chrono::Utc::now().to_rfc3339();
        
        sqlx::query(
            r#"
            INSERT INTO journal_entries (id, doc_id, automerge_data, created_at, updated_at, sync_status, server_id) 
            VALUES (?, ?, ?, ?, ?, 'synced', ?)
            ON CONFLICT(id) DO UPDATE SET
                automerge_data = excluded.automerge_data,
                updated_at = excluded.updated_at,
                sync_status = 'synced'
            "#
        )
        .bind(entry_id)
        .bind(entry_id) // doc_id same as id for simplicity
        .bind(&encrypted)
        .bind(&now)
        .bind(&now)
        .bind(entry_id)
        .execute(&self.db.pool)
        .await?;
        
        Ok(())
    }
    
    pub async fn get_status(&self) -> Value {
        match self.db.get_sync_state().await {
            Ok(state) => json!({
                "configured": state.get("api_url").is_some(),
                "authenticated": state.get("auth_token").is_some(),
                "last_sync": state.get("last_sync_token"),
                "device_id": state.get("device_id"),
            }),
            Err(e) => json!({
                "error": e.to_string(),
            }),
        }
    }
}

// Extension trait for Database to support settings
impl Database {
    pub async fn save_setting(&self, key: &str, value: &str) -> Result<()> {
        let now = chrono::Utc::now().to_rfc3339();
        sqlx::query(
            "INSERT INTO settings (key, value, modified_at) VALUES (?, ?, ?)
             ON CONFLICT(key) DO UPDATE SET value = excluded.value, modified_at = excluded.modified_at"
        )
        .bind(key)
        .bind(value)
        .bind(&now)
        .execute(&self.pool)
        .await?;
        
        Ok(())
    }
    
    pub async fn get_setting(&self, key: &str) -> Result<Option<String>> {
        let row = sqlx::query("SELECT value FROM settings WHERE key = ?")
            .bind(key)
            .fetch_optional(&self.pool)
            .await?;
        
        Ok(row.map(|r| r.get::<String, _>("value")))
    }
}

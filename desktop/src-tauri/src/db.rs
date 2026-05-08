use anyhow::{anyhow, Result};
use serde_json::{json, Value};
use sqlx::{migrate::MigrateDatabase, sqlite::SqlitePoolOptions, Pool, Sqlite};
use std::path::Path;

#[derive(Clone)]
pub struct Database {
    pool: Pool<Sqlite>,
}

impl Database {
    pub async fn new(db_path: &Path) -> Result<Self> {
        let db_url = format!("sqlite:{}", db_path.display());
        
        // Create database if it doesn't exist
        if !Sqlite::database_exists(&db_url).await.unwrap_or(false) {
            Sqlite::create_database(&db_url).await?;
        }
        
        let pool = SqlitePoolOptions::new()
            .max_connections(5)
            .connect(&db_url)
            .await?;
        
        let db = Self { pool };
        db.init_tables().await?;
        
        Ok(db)
    }
    
    async fn init_tables(&self) -> Result<()> {
        sqlx::query(
            r#"
            CREATE TABLE IF NOT EXISTS sync_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                last_sync_token TEXT,
                vector_clock TEXT NOT NULL DEFAULT '{}',
                device_id TEXT,
                api_url TEXT,
                auth_token TEXT
            );
            
            CREATE TABLE IF NOT EXISTS journal_entries (
                id TEXT PRIMARY KEY,
                doc_id TEXT UNIQUE NOT NULL,
                server_id TEXT,
                automerge_data BLOB NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                is_deleted INTEGER DEFAULT 0,
                sync_status TEXT DEFAULT 'pending'
            );
            
            CREATE TABLE IF NOT EXISTS sync_outbox (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_id TEXT NOT NULL,
                operation TEXT NOT NULL,
                automerge_changes BLOB NOT NULL,
                created_at TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                modified_at TEXT NOT NULL,
                sync_status TEXT DEFAULT 'synced'
            );
            
            CREATE TABLE IF NOT EXISTS highlights (
                id TEXT PRIMARY KEY,
                verse_ref TEXT NOT NULL,
                color TEXT NOT NULL DEFAULT 'yellow',
                note TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                sync_status TEXT DEFAULT 'synced'
            );
            
            -- Full text search for journal entries
            CREATE VIRTUAL TABLE IF NOT EXISTS journal_entries_fts USING fts5(
                entry_id UNINDEXED,
                content
            );
            
            -- Indexes
            CREATE INDEX IF NOT EXISTS idx_entries_updated ON journal_entries(updated_at);
            CREATE INDEX IF NOT EXISTS idx_entries_sync ON journal_entries(sync_status);
            CREATE INDEX IF NOT EXISTS idx_outbox_created ON sync_outbox(created_at);
            "#
        )
        .execute(&self.pool)
        .await?;
        
        // Insert default sync state if not exists
        sqlx::query(
            "INSERT OR IGNORE INTO sync_state (id, vector_clock) VALUES (1, '{}')"
        )
        .execute(&self.pool)
        .await?;
        
        Ok(())
    }
    
    pub async fn create_entry(
        &self,
        content: String,
        mood: Option<String>,
        tags: Vec<String>,
    ) -> Result<String> {
        let id = uuid::Uuid::new_v4().to_string();
        let doc_id = uuid::Uuid::new_v4().to_string();
        let now = chrono::Utc::now().to_rfc3339();
        
        // Create Automerge document
        let mut doc = automerge::Automerge::new();
        let mut tx = doc.transaction();
        
        let content_obj = tx.put_object(automerge::ObjId::Root, "content", automerge::ObjType::Text)?;
        tx.splice_text(&content_obj, 0, 0, &content)?;
        
        if let Some(m) = mood {
            tx.put(automerge::ObjId::Root, "mood", m)?;
        }
        
        let tags_obj = tx.put_object(automerge::ObjId::Root, "tags", automerge::ObjType::List)?;
        for (i, tag) in tags.iter().enumerate() {
            tx.insert(&tags_obj, i, tag.clone())?;
        }
        
        tx.put(automerge::ObjId::Root, "created_at", now.clone())?;
        tx.put(automerge::ObjId::Root, "updated_at", now.clone())?;
        
        tx.commit();
        
        let automerge_bytes = doc.save();
        let encrypted = crate::crypto::encrypt_with_root(&automerge_bytes)?;
        
        sqlx::query(
            "INSERT INTO journal_entries (id, doc_id, automerge_data, created_at, updated_at, sync_status) VALUES (?, ?, ?, ?, ?, 'pending')"
        )
        .bind(&id)
        .bind(&doc_id)
        .bind(&encrypted)
        .bind(&now)
        .bind(&now)
        .execute(&self.pool)
        .await?;
        
        // Queue for sync
        sqlx::query(
            "INSERT INTO sync_outbox (entry_id, operation, automerge_changes, created_at) VALUES (?, 'create', ?, ?)"
        )
        .bind(&id)
        .bind(&automerge_bytes)
        .bind(&now)
        .execute(&self.pool)
        .await?;
        
        // Update FTS index
        sqlx::query("INSERT INTO journal_entries_fts (entry_id, content) VALUES (?, ?)")
            .bind(&id)
            .bind(&content)
            .execute(&self.pool)
            .await?;
        
        Ok(id)
    }
    
    pub async fn get_entries(&self, limit: i64, offset: i64) -> Result<Vec<Value>> {
        let rows = sqlx::query(
            "SELECT id, doc_id, automerge_data, created_at, updated_at, sync_status FROM journal_entries WHERE is_deleted = 0 ORDER BY updated_at DESC LIMIT ? OFFSET ?"
        )
        .bind(limit)
        .bind(offset)
        .fetch_all(&self.pool)
        .await?;
        
        let mut entries = Vec::new();
        for row in rows {
            let encrypted: Vec<u8> = row.get("automerge_data");
            let decrypted = crate::crypto::decrypt_with_root(&encrypted)?;
            let doc = automerge::Automerge::load(&decrypted)
                .map_err(|e| anyhow!("Failed to load Automerge doc: {}", e))?;
            
            // Extract text content
            let content = match doc.text(&automerge::ObjId::Root) {
                Some(obj_id) => doc.text(&obj_id).unwrap_or_default(),
                None => String::new(),
            };
            
            entries.push(json!({
                "id": row.get::<String, _>("id"),
                "doc_id": row.get::<String, _>("doc_id"),
                "content_preview": content.chars().take(200).collect::<String>(),
                "created_at": row.get::<String, _>("created_at"),
                "updated_at": row.get::<String, _>("updated_at"),
                "sync_status": row.get::<String, _>("sync_status"),
            }));
        }
        
        Ok(entries)
    }
    
    pub async fn search_entries(&self, query: &str) -> Result<Vec<Value>> {
        let rows = sqlx::query(
            "SELECT entry_id FROM journal_entries_fts WHERE content MATCH ? ORDER BY rank"
        )
        .bind(query)
        .fetch_all(&self.pool)
        .await?;
        
        let mut results = Vec::new();
        for row in rows {
            let id: String = row.get("entry_id");
            let entry = sqlx::query(
                "SELECT id, doc_id, automerge_data, created_at, updated_at FROM journal_entries WHERE id = ?"
            )
            .bind(&id)
            .fetch_one(&self.pool)
            .await?;
            
            let encrypted: Vec<u8> = entry.get("automerge_data");
            let decrypted = crate::crypto::decrypt_with_root(&encrypted)?;
            let doc = automerge::Automerge::load(&decrypted)
                .map_err(|e| anyhow!("Failed to load Automerge doc: {}", e))?;
            
            let content = match doc.text(&automerge::ObjId::Root) {
                Some(obj_id) => doc.text(&obj_id).unwrap_or_default(),
                None => String::new(),
            };
            
            results.push(json!({
                "id": id,
                "content_preview": content.chars().take(200).collect::<String>(),
                "created_at": entry.get::<String, _>("created_at"),
            }));
        }
        
        Ok(results)
    }
    
    pub async fn get_sync_state(&self) -> Result<Value> {
        let row = sqlx::query(
            "SELECT last_sync_token, vector_clock, device_id, api_url FROM sync_state WHERE id = 1"
        )
        .fetch_one(&self.pool)
        .await?;
        
        Ok(json!({
            "last_sync_token": row.get::<Option<String>, _>("last_sync_token"),
            "vector_clock": serde_json::from_str::<Value>(&row.get::<String, _>("vector_clock"))?,
            "device_id": row.get::<Option<String>, _>("device_id"),
            "api_url": row.get::<Option<String>, _>("api_url"),
        }))
    }
    
    pub async fn update_sync_state(&self, token: &str, vector_clock: &str) -> Result<()> {
        sqlx::query(
            "UPDATE sync_state SET last_sync_token = ?, vector_clock = ? WHERE id = 1"
        )
        .bind(token)
        .bind(vector_clock)
        .execute(&self.pool)
        .await?;
        
        Ok(())
    }
    
    pub async fn get_outbox_items(&self, limit: i64) -> Result<Vec<Value>> {
        let rows = sqlx::query(
            "SELECT id, entry_id, operation, automerge_changes, created_at FROM sync_outbox ORDER BY created_at LIMIT ?"
        )
        .bind(limit)
        .fetch_all(&self.pool)
        .await?;
        
        let mut items = Vec::new();
        for row in rows {
            items.push(json!({
                "id": row.get::<i64, _>("id"),
                "entry_id": row.get::<String, _>("entry_id"),
                "operation": row.get::<String, _>("operation"),
                "automerge_changes": base64::encode(row.get::<Vec<u8>, _>("automerge_changes")),
                "created_at": row.get::<String, _>("created_at"),
            }));
        }
        
        Ok(items)
    }
    
    pub async fn clear_outbox_item(&self, id: i64) -> Result<()> {
        sqlx::query("DELETE FROM sync_outbox WHERE id = ?")
            .bind(id)
            .execute(&self.pool)
            .await?;
        
        Ok(())
    }
}

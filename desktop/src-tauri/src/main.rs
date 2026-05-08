#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod crypto;
mod db;
mod sync;
mod tray;

use std::sync::Arc;
use tauri::{Manager, State};
use tokio::sync::RwLock;

/// Application state shared across commands
pub struct AppState {
    db: db::Database,
    sync: sync::SyncEngine,
}

#[tauri::command]
async fn authenticate(
    state: State<'_, Arc<RwLock<AppState>>>,
    email: String,
    api_url: String,
) -> Result<String, String> {
    let state = state.read().await;
    state
        .sync
        .initiate_auth(email, api_url)
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
async fn verify_magic_link(
    state: State<'_, Arc<RwLock<AppState>>>,
    token: String,
) -> Result<serde_json::Value, String> {
    let state = state.read().await;
    state
        .sync
        .verify_magic_link(token)
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
async fn create_journal_entry(
    state: State<'_, Arc<RwLock<AppState>>>,
    content: String,
    mood: Option<String>,
    tags: Vec<String>,
) -> Result<String, String> {
    let state = state.read().await;
    state
        .db
        .create_entry(content, mood, tags)
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
async fn get_journal_entries(
    state: State<'_, Arc<RwLock<AppState>>>,
    limit: Option<i64>,
    offset: Option<i64>,
) -> Result<Vec<serde_json::Value>, String> {
    let state = state.read().await;
    state
        .db
        .get_entries(limit.unwrap_or(50), offset.unwrap_or(0))
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
async fn search_entries(
    state: State<'_, Arc<RwLock<AppState>>>,
    query: String,
) -> Result<Vec<serde_json::Value>, String> {
    let state = state.read().await;
    state
        .db
        .search_entries(&query)
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
async fn trigger_sync(state: State<'_, Arc<RwLock<AppState>>>) -> Result<serde_json::Value, String> {
    let state = state.read().await;
    state
        .sync
        .perform_sync()
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
async fn get_sync_status(
    state: State<'_, Arc<RwLock<AppState>>>,
) -> Result<serde_json::Value, String> {
    let state = state.read().await;
    Ok(state.sync.get_status().await)
}

#[tauri::command]
fn lock_app() {
    // Emit event to frontend to show lock screen
}

#[tauri::command]
async fn unlock_app(password: Option<String>) -> Result<bool, String> {
    // Verify password or biometric
    // For MVP: just check if password matches stored hash
    Ok(true)
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_clipboard_manager::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_http::init())
        .plugin(tauri_plugin_notification::init())
        .plugin(tauri_plugin_os::init())
        .plugin(tauri_plugin_process::init())
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_sql::Builder::default().build())
        .plugin(tauri_plugin_store::init())
        .plugin(tauri_plugin_stronghold::init())
        .setup(|app| {
            // Initialize database
            let app_dir = app.path().app_data_dir()?;
            let db_path = app_dir.join("devotional.db");
            
            let rt = tokio::runtime::Runtime::new()?;
            let db = rt.block_on(db::Database::new(&db_path))?;
            let sync = rt.block_on(sync::SyncEngine::new(db.clone()))?;
            
            let state = Arc::new(RwLock::new(AppState { db, sync }));
            app.manage(state);

            // Setup tray
            tray::setup_tray(app)?;

            // Setup single instance handler
            #[cfg(desktop)]
            app.handle()
                .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
                    let _ = app.get_webview_window("main").expect("no main window")
                        .set_focus();
                }));

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            authenticate,
            verify_magic_link,
            create_journal_entry,
            get_journal_entries,
            search_entries,
            trigger_sync,
            get_sync_status,
            lock_app,
            unlock_app
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

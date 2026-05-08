use tauri::{
    menu::{Menu, MenuItem},
    tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent},
    Manager, Runtime,
};

pub fn setup_tray<R: Runtime>(app: &tauri::App<R>) -> tauri::Result<()> {
    let quit_i = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;
    let settings_i = MenuItem::with_id(app, "settings", "Settings", true, None::<&str>)?;
    let quick_capture_i = MenuItem::with_id(app, "quick_capture", "Quick Capture", true, None::<&str>)?;
    let todays_reading_i = MenuItem::with_id(app, "todays_reading", "Today's Reading", true, None::<&str>)?;
    let sync_now_i = MenuItem::with_id(app, "sync_now", "Sync Now", true, None::<&str>)?;
    
    let menu = Menu::with_items(
        app,
        &[
            &quick_capture_i,
            &todays_reading_i,
            &sync_now_i,
            &settings_i,
            &quit_i,
        ],
    )?;
    
    TrayIconBuilder::with_id("main-tray")
        .menu(&menu)
        .tooltip("Devotional Journal")
        .icon(app.default_window_icon().unwrap().clone())
        .on_tray_icon_event(|tray, event| {
            if let TrayIconEvent::Click {
                button: MouseButton::Left,
                button_state: MouseButtonState::Up,
                ..
            } = event
            {
                let app = tray.app_handle();
                if let Some(window) = app.get_webview_window("main") {
                    let _ = window.show();
                    let _ = window.set_focus();
                }
            }
        })
        .on_menu_event(|app, event| {
            match event.id.as_ref() {
                "quit" => {
                    app.exit(0);
                }
                "settings" => {
                    if let Some(window) = app.get_webview_window("main") {
                        let _ = window.show();
                        let _ = window.set_focus();
                        let _ = window.eval("window.location.href = '/settings'");
                    }
                }
                "quick_capture" => {
                    if let Some(window) = app.get_webview_window("main") {
                        let _ = window.show();
                        let _ = window.set_focus();
                        let _ = window.eval("window.location.href = '/journal?quick=true'");
                    }
                }
                "todays_reading" => {
                    if let Some(window) = app.get_webview_window("main") {
                        let _ = window.show();
                        let _ = window.set_focus();
                        let _ = window.eval("window.location.href = '/reading'");
                    }
                }
                "sync_now" => {
                    if let Some(window) = app.get_webview_window("main") {
                        let _ = window.emit("trigger-sync", ());
                    }
                }
                _ => {}
            }
        })
        .build(app)?;
    
    Ok(())
}

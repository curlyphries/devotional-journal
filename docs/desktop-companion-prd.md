# Devotional Journal Desktop Companion — PRD

**Version:** 1.0  
**Status:** Draft — Ready for Review  
**Target Platforms:** Windows 11, macOS 14+, Ubuntu 22.04+ (x64 + Apple Silicon)  
**Tech Stack:** Tauri (Rust) + React + SQLite (libSQL/Turso local replica)

---

## 1. Vision

A privacy-first, offline-capable desktop companion to the Devotional Journal web app. Users can journal, read scripture, and reflect without an internet connection — data syncs seamlessly when back online. End-to-end encryption ensures entries remain private even on a shared computer.

**Key Differentiators:**
- **True offline operation** — no loading spinners, no "retry" buttons
- **Hardware-backed encryption** — Touch ID / Windows Hello / Linux TPM where available
- **Instant sync** — background push/pull when online, conflict-free merging
- **Small footprint** — < 50MB download, < 100MB RAM

---

## 2. User Stories

| ID | As a... | I want to... | So that... | Priority |
|----|---------|--------------|------------|----------|
| DC-1 | commuter without Wi-Fi | write my morning devotional offline | I don't break my streak on the train | P0 |
| DC-2 | privacy-conscious user | lock the app with biometrics | my family can't read my journal on a shared laptop | P0 |
| DC-3 | pastor preparing sermons | search my 2 years of journal entries instantly | I can find that insight from last March | P1 |
| DC-4 | multi-device user | have my journal sync seamlessly between web and desktop | I can start on desktop, finish on web | P0 |
| DC-5 | battery-conscious user | have the app pause sync when on battery saver | my laptop lasts through a full day | P2 |
| DC-6 | new user | onboard without creating another password | I can use the same magic link from the web app | P1 |

---

## 3. Core Features

### 3.1 Offline-First Journal
- Full CRUD for journal entries offline
- Local SQLite database with libSQL (Turso local replica compatible)
- End-to-end encryption using same scheme as web (AES-GCM with per-user keys)
- Rich text support (markdown) with local autosave

### 3.2 Scripture Reader
- Downloaded KJV text (bundled ~5MB SQLite)
- Highlighting and notes (syncs to web)
- Cross-references and footnotes

### 3.3 Sync Engine
- **Conflict-free replicated data type (CRDT)** for journal entries
- Background sync when network available
- Queue for offline operations (create, update, delete)
- Resume interrupted syncs
- Last-write-wins for profile/settings, CRDT for journal content

### 3.4 Security
- **Key storage:** OS keychain (macOS Keychain, Windows DPAPI/ Credential Guard, Linux Secret Service / TPM)
- **App lock:** Biometric or PIN when enabled
- **Screen privacy:** Auto-blur on lock screen / app switch
- **Auto-lock:** After configurable idle time (default: 5 min)

### 3.5 System Integration
- **Tray icon:** Quick capture journal entry
- **Global shortcut:** Cmd/Ctrl+Shift+J to open quick capture
- **Notifications:** Daily reminder (respects system Do Not Disturb)
- **Badge:** Streak count on dock/taskbar

---

## 4. Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Tauri (Rust)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Auth      │  │   Sync      │  │   Encryption        │  │
│  │   Commands  │  │   Engine    │  │   (Rust-crypto)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Journal   │  │   Reader    │  │   Dashboard         │  │
│  │   Editor    │  │   Component │  │   (TanStack Query)  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Local Storage                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   libSQL    │  │   OS        │  │   Encrypted         │  │
│  │   (SQLite)  │  │   Keychain  │  │   Entry Cache       │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 4.1 Stack Justification

| Layer | Choice | Why |
|-------|--------|-----|
| Framework | Tauri | Rust core = memory safety, small bundle (<50MB vs Electron 150MB+), native OS integration |
| UI | React | Reuse web app components, familiar to team |
| DB | libSQL (SQLite fork) | Single file, zero config, CRDT extensions, Turso sync compatibility |
| Auth | Same JWT + magic link | Web parity, no new auth system |
| Crypto | Rust `ring` + OS keychain | Audited crypto, hardware-backed key storage |

### 4.2 Security Model

```
Encryption Root Key
       │
       ▼ (HKDF-SHA256)
┌──────────────┐     ┌──────────────┐
│  Data Key    │────▶│  AES-256-GCM │────▶ Journal entries
└──────────────┘     └──────────────┘
       │
       ▼
┌──────────────┐
│ OS Keychain  │  (encrypted at rest, biometric unlock)
└──────────────┘
```

---

## 5. Data Flow

### 5.1 First Launch (Online)
1. User clicks magic link or enters email
2. Tauri opens webview OAuth / magic link flow
3. Receives JWT tokens (access + refresh)
4. Generates local device keypair
5. Fetches user's encryption root key (encrypted with device public key)
6. Stores root key in OS keychain
7. Full sync: pulls journal, plans, highlights, settings

### 5.2 Normal Operation (Offline)
1. User opens app, biometric/PIN unlocks keychain
2. Journal entries decrypted on read, encrypted on write
3. Changes queued in local "outbox" table
4. Autosave to SQLite every 3 seconds

### 5.3 Sync Trigger (Online Detected)
1. Background Rust task detects connectivity
2. Uploads outbox items (with vector clock for CRDT)
3. Server returns remote changes since last sync token
4. Local CRDT merge (no conflicts for journal text)
5. Updates "last sync" timestamp
6. Clears outbox

### 5.4 Conflict Resolution
- Journal content: CRDT (automerge or custom LWW-element-set)
- Settings/profile: Last-write-wins with timestamp
- Deleted items: Tombstones with 30-day retention

---

## 6. UI/UX Specifications

### 6.1 Window & Layout
- **Size:** 900x650 min, 1200x800 optimal
- **Theme:** Match system (light/dark), same Tailwind config as web
- **Navigation:** Sidebar (collapsible) + main content area
- **Font:** Inter (web parity), system fallback

### 6.2 Key Screens

**Dashboard (Home)**
- Today's focus / devotional passage
- Streak badge with share button
- Quick capture button
- Recent entries list

**Journal Editor**
- Markdown editor with preview toggle
- Date picker (defaults to today)
- Mood selector (emoji + color)
- Associated plan/passage selector
- Autosave indicator

**Reader**
- Passage view (KJV default, translation switcher)
- Highlight tool (color palette)
- Note sidebar
- Reading plans progress

**Settings**
- Biometric toggle
- Auto-lock timeout
- Offline content download (KJV, plans)
- Sync status / manual sync button
- Sign out (wipes local data)

### 6.3 Tray/Dock Integration
- Left-click: Show/hide main window
- Right-click menu:
  - Quick Capture
  - Today's Reading
  - Sync Now
  - Settings
  - Quit

---

## 7. API Requirements

### New Backend Endpoints Needed

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/devices/register` | Register device, get device_id |
| POST | `/api/v1/devices/{id}/key` | Exchange encrypted root key |
| DELETE | `/api/v1/devices/{id}` | Revoke device, wipe server keys |
| GET | `/api/v1/sync/journal?since={token}` | Delta sync for journal entries |
| POST | `/api/v1/sync/journal` | Upload local changes |
| GET | `/api/v1/sync/highlights?since={token}` | Delta sync for highlights |
| POST | `/api/v1/sync/highlights` | Upload highlight changes |

### Sync Protocol
```json
{
  "client_vector_clock": {"device-a": 45, "device-b": 12},
  "changes": [
    {
      "id": "entry-uuid",
      "op": "update",
      "field": "content",
      "value": "encrypted-ciphertext",
      "timestamp": "2026-05-03T18:30:00Z",
      "device": "desktop-macbook"
    }
  ]
}
```

---

## 8. Platform-Specific Notes

### macOS
- Notarize app for Gatekeeper
- Touch ID via `LocalAuthentication` framework (Tauri plugin)
- Sparkle framework for auto-updates

### Windows
- Code sign with EV cert (SmartScreen)
- Windows Hello via `WebAuthenticationCoreManager`
- MSIX installer for Store distribution

### Linux
- AppImage + .deb + Flatpak
- Secret Service API (`org.freedesktop.secrets`)
- TPM2 support where available (tpm2-tss)

---

## 9. Privacy & Compliance

- **GDPR:** Right to be forgotten — wipe all local data + server device record
- **No telemetry:** All analytics opt-in only
- **Data minimization:** Only cache what's needed for offline (configurable)
- **Encryption:** Same scheme as web (already audited)

---

## 10. Release Criteria

### MVP (v1.0)
- [ ] Journal CRUD offline with sync
- [ ] KJV reader offline
- [ ] Biometric lock (macOS/Windows)
- [ ] Basic tray menu
- [ ] Auto-updater

### v1.1
- [ ] Linux biometric/TPM
- [ ] Fulltext search (SQLite FTS5)
- [ ] Import from web export ZIP
- [ ] Global shortcut quick capture

### v1.2
- [ ] Reading plans offline
- [ ] AI prompts cache (last 10)
- [ ] Group leader dashboard (view only)

---

## 11. Open Questions

1. **Turso vs plain SQLite?** Turso gives us sync primitives but adds vendor dependency. Plain SQLite + custom sync = more work, more control.
2. **CRDT library?** Automerge (JS) in Tauri's JS side, or implement simple LWW in Rust?
3. **Auto-updater?** Tauri has built-in updater, but need signing certs for all 3 platforms upfront.
4. **Offline AI?** Should we bundle tiny LLM (llama.cpp) for offline prompt generation? (Phase 2)

---

## 12. Estimation

| Phase | Scope | Estimate |
|-------|-------|----------|
| Foundation | Tauri setup, auth, encryption, SQLite | 2 weeks |
| Sync Engine | Delta sync, CRDT, conflict resolution | 2 weeks |
| UI Implementation | React components, theming, editor | 2 weeks |
| Platform Polish | Signing, notarization, installers | 1 week |
| QA & Beta | Cross-platform testing, edge cases | 1 week |
| **Total MVP** | | **8 weeks** |

---

*Document ready for review. Next step: architecture decision on sync strategy (Turso vs custom).*

# Devotional Journal Desktop

Offline-first desktop companion built with Tauri (Rust) + React.

## Prerequisites

- **Rust** (1.75+) — [rustup.rs](https://rustup.rs)
- **Node.js** (20+) — [nodejs.org](https://nodejs.org)
- **Tauri CLI** — `cargo install tauri-cli`

## Quick Start

```bash
cd desktop

# Install JS dependencies
npm install

# Run development server
npm run tauri:dev
```

## Build for Production

```bash
# Build all platforms
npm run tauri:build

# Or use cargo directly
cargo tauri build
```

## Project Structure

```
desktop/
├── src/                    # React frontend
│   ├── components/         # UI components
│   ├── pages/              # Route pages
│   ├── store/              # Zustand state management
│   ├── App.tsx             # Main app component
│   └── main.tsx            # Entry point
├── src-tauri/              # Rust backend
│   ├── src/
│   │   ├── main.rs         # App entry
│   │   ├── lib.rs          # Module exports
│   │   ├── crypto.rs       # Encryption (OS keychain + AES-GCM)
│   │   ├── db.rs           # SQLite + Automerge
│   │   ├── sync.rs         # Delta sync engine
│   │   └── tray.rs         # System tray
│   ├── Cargo.toml          # Rust deps
│   └── tauri.conf.json     # Tauri config
├── package.json            # Node deps
├── vite.config.ts          # Vite config
└── tailwind.config.js      # Tailwind
```

## Architecture Decisions

See `../docs/desktop-companion-adr.md` for full ADRs.

### Key Choices

| Decision | Choice |
|----------|--------|
| Sync Strategy | Custom delta sync (not Turso) |
| CRDT | Automerge WASM |
| Signing | Unsigned builds for MVP |
| Key Storage | OS keychain (Keychain/DPAPI/Secret Service) |
| Database | SQLite + sqlx |

## Security Model

```
User Password/Biometric
       ↓
OS Keychain (stores root key)
       ↓
HKDF-SHA256 (derive data key)
       ↓
AES-256-GCM (encrypt journal entries)
       ↓
SQLite (encrypted Automerge documents)
```

## Backend Requirements

The desktop app requires these new backend endpoints:

- `POST /api/v1/devices/register` — Register device
- `POST /api/v1/sync/journal/delta` — Delta sync

See `../docs/desktop-companion-adr.md` for API spec.

## Platform Notes

### macOS
- Right-click app → Open to bypass Gatekeeper
- Or: `xattr -d com.apple.quarantine /Applications/Devotional\ Journal.app`

### Windows
- Click "More info" → "Run anyway" on SmartScreen
- Future: Chocolatey/Scoop distribution

### Linux
- AppImage works without signing
- Flatpak for store distribution

## Roadmap

- [x] Foundation (Tauri, SQLite, encryption)
- [x] Basic UI (React, Tailwind, routing)
- [ ] Journal CRUD with Automerge
- [ ] Sync engine implementation
- [ ] Device registration flow
- [ ] KJV offline bundle
- [ ] Tray/quick capture
- [ ] Settings panel
- [ ] Cross-platform testing
- [ ] Installers (DMG, MSI, AppImage)

## License

AGPL-3.0 — same as main project.

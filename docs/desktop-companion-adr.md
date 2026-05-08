# Desktop Companion — Architecture Decision Records

## ADR-001: Custom Sync over Turso

**Status:** Accepted  
**Date:** 2026-05-03

### Context
Turso offers managed sync with CRDTs but introduces vendor dependency and costs. We already have a Django backend with PostgreSQL.

### Decision
Implement custom delta sync protocol:
- Client maintains `last_sync_token` (timestamp + vector clock)
- Server returns changes since token, client merges with Automerge
- Conflict-free: journal entries use Automerge text, settings use LWW

### Consequences
- **+** No vendor lock-in, works with existing infrastructure
- **+** Full control over sync behavior
- **-** More code to maintain (sync engine, CRDT merge logic)
- **-** Need to design schema for sync metadata

---

## ADR-002: Automerge (WASM) over Custom LWW

**Status:** Accepted  
**Date:** 2026-05-03

### Context
Need CRDT for journal text merging. Options: Automerge (mature) vs custom Last-Write-Wins (simpler).

### Decision
Use Automerge WASM in Tauri's JavaScript side:
- Journal content: Automerge.Text for rich merging
- Metadata (title, mood, tags): Automerge.Map
- Serialized to binary for SQLite storage

### Consequences
- **+** Battle-tested CRDT, handles concurrent edits gracefully
- **+** Future-proof for collaborative features
- **-** WASM bundle size (~500KB)
- **-** Slightly more complex integration with Tauri

---

## ADR-003: Unsigned Builds for MVP

**Status:** Accepted  
**Date:** 2026-05-03

### Context
No Apple Developer account, no Windows EV cert available for MVP.

### Decision
Ship unsigned builds with clear documentation:
- **macOS:** Users right-click → Open, or `xattr -d com.apple.quarantine`
- **Windows:** Users click "More info" → "Run anyway" on SmartScreen
- **Linux:** AppImage/Flatpak (no signing needed)

### Consequences
- **+** Can ship immediately without $300+ in certificates
- **+** Early adopters/devs comfortable with unsigned apps
- **-** Poor UX for non-technical users on macOS/Windows
- **-** Cannot distribute via Mac App Store or Microsoft Store
- **-** Security warnings may deter some users

### Mitigation
- Clear install instructions with screenshots
- Homebrew formula for macOS (unsigned but trusted channel)
- Chocolatey/Scoop for Windows
- Plan to sign in v1.1 if product gains traction

---

## ADR-004: SQLite (libSQL) with Automerge Documents

**Status:** Accepted  
**Date:** 2026-05-03

### Schema
```sql
-- Sync metadata
CREATE TABLE sync_state (
    id INTEGER PRIMARY KEY,
    last_sync_token TEXT,
    vector_clock BLOB -- JSON {device_id: counter}
);

-- Journal entries (Automerge documents)
CREATE TABLE journal_entries (
    id TEXT PRIMARY KEY,
    doc_id TEXT UNIQUE,        -- Automerge document ID
    automerge_data BLOB,       -- Binary Automerge document
    server_id TEXT,            -- UUID from web backend
    created_at TEXT,
    updated_at TEXT,
    is_deleted BOOLEAN DEFAULT 0,
    sync_status TEXT          -- 'synced', 'pending', 'conflict'
);

-- Outbox for pending changes
CREATE TABLE sync_outbox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id TEXT,
    operation TEXT,            -- 'create', 'update', 'delete'
    automerge_changes BLOB,    -- Automerge change bytes
    created_at TEXT
);

-- Settings (LWW, not CRDT)
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    modified_at TEXT,
    sync_status TEXT
);
```

---

## ADR-005: Tauri Sidecar Pattern for Crypto

**Status:** Accepted  
**Date:** 2026-05-03

### Context
Need to access OS keychain from Rust, but want JS-side encryption for simplicity.

### Decision
- **Rust side:** Keychain access, key derivation (HKDF), raw AES-GCM
- **JS side:** Automerge CRDT operations, business logic
- **Bridge:** Tauri commands for `encrypt(data, keyId)` / `decrypt(cipher, keyId)`

Key never leaves Rust memory except as opaque handle.

---

## Required Backend Changes

### New Models
```python
class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # "MacBook Pro", "Work PC"
    public_key = models.TextField()  # RSA/ECDH public key for key exchange
    last_seen = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class JournalSyncCheckpoint(models.Model):
    """Server-side sync token for each device"""
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    vector_clock = models.JSONField(default=dict)
    last_entry_timestamp = models.DateTimeField(null=True)
```

### New Endpoints

**POST /api/v1/devices/register**
```json
{
  "name": "MacBook Pro",
  "public_key": "base64-encoded-key"
}
```
Response: `{ "device_id": "uuid", "encrypted_root_key": "base64" }`

**POST /api/v1/sync/journal/delta**
```json
{
  "since": {"timestamp": "2026-05-01T00:00:00Z", "vector_clock": {"device-a": 45}},
  "client_changes": [
    {"entry_id": "uuid", "automerge_changes": "base64", "operation": "update"}
  ]
}
```
Response: `{ "server_changes": [...], "new_vector_clock": {...}, "sync_token": "..." }`

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Tauri project setup with React + TypeScript
- [ ] SQLite + libSQL integration
- [ ] OS keychain access (Rust)
- [ ] Automerge WASM integration
- [ ] Basic window/shell

### Phase 2: Core Features (Week 2)
- [ ] Journal entry CRUD (offline)
- [ ] Markdown editor (reuse web components where possible)
- [ ] Encryption/decrypt pipeline
- [ ] Local database schema

### Phase 3: Sync Engine (Week 3)
- [ ] Device registration flow
- [ ] Delta sync implementation
- [ ] Outbox queue
- [ ] Conflict resolution (Automerge merge)

### Phase 4: Integration (Week 4)
- [ ] Magic link auth bridge
- [ ] KJV offline bundle
- [ ] Settings sync
- [ ] Tray/quick capture

### Phase 5: Polish (Week 5)
- [ ] Cross-platform testing
- [ ] Installers (DMG, MSI, AppImage)
- [ ] Documentation
- [ ] Beta release

---

## Open Questions

1. **Should we use the existing React components from web?**
   - PRO: Consistent UI, less work
   - CON: Tauri webview may have slight differences, need to test

2. **Automerge version format compatibility?**
   - Automerge has changed binary format in past
   - Should we pin version or implement migration?

3. **Handling large journal histories?**
   - User with 1000+ entries: full sync on first connect?
   - Solution: Pagination in delta sync (100 entries at a time)

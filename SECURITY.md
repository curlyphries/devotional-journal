# Security Policy

Devotional Journal stores some of the most intimate writing a person can produce — prayers, struggles, and reflections. Security is therefore a first-class concern, not a checklist item.

This document describes the threat model, what protections exist, what protections do **not** exist, and how to report a vulnerability.

---

## Supported versions

Until the project reaches 1.0, only the **`master`** branch receives security patches. If you are running a fork or a pinned release, you are responsible for backporting fixes.

| Version  | Supported          |
|----------|--------------------|
| master   | ✅ Yes             |
| < 1.0    | ⚠️ Latest commit only |

---

## Threat model

### What we protect against

1. **Database compromise** — an attacker with read access to the Postgres database cannot read journal entry text. Per-user AES-encrypted content remains opaque without the user's derived key.
2. **Casual server access** — a sysadmin who logs into the application server cannot trivially read user journal entries by inspecting the database.
3. **JWT replay during a session** — refresh tokens are now invalidated on logout (when the JWT blacklist is configured) and access tokens are short-lived.
4. **Cross-site scripting (XSS)** — React escapes by default; we avoid `dangerouslySetInnerHTML` in user-provided content.
5. **Cross-site request forgery (CSRF)** — same-site cookies and DRF's CSRF middleware on session endpoints.
6. **Private plan disclosure** — a private user-created reading plan is visible only to its creator (verified at the queryset level).
7. **Magic-link brute force** — magic-link requests are rate-limited per IP and per email.
8. **Encryption-key exfiltration via app errors** — `ENCRYPTION_ROOT_KEY` is read from environment, never logged, never echoed.

### What we do NOT protect against

1. **Compromise of the application server's memory** — if an attacker can read the running Django process's memory, they can recover user keys for sessions that recently decrypted entries.
2. **Lost `ENCRYPTION_ROOT_KEY`** — there is no recovery. All journal entries become permanently unreadable. This is intentional; back up your key.
3. **Compromise of a user's email** — magic-link auth flows through email. If your email is compromised, your account can be taken over.
4. **Compromise of a user's Google account** — Google OAuth implies trust in Google's identity attestation.
5. **Side-channel attacks against your AI provider** — if you point the app at a third-party AI (OpenAI, Anthropic, OpenRouter), the prompt content is sent to that provider and subject to their data-handling policy. Use Ollama or a local provider if this is a concern.
6. **Operator misconfiguration** — running with `DEBUG=True` in production, exposing the admin without TLS, etc.

---

## Encryption details

- **Algorithm:** AES (Fernet, AES-128 in CBC mode with HMAC-SHA256 authentication)
- **Key derivation:** per-user key derived from `ENCRYPTION_ROOT_KEY` + a per-user salt using PBKDF2-HMAC-SHA256
- **What's encrypted:** journal entry body, journal entry mood notes
- **What's NOT encrypted:** scripture references, plan progress metadata, life-area scores, streak counts, timestamps. These are needed for queries and aggregations.
- **Key rotation:** not yet automated; planned for 1.0

Audit the implementation: [`backend/shared/encryption.py`](backend/shared/encryption.py)

---

## Operational guidance for self-hosters

If you run this app for yourself or others, follow these operational practices:

### Minimum viable

- [ ] Set `ENCRYPTION_ROOT_KEY` to a 64-character hex string from `secrets.token_hex(32)`
- [ ] Back up `ENCRYPTION_ROOT_KEY` somewhere outside the server (password manager, HSM, paper in a safe)
- [ ] Set `DEBUG=False` in production
- [ ] Set `ALLOWED_HOSTS` to your real domain only
- [ ] Use TLS (Let's Encrypt is fine) for all traffic
- [ ] Keep Django, Postgres, and Redis patched
- [ ] Restrict Postgres listening to the Docker bridge network or localhost
- [ ] Rotate JWT signing key (`SECRET_KEY`) if you suspect compromise

### Recommended

- [ ] Enable rate limiting at the reverse proxy (nginx `limit_req_zone`)
- [ ] Run Postgres with TLS between app ↔ database
- [ ] Run automated backups with encryption-at-rest (e.g., `pgbackrest` + KMS)
- [ ] Restrict the Django admin to a VPN or IP allowlist
- [ ] Enable structured logging and ship logs to a separate host
- [ ] Periodically run `docker scout` or `trivy` against the production images

---

## Reporting a vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Report security issues by opening a [security advisory](https://github.com/curlyphries/devotional-journal/security/advisories/new) on the GitHub repository.

When reporting, please include:

1. A clear description of the vulnerability
2. Steps to reproduce, ideally a proof-of-concept
3. Affected versions (commit SHA if possible)
4. Your assessment of severity and impact
5. Whether you would like to be credited in the changelog (and how)

### Response timeline

| Action                    | Target                                 |
|---------------------------|----------------------------------------|
| Initial acknowledgement   | Within 3 days                          |
| Triage + severity classification | Within 7 days                   |
| Fix in `master`           | Within 30 days for critical issues     |
| Public disclosure         | Coordinated with the reporter          |

This is a side-project run by a small maintainer team. Targets are best-effort.

---

## Disclosure history

No disclosed vulnerabilities yet. New entries will be added here when they happen.

---

## Acknowledgements

If you find and report a real vulnerability, you will be acknowledged in this file (with your permission) and in the corresponding [CHANGELOG.md](CHANGELOG.md) entry.

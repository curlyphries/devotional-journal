# Privacy

Devotional Journal is open-source software. This document describes how the **reference deployment and self-hosted instances** handle user data. If you use a fork or a third-party hosted instance, the operator of that instance is responsible for their own privacy policy.

> **TL;DR.** Your journal is encrypted at rest with a per-user key derived from a secret held by the server operator: a stolen database or backup alone cannot be read, but the operator of the server can decrypt it. It is not end-to-end encryption. We don't run analytics by default. You can export everything. You can delete everything. If you self-host with Ollama, your reflections never leave your network.

---

## What we collect

### Required to run the app

- **Email address** — for magic-link login or Google OAuth
- **Display name** — what you set in Settings
- **Language preference** — `en`, `es`, or `bilingual`
- **Timezone** — for streak calculation and reading reminders
- **Journal entries** — their text **encrypted** with a per-user key; their timestamps, mood tags, and scripture references in plaintext for queries
- **Highlights, reflections, focuses, plan progress, streaks** — stored unencrypted (needed for aggregations and reading plan logic)
- **AI provider settings** — provider name, model, optional API key (encrypted at rest), optional base URL

### Optional, only if you opt in

- **Bring-your-own-AI key** — only stored if you provide one in Settings. Encrypted at rest. Used only to forward your prompt to your chosen AI provider.

### Automatically collected (operational)

- **Server logs** — request ids, error codes, AI provider/model and timing. No request bodies, no journal text, no model output. Sign-in links are not logged unless the operator sets `MAGIC_LINK_LOG=true` (private instances without a mail server).
- **Error logs** — Django exception traces. Configured to **not** include request body or user-provided content.

### What we do NOT collect

- ❌ No third-party analytics by default — no Google Analytics, no Facebook pixel, no Segment, no Mixpanel
- ❌ No advertising trackers
- ❌ No fingerprinting
- ❌ No social-media share pixels
- ❌ No cross-site cookies

If a self-host operator chooses to add analytics (PostHog and Plausible are the recommended options), they should disclose that in their own privacy policy.

---

## Where your data lives

| Data                             | Storage                            | Encrypted?         |
|----------------------------------|------------------------------------|--------------------|
| Journal entry body               | PostgreSQL                         | ✅ Per-user AES    |
| Journal feedback: themes, reflection, reasons, audit candidates | PostgreSQL            | ✅ Per-user AES    |
| Growth reviews, thread summaries, daily reflection notes, focus text | PostgreSQL        | ✅ Per-user AES    |
| Scripture reference + verse text shown with feedback; AI provider/model used | PostgreSQL | ❌ Plaintext (public text / metadata) |
| Speak Your Mind input and results, journey goals, study-guide notes, AI insights on reflections | PostgreSQL | ❌ Plaintext |
| BYOAI API key                    | PostgreSQL                         | ✅ At rest         |
| Email, display name, settings    | PostgreSQL                         | ❌ Plaintext       |
| Reading-plan progress, streaks   | PostgreSQL                         | ❌ Plaintext       |
| Reflections, life-area scores    | PostgreSQL                         | ❌ Plaintext       |
| Bible highlights and notes       | PostgreSQL                         | ❌ Plaintext       |
| Session JWTs                     | Browser localStorage / Redis cache | n/a                |
| Reading-plan AI prompts/outputs  | Sent to your configured AI provider only | n/a          |

---

## What gets sent to AI providers

Every AI feature goes through one code path (`backend/shared/llm.py`) that decides where a prompt may go:

1. **Your own provider**, if you set one in Settings → AI Provider.
2. Otherwise **the server's default**. If that default is a cloud service, nothing is sent until you turn on the consent switch in Settings — until then AI features answer `AI_CONSENT_REQUIRED`.
3. If the operator set `AI_LOCAL_ONLY`, cloud providers are refused for everyone.

- **Ollama (local):** stays on the network where Ollama runs
- **Anthropic / OpenAI / OpenRouter:** sent to their public API

Settings shows which of these applies to you right now, and every piece of journal feedback records the provider and model that produced it (see the Audit log).

What is sent depends on the feature:

| Feature                  | Sent to AI                                                              |
|--------------------------|-------------------------------------------------------------------------|
| Speak Your Mind          | The text you type in the prompt box                                     |
| AI plan generation       | Your topic, duration, and language preference                           |
| Deep-dive study guide    | The journal entry text you select (decrypted in memory, sent in prompt) |
| Journal feedback         | The entry (first 4,000 characters), its mood, your current focus, themes and passage references from recent entries, and summaries of open threads. See [docs/HOW_FEEDBACK_WORKS.md](docs/HOW_FEEDBACK_WORKS.md) |
| Growth review            | Excerpts of that period's entries and check-in notes, themes, thread summaries |
| Scripture lookup         | Not an AI call. Only the reference (book, chapter) goes to `bolls.life`, and nothing at all if a translation is loaded locally |
| Voice entry              | Not handled by this app's server. Chrome, Edge and Safari transcribe speech with the browser vendor's speech service; the app receives only the resulting text |
| Reading-plan reflection  | The day's scripture passage and themes (no journal text)                |

If you do not want any of your reflections to leave your network, configure **Ollama** as your provider (Settings → AI Provider).

---

## Cookies

The app uses:

- **One first-party cookie** (`csrftoken`) for CSRF protection on session-authenticated endpoints.
- **localStorage** for the JWT access/refresh tokens (not a cookie, not sent automatically by the browser).
- No third-party cookies. No tracking cookies.

---

## Your rights

The app gives you four distinct rights, exposed directly in the UI:

### 1. Access — see your data

Settings → "Export My Data" produces a ZIP with your full account in JSON.

### 2. Portability — take your data elsewhere

Markdown exports for journal entries and highlights are available at:

- `Settings → Export Journal as Markdown`
- `Settings → Export Highlights as Markdown`
- `Settings → Export Growth Report as Markdown`

These are clean, portable, importable into Obsidian / Notion / any plain-text system.

### 3. Rectification — change your data

Profile, language, timezone, and AI provider settings are editable from Settings. Journal entries are editable from the journal itself.

### 4. Erasure — delete your data

Account deletion is currently a manual operator request. Until it is automated:

- Self-hosters: delete the user row and all foreign-key children.
- Hosted users: contact the operator and ask for account deletion.

A self-service "Delete my account" button is on the roadmap.

---

## Children

Devotional Journal is not directed at children under 13. The reflection prompts and AI conversations are not appropriate for minors. Operators must enforce the age requirement that applies in their jurisdiction.

---

## Operator responsibilities

If you operate a hosted instance of this app for other users, you are a data controller under common privacy law and you should:

- Publish your own privacy policy linking back to this document
- Disclose any analytics or telemetry you add
- Disclose your AI provider choice and the data-handling implications
- Provide a contact for privacy requests
- Honor data-deletion requests within a reasonable timeframe (30 days is a common standard)

---

## Changes to this document

Changes are tracked in [CHANGELOG.md](CHANGELOG.md). Material changes that affect user privacy will be called out in the changelog and, where possible, surfaced in-app.

Last reviewed: 2026-05-07.

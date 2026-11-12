# Changelog

All notable changes to Devotional Journal are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added — journal feedback, audit log, voice, private deployment
- **Journal feedback**: saving an entry returns a reflection, one scripture passage, why it was chosen, a meditation prompt and a Christlike next step (`POST /api/v1/journal/{id}/feedback/`)
- **Verified scripture**: models suggest references only; verse text is fetched from a Bible source (local database, then Bolls API). Default translations: World English Bible, then KJV (`SCRIPTURE_TRANSLATIONS`)
- **Audit log** (`/audit`, `GET /api/v1/journal/feedback/`): provider, model, inputs used, every candidate passage and its outcome, the selection rule; earlier records are kept when feedback is regenerated
- **Voice entry** in the journal editor and quick capture (browser speech recognition)
- **Growth tracking**: recurring themes feed the next prompt; threads are detected from entries; weekly/monthly reviews are stored and shown under Progress → Reviews
- **One AI layer** (`backend/shared/llm.py`) for every AI feature: per-user provider, explicit consent before a server-configured cloud AI is used (`allow_server_cloud_ai`), `AI_LOCAL_ONLY`, validated AI server addresses
- **Error envelope** on every API error (`error`, `code`, `suggestion`, `request_id`), request ids in logs and the `X-Request-ID` header, toasts / inline errors / error boundary in the UI, real health check
- **Private mesh deployment** for `journal.curlyphries.space`: `docker-compose.mesh.yml`, `MESH_ONLY`, host nginx config, `docs/MESH_DEPLOYMENT.md`
- Management commands: `load_translation`, `create_user`
- Docs: `docs/HOW_FEEDBACK_WORKS.md`, `docs/TROUBLESHOOTING.md`, `docs/MESH_DEPLOYMENT.md`; rewritten in-app Help and onboarding tour
- Tests: backend 80 → 189, frontend 2 → 81

### Changed
- `GET /api/v1/journal/` is paginated (`{count, next, previous, results}`)
- Devotional passages use the fetched text of the cited passage (WEB) instead of model-written "NIV/ESV" text
- Sign-in links are no longer written to the server log when a mail server is configured (override with `MAGIC_LINK_LOG`)
- `SECRET_KEY` is required in production settings

### Fixed
- Refresh tokens were accepted as access tokens
- A dozen reflections endpoints returned 500 (field-name drift, wrong call signatures, routes shadowed by the router)
- Reading page was a mock that discarded what the user wrote; three Progress tabs called non-existent URLs; onboarding focus buttons always failed
- A reflection, thread or focus could be attached to another user's journey; private plans could be enrolled in by id
- Server-side requests to user-supplied AI addresses were not validated (SSRF)
- Key derivation ran on every field decrypt (journal list of 20 entries: ~2s)

### Added — UX & marketing audit pass
- Marketing-focused README with value proposition, badges, FAQ, and audience targeting
- SEO meta tags, Open Graph tags, and Twitter Card metadata in `frontend/index.html`
- PWA `manifest.webmanifest` for "Add to Home Screen" support
- SVG favicon and Apple touch icon
- `robots.txt` blocking authenticated routes from indexing
- Trust-signal row on the login page (encryption · bilingual · BYOAI)
- Quick language toggle in the main navigation (EN ⇄ ES)
- Quick language toggle on the login page
- Skip-to-main-content link for keyboard / screen-reader users
- ARIA improvements on primary navigation (`aria-current`, `aria-label`)
- Footer links on login page (Source · Privacy · License)
- New i18n keys: `nav.plans`, `nav.focus`, `nav.progress`, `nav.insights`, `nav.help`, `nav.changeLanguage`, `nav.quickCapture`, `common.skipToContent`, full `login.*` namespace
- New documentation: `CHANGELOG.md`, `SECURITY.md`, `PRIVACY.md`, `ROADMAP.md`

### Changed
- Login page: Google OAuth promoted to the primary action, magic link is now a progressive-disclosure secondary option to reduce friction
- Login tagline upgraded from "Build consistent devotional habits" to "Daily Bible rhythm. Spiritual focus. Encrypted journaling."
- `Layout.tsx`: hardcoded "Plans / Focus / Progress / Insights" labels now go through `t()` and translate to Spanish
- Logo in the top nav is now a clickable link back to the dashboard
- `<title>` upgraded from "Devotional Journal" to a descriptive, search-friendly tagline
- Spanish translations corrected: added missing accents (`Iniciar sesión`, `Configuración`, `días`, `Reflexión`, etc.) and proper `Bilingüe` with diaeresis

### Fixed
- Spanish strings missing diacritics rendered as visibly broken text to native speakers — now correctly accented across all i18n keys

## [0.1.0] — 2026-05-03

Pre-release milestone — feature-complete on the core daily loop.

### Added
- Magic-link and Google OAuth authentication
- Encrypted journal with mood tagging and AI deep-dive study guides
- AI-curated devotionals with focus intentions and themes
- Reading plans (browse, AI-generate, manual builder, day-by-day editor)
- Bible reader (KJV local; Bolls API for additional translations)
- Highlights with color, notes, and Markdown export
- Daily reflections with life-area scoring
- Open-thread detection with status tracking (open / progressing / resolved)
- Streak tracking with confetti celebrations and Streak Saver modal
- Share cards for streak milestones
- Full data export (ZIP) and Markdown exports for journal, highlights, growth report
- Onboarding wizard for new users (focus + plan in 30 seconds)
- Quick Capture floating action button
- Help page with feature accordions
- Bilingual (EN / ES) i18n scaffolding
- Bring-your-own-AI: Ollama, Anthropic, OpenAI, OpenRouter
- Docker Compose stack (dev + prod) with Nginx, Postgres, Redis, Celery

[Unreleased]: https://github.com/curlyphries/devotional-journal/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/curlyphries/devotional-journal/releases/tag/v0.1.0

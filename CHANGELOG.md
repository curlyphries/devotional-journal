# Changelog

All notable changes to Devotional Journal are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

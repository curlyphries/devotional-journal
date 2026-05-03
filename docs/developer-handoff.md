# Devotional Journal — Developer Handoff Brief

> **Product:** Bilingual (EN/ES) men's devotional web app
> **Last updated:** 2026-05-03
> **Deploy:** Docker Compose on Ubuntu VPS (curlyphries.net/devotional-journal/)
> **Status:** Core features deployed. Needs visibility, retention, and bug-fix pass before public launch.

---

## 1. What This App Is

A Bible study web app built for men — fathers, leaders, men in recovery, men building faith discipline. Users set spiritual focus intentions, follow reading plans, journal with mood tracking, get AI-powered scripture recommendations, and track life-area growth over time.

**The emotional promise:** "I want to be consistent in my faith, but I keep falling off." This app gives you structure, accountability, and an AI companion that remembers what you're working through.

### Tech Stack

| Layer      | Stack                                           |
|------------|------------------------------------------------|
| Backend    | Django 5 + DRF, PostgreSQL, Celery + Redis     |
| AI         | Ollama (local) or Anthropic Claude (cloud)      |
| Frontend   | React 18 + TypeScript, TanStack Query, Tailwind |
| Auth       | JWT (custom), Magic Link, Google OAuth          |
| Deploy     | Docker Compose, Gunicorn, Nginx reverse proxy   |
| Encryption | Per-user AES encryption for journal content     |

### Backend Apps (9 total)

| App            | Purpose                                          |
|----------------|--------------------------------------------------|
| `users`        | Auth, profiles, magic links, Google OAuth, BYOAI |
| `bible`        | Translations, passages, search, highlights       |
| `plans`        | Reading plans, enrollment, daily progress        |
| `journal`      | Encrypted journal entries, mood, deep-dive AI    |
| `prompts`      | AI prompt service (Ollama/Anthropic abstraction) |
| `reflections`  | Daily reflections, life areas, threads, insights |
| `streaks`      | Journal streak tracking                          |
| `groups`       | Group models + Celery tasks (NO frontend yet)    |
| `billing`      | Empty — placeholder for premium tier             |

### Frontend Pages (16 routes)

| Route              | Page              | In nav? | Notes                        |
|--------------------|-------------------|---------|------------------------------|
| `/`                | Dashboard         | ✅      | Main hub, onboarding wizard  |
| `/journal`         | Journal History   | ✅      | List of past entries         |
| `/journal/new`     | Journal Entry     | —       | Create/edit with mood, scripture |
| `/plans`           | Plans             | ✅      | Browse, build, enroll        |
| `/devotional`      | Focus / Devotional| ✅      | Set focus, themed scripture  |
| `/progress`        | Progress          | ✅      | Studies, milestones, growth  |
| `/settings`        | Settings          | ✅      | Profile, AI provider config  |
| `/bible`           | Bible Reader      | —       | Read, highlight, search      |
| `/reflection`      | Daily Reflection  | —       | Multi-step reflection flow   |
| `/journey`         | Journey           | ❌ **HIDDEN** | Life-area self-assessment |
| `/insights`        | Insights History  | ❌ **HIDDEN** | Reflection + journal history |
| `/threads`         | Open Threads      | —       | AI-detected follow-up themes |
| `/reading/:id`     | Today's Reading   | —       | Plan day reading view        |
| `/login`           | Login             | —       | Magic link + Google OAuth    |
| `/auth/verify`     | Verify            | —       | Magic link verification      |
| `/auth/callback`   | OAuth Callback    | —       | Google OAuth return handler  |

---

## 2. What's Already Working Well

These are the product strengths. Don't break them; build on them.

### Core Daily Loop
`Dashboard → Focus → Read → Journal → Reflect` — each step feeds the next. The dashboard shows streak, focus, plan progress, and AI-generated insight. This is the habit engine.

### AI Features (Differentiators)
1. **"Speak Your Mind" (HeartPromptExplorer)** — User types what's on their heart, AI returns relevant scripture + reflection prompts. Lives on the dashboard.
2. **Open Threads** — AI detects recurring themes from journal/reflections (struggles, commitments, questions) and follows up: "Last week you mentioned anxiety about your job. How's that going?" Status tracking: open → progressing → resolved.
3. **AI Plan Builder** — Describe a topic, AI generates a multi-day reading plan with passages, themes, and prompts.
4. **Deep Dive Study Guides** — AI generates study guides from journal entries.

### Engagement Systems
- **Streak tracking** with confetti celebrations on milestones
- **Streak Saver modal** — appears after 6pm if user has 3+ day streak but hasn't journaled
- **Onboarding wizard** — new users pick a focus + plan within 30 seconds
- **Quick Capture FAB** — floating button always visible to capture a thought

### Data Model Strengths
- Bilingual baked into models: `title_en`/`title_es`, `theme_en`/`theme_es`, `description_en`/`description_es`
- Per-user AES encryption for journal content
- BYOAI: users can plug in their own OpenAI/Anthropic/Ollama/OpenRouter keys
- Reading plan ownership: `is_owned`, `is_public`, `created_by`

---

## 3. Known Bugs — Fix Before Anything Else

These are actively broken or exposed in production.

### 🔴 P0 — Fix Immediately

**3.1 — Private plans leak via detail endpoint**
- `PlanDetailView` (GET `/plans/<id>/`) only checks `is_active=True`. Any authenticated user can view any private plan by UUID.
- **Fix:** Add `Q(is_public=True) | Q(created_by=request.user)` to the detail queryset.
- **File:** `backend/apps/plans/views.py`, `PlanDetailView`

**3.2 — Auth redirect ignores base path**
- `frontend/src/api/client.ts` line 46: `window.location.href = '/login'`
- In production the app lives at `/devotional-journal/`. This redirect 404s.
- **Fix:** Use `window.location.href = import.meta.env.BASE_URL + 'login'` or the router's navigate.

**3.3 — JWT refresh tokens never invalidated**
- `refresh_access_token()` in `backend/apps/users/authentication.py` returns new tokens but the old refresh token stays valid for 7 days. Logout is client-side only.
- **Fix (quick):** Add `jti` claim to tokens. Maintain a Redis blacklist. Blacklist old `jti` on refresh and on logout.
- **Fix (better):** Migrate to `djangorestframework-simplejwt`.

### 🟡 P1 — Fix Before Public Launch

**3.4 — No production logging config**
- 13 modules use `logging.getLogger()` but no `LOGGING` dict exists in any settings file. All AI errors are invisible in production.
- **Fix:** Add structured `LOGGING` config in `backend/config/settings/prod.py`.

**3.5 — `datetime.utcnow()` deprecated**
- `backend/apps/users/authentication.py` line 54. Python 3.12+ deprecation.
- **Fix:** `datetime.now(timezone.utc)`

**3.6 — `PlanSaveView` accepts malformed day_numbers**
- No validation for duplicate, gapped, or out-of-range day_numbers.
- **Fix:** Validate `day_numbers` are `1..len(days)`, contiguous, no duplicates.

**3.7 — Gunicorn timeout vs AI generation**
- Timeout is 120s. Ollama plan generation for 28-day plans on 8B model can exceed this.
- **Fix:** Bump to 180s, or move AI generation to Celery with frontend polling.

---

## 4. Priority Roadmap

Ordered by **impact on user retention and growth**, not technical complexity.

### Sprint 1 — Surface & Retain (1-2 days)

**Goal:** Make existing features visible. Give users reasons to come back.

| # | Task | Why | Effort |
|---|------|-----|--------|
| 1.1 | Add `/journey` and `/insights` to nav (or merge into existing pages) | Two of the deepest features are unreachable. Journey is hidden, Insights is hidden. | S |
| 1.2 | Dashboard plan card → direct link to today's reading | Currently links to Plans list. User wants to go straight to today's scripture. | S |
| 1.3 | Add PWA manifest + "Add to Home Screen" prompt | Devotional time is a phone activity. This turns the web app into a phone app. | M |
| 1.4 | Fix the 3 P0 bugs (3.1, 3.2, 3.3) | Data leak, broken redirect, auth vulnerability. | M |

### Sprint 2 — Pull Users Back (2-3 days)

**Goal:** Notifications and sharing. Users who don't open the app need to be prompted.

| # | Task | Why | Effort |
|---|------|-----|--------|
| 2.1 | Wire up real SMTP in production | `.env.prod` still uses `console.EmailBackend`. No emails are being sent. | S |
| 2.2 | Daily reading reminder email (Celery beat) | "Your Day 4 reading is ready, [Name]" at user's preferred time. Biggest retention lever. | M |
| 2.3 | Streak-at-risk email | "You're about to lose your 14-day streak. Journal now to keep it alive." | S |
| 2.4 | Share cards for milestones | When a man hits a streak milestone or finishes a plan, generate a shareable image/card. This is organic growth. | M |

### Sprint 3 — Community (3-5 days)

**Goal:** Men's Bible study is communal. One man alone will churn. Five accountable men stick.

| # | Task | Why | Effort |
|---|------|-----|--------|
| 3.1 | Groups frontend (the backend `groups` app already has models + tasks) | "Invite a friend to this plan." Shared enrollment, shared progress. | L |
| 3.2 | Group discussion prompts | AI generates discussion questions from the day's reading for group use. | M |
| 3.3 | Accountability check-ins | "How are you doing with your focus this week?" — visible to the group. | M |

### Sprint 4 — Growth & Analytics (2-3 days)

**Goal:** Know what's working. Give users proof they're growing.

| # | Task | Why | Effort |
|---|------|-----|--------|
| 4.1 | Add product analytics (PostHog or Plausible) | You have zero visibility into what features users actually use. | S |
| 4.2 | Landing page (pre-login marketing page) | Currently: login form. Needed: story, screenshots, social proof, CTA. | M |
| 4.3 | ~~30/60/90 day growth report~~ ✅ | Growth report export at `GET /me/export/growth/` — Markdown with stats, area averages, mood distribution. | ~~L~~ Done |
| 4.4 | Year-in-review | Annual summary. Shareable. Drives December/January re-engagement. | L |

---

## 5. Architecture Notes for New Developer

### API Pattern
All endpoints live under `/api/v1/`. DRF views with JWT auth. Default permission is `IsAuthenticated` unless noted. Throttling is configured globally with per-endpoint overrides.

```
/api/v1/auth/          → users app (login, register, refresh, Google OAuth)
/api/v1/me/            → users app (profile CRUD, data export)
/api/v1/bible/         → bible app (translations, passages, search)
/api/v1/plans/         → plans app (CRUD, enroll, advance, today, generate, save)
/api/v1/journal/       → journal app (entries CRUD, deep-dive)
/api/v1/prompts/       → prompts app (AI status, exploration)
/api/v1/groups/        → groups app (models exist, views TBD)
/api/v1/               → reflections app (reflections, threads, focus, dashboard)
```

### Complete API Reference

> All paths are relative to `/api/v1/`. Methods marked 🔓 are `AllowAny` (no auth needed).

#### Auth — `/auth/`

| Method | Path | Description |
|--------|------|-------------|
| POST 🔓 | `auth/magic-link/request/` | Send magic link email (rate-limited) |
| POST 🔓 | `auth/magic-link/verify/` | Verify magic link token → JWT tokens |
| POST | `auth/refresh/` | Refresh JWT access token (rotates refresh token) |
| POST | `auth/logout/` | Logout — blacklists access + refresh tokens |
| POST | `auth/test-ai/` | Test user's AI provider connection |
| GET/PUT | `auth/profile/` | Get or update user profile |
| GET 🔓 | `auth/google/login/` | Initiate Google OAuth flow |
| GET 🔓 | `auth/google/callback/` | Google OAuth callback |
| POST 🔓 | `auth/google/exchange/` | Exchange OAuth code for JWT tokens |
| POST 🔓 | `auth/google/token/` | Exchange Google ID token for JWT tokens |
| POST 🔓 | `auth/dev-login/` | Dev-only: login by email (DEBUG=true only) |

#### Profile & Export — `/me/`

| Method | Path | Description |
|--------|------|-------------|
| GET/PUT | `me/` | Get or update profile |
| GET | `me/export/` | Full data export — ZIP with all JSON files (GDPR) |
| GET | `me/export/journal/` | Journal entries as Markdown |
| GET | `me/export/highlights/` | Verse highlights as Markdown, grouped by book |
| GET | `me/export/growth/` | Growth report — stats, area averages, mood distribution |

#### Bible — `/bible/`

| Method | Path | Description |
|--------|------|-------------|
| GET 🔓 | `bible/translations/` | List local Bible translations |
| GET 🔓 | `bible/read/` | Read a passage (`?translation=KJV&book=John&chapter=3&verse_start=16&verse_end=17`) |
| GET 🔓 | `bible/search/` | Search verses (`?translation=KJV&query=love`) |
| GET 🔓 | `bible/bolls/translations/` | List external Bolls Bible API translations |
| GET 🔓 | `bible/bolls/read/` | Read passage from Bolls API (KJV, ASV, YLT, WEB, RVR1960) |
| GET 🔓 | `bible/bolls/search/` | Search via Bolls API |
| GET 🔓 | `bible/bolls/verify/` | Verify a passage reference exists |
| GET | `bible/highlights/` | List user's verse highlights |
| POST | `bible/highlights/` | Create a highlight (`{book, chapter, verse_start, verse_end, color, note, translation}`) |
| GET/PUT/DELETE | `bible/highlights/<uuid>/` | Get, update, or delete a highlight |

#### Reading Plans — `/plans/`

| Method | Path | Description |
|--------|------|-------------|
| GET | `plans/` | List available reading plans (public + user's own) |
| POST | `plans/generate/` | AI-generate a plan (`{topic, duration_days, ...}`) |
| POST | `plans/save/` | Save a generated or manual plan |
| GET | `plans/<uuid>/` | Plan detail (must be public or owned by user) |
| DELETE | `plans/<uuid>/delete/` | Delete a plan (owner only) |
| POST | `plans/<uuid>/enroll/` | Enroll in a plan |
| GET | `plans/enrolled/` | List user's active enrollments |
| GET | `plans/enrolled/<uuid>/today/` | Get today's reading for an enrollment |
| POST | `plans/enrolled/<uuid>/advance/` | Mark today complete, advance to next day |

#### Journal — `/journal/`

| Method | Path | Description |
|--------|------|-------------|
| GET | `journal/` | List entries (`?date_from=&date_to=&mood=`) |
| POST | `journal/` | Create entry (`{content, mood_tag, date, ...}`) |
| GET/PATCH/DELETE | `journal/<uuid>/` | Get, update, or delete an entry |
| POST | `journal/<uuid>/deep-dive/` | Generate AI study guide from a journal entry |
| GET | `journal/export/` | Export entries as JSON (`?date_from=&date_to=`, max 365 days) |

#### AI & Prompts — `/prompts/`

| Method | Path | Description |
|--------|------|-------------|
| GET | `prompts/ai-status/` | Check if configured LLM backend is reachable |
| POST | `prompts/generate/` | Generate reflection prompts from a passage |
| POST | `prompts/explore/` | "Speak Your Mind" — freeform input → scripture + prompts + plan suggestions |
| GET | `prompts/explorations/` | List saved explorations (`?bookmarked=true`) |
| GET/DELETE | `prompts/explorations/<uuid>/` | Get or delete a saved exploration |
| POST | `prompts/explorations/<uuid>/bookmark/` | Toggle bookmark on an exploration |

#### Reflections & Focus — `/` (root of `/api/v1/`)

**ViewSet endpoints** (DRF router — standard CRUD):

| Resource | List/Create | Detail | Custom Actions |
|----------|-------------|--------|----------------|
| `life-areas/` | GET/POST | GET/PUT/PATCH/DELETE `<uuid>/` | — |
| `journeys/` | GET/POST | GET/PUT/PATCH/DELETE `<uuid>/` | — |
| `reflections/` | GET/POST | GET/PUT/PATCH/DELETE `<uuid>/` | — |
| `trends/` | GET/POST | GET/PUT/PATCH/DELETE `<uuid>/` | — |
| `threads/` | GET/POST | GET/PUT/PATCH/DELETE `<uuid>/` | — |
| `thread-prompts/` | GET/POST | GET/PUT/PATCH/DELETE `<uuid>/` | — |
| `focus/` | GET/POST | GET/PUT/PATCH/DELETE `<uuid>/` | `active/` (GET), `today/` (GET), `<uuid>/complete/` (POST), `<uuid>/passages/` (GET) |
| `passages/` | GET | GET `<uuid>/` | `<uuid>/mark_read/` (POST), `<uuid>/reflect/` (POST), `<uuid>/deep_dive/` (POST) |
| `study-sessions/` | GET | GET `<uuid>/` | `summary/` (GET) |

**Standalone endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| GET | `dashboard/stats/` | Unified dashboard — streak, focus, plan, highlights, life areas, insight |
| GET | `thread-prompts/pending/` | Get open threads needing follow-up (max 2) |
| POST | `thread-prompts/<uuid>/respond/` | Respond to a thread (`{response: better/same/worse/resolved, expanded_text}`) |
| GET | `milestones/` | User milestones — next milestone, recent achievements, stats |
| GET | `trends/growth/` | Growth visualization — life areas, weekly activity, focus history |
| GET | `insights/scripture/` | Scripture insights based on recent reflections and focus |

**Crew (AI Agent):**

| Method | Path | Description |
|--------|------|-------------|
| GET | `crew/health/` | Agent health check |
| POST | `crew/weekly-review/` | Trigger AI weekly review |
| POST | `crew/monthly-recap/` | Trigger AI monthly recap |
| POST | `crew/ask-agent/` | Freeform agent query |

#### Groups — `/groups/` (Phase 2 — backend ready, no frontend yet)

| Method | Path | Description |
|--------|------|-------------|
| GET | `groups/` | List user's groups |
| POST | `groups/` | Create a group |
| GET | `groups/<uuid>/` | Group detail |
| POST | `groups/<uuid>/join/` | Join via invite code (`{invite_code}`) |
| DELETE | `groups/<uuid>/leave/` | Leave a group |
| GET | `groups/<uuid>/engagement/` | Engagement metrics (leaders only) |
| POST | `groups/<uuid>/set-plan/` | Assign reading plan to group (leaders only) |

#### Admin — (staff only)

| Method | Path | Description |
|--------|------|-------------|
| GET | `admin/audits/` | List devotional audits (`?status=&days=&min_accuracy=`) |
| GET | `admin/audits/dashboard/` | Audit dashboard stats |
| GET | `admin/quality-report/` | Devotional quality report |

#### System

| Method | Path | Description |
|--------|------|-------------|
| GET 🔓 | `health/` | Health check → `{"status": "ok"}` |

### AI Service Abstraction
`backend/apps/prompts/services.py` defines `PromptService` (abstract) with `OllamaPromptService` and `AnthropicPromptService` implementations. Factory: `get_prompt_service()` reads `LLM_BACKEND` env var. Methods:
- `generate_reflection_prompts()` — scripture → questions
- `generate_reading_plan()` — topic → multi-day plan JSON
- `explore_heart_prompt()` — freeform input → scripture + prompts
- `generate_discussion_guide()` — passages → group discussion guide (Anthropic implementation is a stub)

### Frontend Patterns
- **State:** TanStack Query for server state, `useState` for local. No Redux/Zustand.
- **Auth:** `AuthContext` with JWT in localStorage. `client.ts` interceptor auto-refreshes on 401.
- **Styling:** Tailwind with CSS custom properties for theming (`bg-bg-primary`, `text-text-primary`, etc.)
- **i18n:** `react-i18next` for translation keys (partially implemented — some labels are hardcoded English).

### Deployment
```bash
# Pull, build, deploy
ssh curlyphries@curlyphries.net
cd /home/curlyphries/projects/devotional-journal
git pull origin master
docker-compose -f docker-compose.prod.yml --env-file .env.prod build dj-backend dj-frontend
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d dj-backend dj-frontend
```

Frontend Nginx handles sub-path routing (`/devotional-journal/`). API requests proxied to Django. Static assets served with 30d cache + immutable headers.

---

## 6. Testing State

**Backend:** 120 lines of tests in `apps/plans/tests.py` + `conftest.py` fixtures. Coverage: plan CRUD, enrollment, advancement. **No tests for:** save endpoint, generate endpoint, delete endpoint, auth flow, AI service, reflections, journal, threads.

**Frontend:** 1 test file (`Layout.test.tsx`, 34 lines, 2 assertions). Effectively zero coverage.

**Priority tests to write:**
1. `PlanSaveView` — manual + AI save paths
2. `PlanGenerateView` — throttle, validation, partial plan recovery
3. `PlanDeleteView` — ownership check, 404 for non-owned
4. Auth refresh + blacklist (once implemented)
5. Frontend: PlanBuilderModal flow (form → generate → preview → save)

---

## 7. Files You'll Touch Most

```
backend/
  apps/plans/views.py          — plan CRUD, generate, save, delete
  apps/prompts/services.py     — AI abstraction (Ollama + Anthropic)
  apps/reflections/views.py    — dashboard stats, threads, focus, insights (1500+ lines)
  apps/users/authentication.py — JWT generation, refresh, validation
  config/settings/prod.py      — production config
  config/settings/base.py      — shared config

frontend/
  src/pages/DashboardPage.tsx   — main hub (682 lines)
  src/pages/PlansPage.tsx       — plan list, enroll, delete
  src/pages/DevotionalPage.tsx  — focus + themed scripture (846 lines)
  src/components/PlanBuilderModal.tsx — AI + manual plan creation
  src/components/HeartPromptExplorer.tsx — "Speak Your Mind" AI
  src/api/client.ts             — Axios with JWT interceptor
  src/context/AuthContext.tsx    — Auth state
```

---

## 8. What NOT to Do

1. **Don't rewrite the AI service to use SDKs.** The raw `httpx` approach works and keeps dependencies minimal. The abstraction layer is clean.
2. **Don't add a state management library.** TanStack Query handles server state well. Local state with `useState` is fine at this scale.
3. **Don't try to compete with YouVersion's Bible reader.** The built-in reader is "just enough." The differentiators are the AI features, journaling, and thread follow-ups.
4. **Don't touch the encryption system** without reading `shared/encryption.py` thoroughly. Per-user salt + root key. Breaking this loses all journal data.
5. **Don't add features before surfacing existing ones.** Journey and Insights pages are hidden. The HeartPromptExplorer is only on the dashboard. Thread follow-ups are buried in Progress. Surface before you build.

---

## 9. Success Metrics (What "Done" Looks Like)

For public launch readiness:
- [x] All P0 bugs fixed (plan data leak, login redirect, JWT refresh reuse)
- [x] Hidden pages surfaced in navigation (Journey in Progress tab, Insights in nav)
- [ ] PWA manifest installed, "Add to Home Screen" working on iOS + Android
- [ ] Real SMTP sending emails in production
- [ ] Daily reminder email working via Celery beat
- [x] Sharing mechanism (streak share card, achievement share card on dashboard + milestones)
- [x] Data export — full JSON ZIP, journal/highlights/growth as Markdown (Settings → Export)
- [ ] Landing page with app screenshots and CTA before login
- [ ] Product analytics capturing DAU, feature usage, and drop-off points

### Export Endpoints (New)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/me/export/` | Full data export — ZIP with JSON files (GDPR) |
| GET | `/api/v1/me/export/journal/` | Journal entries as Markdown |
| GET | `/api/v1/me/export/highlights/` | Verse highlights as Markdown grouped by book |
| GET | `/api/v1/me/export/growth/` | Growth report with stats, area averages, mood distribution |

### Share Cards (New)

`ShareCard` component (`frontend/src/components/ShareCard.tsx`) generates shareable PNG images via Canvas API. Three variants: `streak`, `achievement`, `plan_complete`. Supports Web Share API on mobile, falls back to download. Integrated on Dashboard (streak badge) and Milestones (achievements).

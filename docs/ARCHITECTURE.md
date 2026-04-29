# Architecture

This document describes the system design, data flow, and key technical decisions for the Devotional Journal platform.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Service Topology](#service-topology)
3. [Authentication](#authentication)
4. [Encryption Model](#encryption-model)
5. [AI Crew Pattern](#ai-crew-pattern)
6. [Task Queue](#task-queue)
7. [Data Models](#data-models)
8. [API Design](#api-design)
9. [Frontend Architecture](#frontend-architecture)
10. [Security Decisions](#security-decisions)

---

## System Overview

Devotional Journal is a bilingual (English/Spanish) private journaling platform with AI-assisted reflection. The core design constraint is **privacy by default**: journal entries, reflections, and personal notes are encrypted at rest using per-user keys — the server cannot read plaintext user content without the user's session context.

```
┌─────────────────────────────────────────────────────┐
│                     Browser / Mobile                │
│                   React (TypeScript)                │
└────────────────────────┬────────────────────────────┘
                         │ HTTPS (JWT Bearer)
┌────────────────────────▼────────────────────────────┐
│               Django REST Framework API             │
│          Authentication · Permissions · Throttling  │
└──────┬──────────┬───────────────┬───────────────────┘
       │          │               │
┌──────▼──┐  ┌────▼────┐  ┌──────▼──────┐
│PostgreSQL│  │  Redis  │  │  Celery     │
│(encrypted│  │(cache + │  │  Workers    │
│ content) │  │ broker) │  │(AI + email) │
└──────────┘  └─────────┘  └──────┬──────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │         LLM Backend         │
                    │  Ollama (dev) · OpenAI ·    │
                    │  Anthropic · OpenRouter     │
                    └────────────────────────────┘
```

---

## Service Topology

| Service | Technology | Port (dev) | Purpose |
|---------|-----------|------------|---------|
| `backend` | Django 5 + DRF | 8001 | REST API, auth, business logic |
| `frontend` | React 18 + Vite | 3001 | SPA web client |
| `db` | PostgreSQL 16 | 5433 | Primary data store |
| `redis` | Redis 7 | 6380 | Celery broker + result backend |
| `celery` | Celery 5 | — | Async task workers |
| `celery-beat` | Celery Beat | — | Scheduled tasks (weekly review, streak updates) |

All services are defined in `docker-compose.yml` and configured entirely through environment variables — no secrets are baked into images or source code.

---

## Authentication

The platform uses **passwordless authentication** with two supported flows:

### Magic Link Flow

```
Client                    Backend                      Email
  │                          │                           │
  ├─POST /auth/magic-link/───►│                           │
  │   { email }              │── generate SHA-256 token ─┤
  │                          │── send magic link ────────►│
  │◄─ 200 OK ────────────────┤                           │
  │                          │                           │
  │  (user clicks email link)│                           │
  │                          │                           │
  ├─POST /auth/magic-link/───►│                           │
  │   verify/ { token }      │── hash + lookup token     │
  │                          │── invalidate token        │
  │◄─ { access, refresh } ───┤                           │
```

- Raw tokens are never stored; only their SHA-256 hash persists in the database
- Tokens expire after 15 minutes (`MAGIC_LINK_EXPIRY_MINUTES`)
- Requesting a magic link for an unknown email silently no-ops (prevents account enumeration)

### Google OAuth Flow

```
Client          Backend              Google
  │                │                    │
  ├─GET /google/──►│                    │
  │   login/       │── state + redirect►│
  │◄─ redirect ────┤                    │
  │                                     │
  │  (user authenticates at Google)     │
  │                                     │
  │◄────────────── callback with code ──┤
  │                │                    │
  │         ┌──────▼──────┐             │
  │         │ verify state│             │
  │         │ exchange code│◄──────────►│
  │         │ get userinfo│             │
  │         └──────┬──────┘             │
  │                │── one-time code ──►session
  │◄─ redirect ?code=<otp> ────────────┤
  │                │
  ├─POST /google/──►│
  │   exchange/     │── pop session key
  │◄─ { access,    ◄┤
  │    refresh }    │
```

JWT tokens are **never placed in redirect URLs**. Instead, a cryptographically random one-time code is stored server-side in the session; the frontend redeems it via a POST request within a 5-minute window. This prevents tokens appearing in browser history, server access logs, or referrer headers.

### JWT Structure

```python
{
    "user_id": "<uuid>",
    "exp":     <unix timestamp>,
    "iat":     <unix timestamp>,
    "type":    "access" | "refresh"
}
```

Signed with `HS256` using `SECRET_KEY`. Access tokens are short-lived; refresh tokens are longer-lived and rotated on use.

---

## Encryption Model

All sensitive user content is **encrypted at rest** using symmetric encryption. The design prevents the database alone from being sufficient to read user data.

### Key Hierarchy

```
ENCRYPTION_ROOT_KEY  (environment variable, never in DB)
        │
        │  PBKDF2-HMAC-SHA256
        │  600,000 iterations (NIST SP 800-132)
        │  salt = per-user random 32 bytes (stored in users table)
        ▼
  user_derived_key  (32 bytes → base64url → Fernet key)
        │
        │  Fernet (AES-128-CBC + HMAC-SHA256)
        ▼
  encrypted_content  (stored as BinaryField in PostgreSQL)
```

### What Is Encrypted

| Model | Encrypted Fields |
|-------|-----------------|
| `JournalEntry` | `encrypted_content` |
| `DailyReflection` | `encrypted_reflection`, `encrypted_gratitude`, `encrypted_struggle`, `encrypted_tomorrow_intention` |
| `UserJourney` | `encrypted_specific_struggle` |
| `OpenThread` | `encrypted_summary`, `encrypted_resolution_note` |
| `FocusIntention` | `encrypted_intention` |
| `User` | `ai_api_key` (encrypted via `set_ai_api_key()`) |

### What Is NOT Encrypted

Metadata required for queries (dates, scripture references, area scores, AI-generated insights) is stored in plaintext. AI-generated content is considered non-sensitive — it reflects the AI's output, not the user's raw thoughts.

### Group Privacy Guarantee

Group leaders see only aggregate engagement metrics (streak counts, reflection frequency). They have no access to any encrypted content. This is enforced at the permission layer (`IsOwner`) and architectural separation — the `GroupEngagementSnapshot` model stores only counts, never content references.

---

## AI Crew Pattern

AI-powered features use a **multi-agent crew** pattern where specialised agents collaborate to produce richer output than a single LLM call.

```
┌─────────────────────────────────────────┐
│              Crew Coordinator           │
│  (synthesises outputs from all agents) │
└───┬─────────┬──────────┬───────────────┘
    │         │          │
┌───▼──┐ ┌───▼───┐ ┌────▼──────────┐
│Mentor│ │Scrip- │ │   Spiritual   │
│Agent │ │ture   │ │   Director    │
│      │ │Scholar│ │    Agent      │
└──────┘ └───────┘ └───────────────┘
```

### Task Types

| Task | Agents Involved | Trigger |
|------|----------------|---------|
| `DailyInsightTask` | Mentor → Coordinator | On reflection save |
| `WeeklyReviewTask` | All agents | Celery Beat (Sunday night) |
| `MonthlyRecapTask` | All agents | Celery Beat (month end) |
| `ThreadDetectionTask` | Standalone (Ollama) | On journal save |

### LLM Backend Abstraction

The `PromptService` base class abstracts over LLM providers. The active backend is selected at runtime via `LLM_BACKEND`:

```
LLM_BACKEND=ollama     → OllamaPromptService
LLM_BACKEND=anthropic  → AnthropicPromptService
LLM_BACKEND=openai     → OpenAIPromptService
```

A fallback chain is supported: if the primary backend fails, `LLM_FALLBACK_BACKEND` is tried before returning a graceful error.

---

## Task Queue

Celery handles all work that should not block an HTTP response:

| Task | Queue | Schedule |
|------|-------|----------|
| `send_magic_link_email` | default | on-demand |
| `generate_daily_insight` | ai | on-demand (post-save) |
| `generate_weekly_review` | ai | Sunday 10 PM (user timezone) |
| `generate_monthly_recap` | ai | 1st of month |
| `update_streak` | default | daily midnight |
| `compute_alignment_trends` | default | weekly |

Redis serves as both the broker and result backend. In production, separate queues (`default`, `ai`) allow AI tasks to be scaled independently without starving email delivery.

---

## Data Models

### Core Relationships

```
User
 ├── JournalEntry (1:many)
 ├── UserJourney (1:many)
 │    └── DailyReflection (1:many)
 │         └── OpenThread (1:many)
 ├── FocusIntention (1:many)
 ├── UserStreak (1:1)
 ├── UserPlanEnrollment (1:many)
 └── GroupMembership (1:many)
      └── Group
```

### Key Design Decisions

- **UUID primary keys** on `User` — avoids sequential ID enumeration
- **`encryption_key_salt`** is generated once at user creation and never changes — re-encryption on key rotation would require a migration job
- **`area_scores`** is a `JSONField` — life areas (integrity, faith, work, etc.) can be added without schema migrations
- **`scripture_themes`** is a `JSONField` array — populated by LLM, queryable for trend analysis

---

## API Design

- All endpoints are under `/api/v1/`
- Authentication: `Authorization: Bearer <access_token>`
- Pagination: cursor-based via `StandardPagination` (page size 20)
- Filtering: `django-filters` on list endpoints (date range, mood, etc.)
- Throttling: 5 req/hr (magic link), 10 req/hr (auth), 1000 req/hr (authenticated users)

See [API.md](API.md) for full endpoint reference.

---

## Frontend Architecture

```
src/
├── components/       # Shared UI components
├── pages/            # Route-level page components
├── hooks/            # Custom React hooks (auth, data fetching)
├── stores/           # Zustand state (auth token, user profile)
├── api/              # Typed API client (axios + React Query)
└── lib/              # Utilities (date formatting, encryption helpers)
```

Auth tokens are stored in memory (Zustand) and in `localStorage` for persistence across page refreshes. The access token is refreshed automatically when a 401 is received, using the refresh token.

---

## Security Decisions

| Decision | Rationale |
|----------|-----------|
| Passwordless auth only | Eliminates password breach risk entirely |
| Per-user encryption keys | A DB compromise alone cannot decrypt any content |
| JWT never in URLs | Prevents token leakage via browser history, logs, referrer headers |
| `REMOTE_ADDR` only for IP checks | `X-Forwarded-For` is trivially spoofable; Tailscale access control requires real IP |
| Magic link no-op for unknown emails | Prevents account enumeration by timing/response differences |
| PBKDF2 at 600k iterations | NIST SP 800-132 (2023) recommendation for SHA-256 |
| `send_default_pii=False` in Sentry | Ensures error reports never contain user content |
| `SECURE_REFERRER_POLICY: strict-origin-when-cross-origin` | Prevents URL leakage to third-party domains via Referer header |

---

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup, environment variable reference, and Nginx/reverse proxy configuration.

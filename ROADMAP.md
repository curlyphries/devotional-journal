# Roadmap

This roadmap captures the **product** direction. The technical priority list — bugs, refactors, infrastructure — lives in [`docs/developer-handoff.md`](docs/developer-handoff.md).

The order below is by **impact on user retention and growth**, not by technical complexity.

---

## ✅ Shipped

The core daily loop is feature-complete:

- Magic-link + Google OAuth authentication
- Encrypted journal with mood tagging
- AI-curated devotionals tied to user-set focus intentions
- Reading plans (browse, AI-generate, manual builder)
- Bible reader with highlights, notes, and Bolls API multi-translation support
- Daily reflections with life-area scoring
- AI thread detection with status tracking
- Streak tracking with confetti and Streak Saver modal
- Onboarding wizard for new users
- Quick Capture floating action button
- Help page with feature accordions
- Bilingual (EN / ES) i18n scaffolding
- Bring-your-own-AI for Ollama / Anthropic / OpenAI / OpenRouter
- Full data export (ZIP + Markdown)
- Share cards for milestones
- Docker Compose deployment

---

## 🎯 Next: Surface & retain

**Goal:** make existing features visible. Give users reasons to come back.

| Item | Why | Status |
|------|-----|--------|
| Add `/journey` to the main nav | Currently unreachable — life-area self-assessment is one of the deepest features | TBD |
| Dashboard plan card → direct link to today's reading | Currently links to plan list. User wants today's scripture, not a list. | TBD |
| PWA install prompt + Add to Home Screen | Devotional time is a phone activity. Manifest is now in place. | In progress |
| Fix P0 bugs from `developer-handoff.md` | Private-plan disclosure, broken redirect under base path, JWT refresh invalidation | TBD |

---

## 📬 Pull users back (notifications & sharing)

**Goal:** Users who don't open the app need to be prompted, gently.

| Item | Why |
|------|-----|
| Wire real SMTP in production | `.env.prod` still uses console backend; no emails are being sent |
| Daily reading reminder email (Celery beat) | "Your Day 4 reading is ready, [Name]" at the user's preferred time. Biggest retention lever. |
| Streak-at-risk email | "You're about to lose your 14-day streak. Journal now to keep it alive." |
| Email digest opt-out per channel | Users should control reminder, streak-saver, and weekly-summary emails independently |

---

## 👥 Community

**Goal:** men's Bible study is communal. One man alone will churn. Five accountable men will stick.

| Item | Why |
|------|-----|
| Groups frontend | `groups` app already has models + Celery tasks; needs UI |
| "Invite a friend to this plan" | Shared enrollment, shared progress |
| Group discussion prompts | AI generates discussion questions from the day's reading for group use |
| Accountability check-ins | "How are you doing with your focus this week?" — visible to the group |
| Crew threads | Shared follow-up prompts among accountability partners |

---

## 📊 Growth & analytics

**Goal:** know what's working. Give users proof they're growing.

| Item | Why |
|------|-----|
| Opt-in product analytics (PostHog or Plausible) | Currently zero visibility into what features users actually use |
| Public landing page | Pre-login marketing page with screenshots, story, social proof |
| Year-in-review | Annual summary, shareable, drives December/January re-engagement |
| Weekly automated digest | "Here's what your week looked like" — one email summarizing reflections, highlights, and growth |
| Self-service account deletion | Currently manual; should be a button in Settings |

---

## 🔮 Future / open ideas

These aren't committed but they are the obvious next steps once the above is done:

- **Audio devotionals** — text-to-speech for the daily passage and reflection
- **Voice journaling** — speech-to-text for journal entries
- **Mobile native app** — wrapper around the PWA, push notifications
- **Shared reading plans marketplace** — public plans rated and forkable
- **Accountability partner matching** — opt-in for people without an existing group
- **Reading plan from a sermon** — paste a sermon transcript, generate a 7-day plan around it
- **Multi-translation diff view** — read the same passage in three translations side by side
- **Translation expansion** — Portuguese, French, Korean
- **Calendar / Google Calendar integration** — "Block 15 minutes for devotional time"
- **Family / household mode** — multiple profiles under one account
- **Apple Health / Whoop sleep correlation** — does your reflection mood correlate with sleep quality?
- **Premium tier** — hosted instance with managed AI, no key required (the `billing` Django app is a placeholder)

---

## How decisions are made

This is an open-source side project. Roadmap order can change for any of these reasons, in this order of weight:

1. A real user has been hitting a real problem repeatedly
2. A security or data-loss issue is found
3. A small change has disproportionate retention impact
4. The maintainer is excited about it and the work is its own reward

Pull requests that move items above the line are welcome — open an issue first if the item is large.

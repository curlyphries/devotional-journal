# Integration Roadmap — Connecting the Silos

**Goal:** Transform disconnected features into a cohesive, evolving spiritual journey.

**Status key:** ✅ Done · 🔶 Partial · ❌ Not started

---

## Audit: What's Actually Built vs Connected

| Feature | Model Exists | API Exists | Frontend Uses It | Connected to Focus |
|---------|-------------|-----------|----------------|--------------------|
| FocusIntention | ✅ | ✅ | ✅ Dashboard | — |
| DevotionalPassage | ✅ | ✅ | ✅ Dashboard | ✅ Generated from focus |
| JournalEntry | ✅ | ✅ | ✅ JournalPage | 🔶 Context passed, not stored |
| ReadingPlan / Enrollment | ✅ | ✅ | ✅ PlansPage | ❌ No focus awareness |
| OpenThread | ✅ | ✅ | 🔶 JournalPage (pending) | ❌ Not surfaced in UI |
| UserJourney | ✅ | ✅ | ❌ Nowhere | ❌ Not used |
| DailyReflection | ✅ | ✅ | ❌ Nowhere | ❌ Not used |
| AlignmentTrend | ✅ | 🔶 | ❌ ProgressPage (stub) | ❌ Not computed |
| AI Crew (weekly/monthly) | ✅ Celery tasks | ✅ | ❌ Not surfaced | 🔶 Uses journey if exists |

---

## Phase 1 — The Critical Connections (1–2 weeks)

These are the joins that make everything feel cohesive. Implement in order.

### 1A · Store focus_intention on JournalEntry

**Why:** The focus context is already *passed* to the journal AI prompt but never persisted.
Without this, you can't show "entries from your Consistency focus" or compute per-focus trends.

**Backend change:**
- Add `focus_intention = ForeignKey(FocusIntention, null=True, on_delete=SET_NULL)` to `JournalEntry`
- Migration
- Update `JournalEntrySerializer` to include `focus_intention_id`
- Update `JournalEntryViewSet.perform_create()` to auto-assign the user's active focus

**Frontend change:**
- None required — happens automatically on save

---

### 1B · Focus-aware Reading Plan insights

**Why:** This is the single highest-impact connection. When a user reads a plan passage,
the AI insight should reference their active focus — making the same scripture feel
personally relevant to what they're working on right now.

**Backend change — `ReadingPage` API call:**
- `GET /api/v1/reflections/reading/{enrollment_id}/day/{day}/insight/`
- Already returns AI insight — modify to fetch active `FocusIntention` and inject into prompt:

```python
# In generate_theme_insight() or equivalent
active_focus = FocusIntention.objects.filter(
    user=user, status='active'
).order_by('-created_at').first()

focus_context = ""
if active_focus:
    focus_context = f"\n\nUSER'S CURRENT FOCUS: {active_focus.intention_text}\nThemes: {', '.join(active_focus.themes)}\nConnect the passage to this focus if relevant."
```

**Frontend change — `ReadingPage.tsx`:**
- If insight contains a focus connection, render a highlighted "Your Focus" callout block

---

### 1C · Surface OpenThreads properly in JournalPage

**Why:** The model, Celery detection task, and API endpoint exist
(`/thread-prompts/pending/`) — but the UI just fetches them without rendering check-ins.

**Frontend change — `JournalPage.tsx`:**
- Render the `ThreadPromptCard` component (already built in `components/ThreadPromptCard.tsx`)
  at the top of the journal form when pending threads exist
- Wire up Better/Same/Worse/Skip responses to `POST /api/v1/reflections/thread-prompts/{id}/respond/`
- Show max 2 prompts per session (already enforced by the API)

---

## Phase 2 — UserJourney as the Spine (1 week)

The `UserJourney` model is the intended unifying structure — it ties together
focus, reading plan, open threads, and daily reflections into one named journey.
Currently nothing creates or uses it.

### 2A · Journey creation on onboarding

**Dashboard wizard already exists** for focus + plan selection. Extend it to create a
`UserJourney` that links them:

```
Step 1: "What do you want to work on?" → goal_statement + focus_areas
Step 2: "How long?" → duration_days (7 / 14 / 30 / 90)
Step 3: "Pick a reading plan (or skip)" → reading_plan FK
Step 4: Creates UserJourney + FocusIntention + ReadingPlan enrollment atomically
```

**Backend:** `POST /api/v1/reflections/journeys/` — already exists, wire up `perform_create`
to also create the `FocusIntention` and `UserPlanEnrollment` in one transaction.

**Frontend:** Extend the existing dashboard wizard 3 steps → wrap in `UserJourney`.

### 2B · JourneyPage — show the active journey

`JourneyPage.tsx` exists but is a stub. Wire it to `GET /api/v1/reflections/journeys/active/`:

```
┌─────────────────────────────────────────┐
│  📍 Your Journey: "30 Days of Discipline" │
│  Day 12 of 30                            │
│  ──────────────────────────────          │
│  🎯 Focus: Self-Control                  │
│  📖 Reading Plan: James — Day 12        │
│  🧵 Open Threads: 2 active              │
│  📊 This week: Faith ↑ Self-Control ↑   │
└─────────────────────────────────────────┘
```

---

## Phase 3 — DailyReflection as the Evening Loop (1 week)

The `DailyReflection` model (with area scores 1–5) captures the "how did I live this?"
half of the alignment loop. Nothing creates these yet.

### 3A · Evening reflection entry

Currently `JournalEntry` captures free text. `DailyReflection` adds life area self-scores.
Options:
- **Option A (simple):** Add area score sliders to the existing `JournalPage` form
- **Option B (distinct):** Create a dedicated `ReflectionPage` evening mode (already exists as stub)

Recommendation: **Option A first** — add 3–4 life area sliders at the bottom of the journal
form. Store the scores on `DailyReflection`, linked to the `JournalEntry` by date + user.

### 3B · Compute AlignmentTrend via Celery

A Celery beat task already runs weekly/monthly AI crew analysis. Add a companion task
that aggregates the `DailyReflection.area_scores` into `AlignmentTrend` records:

```python
@shared_task
def compute_alignment_trends(user_id):
    # Aggregate last 7 days of area_scores per user
    # Write AlignmentTrend record
    # Compute deltas vs previous week
```

### 3C · Surface trends in ProgressPage

`ProgressPage.tsx` is mostly a stub. Wire it to `GET /api/v1/reflections/trends/`:

```
Faith:          ████████░░  4.1  (+0.3 ↑)
Self-Control:   █████░░░░░  2.8  (-0.2 ↓)
Relationships:  ███████░░░  3.6  (→ stable)
```

---

## Phase 4 — The Weekly Review Loop (3–4 days)

### 4A · Weekly summary card on Dashboard

The AI crew already runs on Sundays and saves output to `AlignmentTrend.ai_summary`.
Surface it:

- After Sunday's crew run, show a dismissible card on the Dashboard:
  > "Here's what the week showed about your focus on Self-Control..."
  > [Read full review]

### 4B · Weekly review prompt

End-of-week: prompt user with one question tied to their focus:
> "This week you focused on **Self-Control**. You journaled 5 times and highlighted
> 8 verses about discipline. What's one thing you're carrying into next week?"

Store as a `JournalEntry` with tag `weekly_review`.

---

## What This Achieves

```
BEFORE:
  Focus ──────────────────────── (isolated)
  Reading Plan ───────────────── (isolated)
  Journal ────────────────────── (isolated)

AFTER:
  UserJourney
    ├── FocusIntention ◄──── informs ──► ReadingPlan insights
    ├── ReadingPlan enrollment
    ├── JournalEntries (tagged with focus)
    │     └── OpenThreads (detected, followed up)
    ├── DailyReflections (area scores)
    │     └── AlignmentTrend (weekly aggregates)
    └── AI Crew output (weekly summary, surfaced in UI)
```

Every feature feeds every other feature. A user's stated goal shapes their reading.
Their reading shapes their journal prompts. Their journal spawns open threads that
follow them. Their scores accumulate into visible growth. The AI crew synthesizes
all of it weekly into something personal and human.

---

## Suggested Build Order

| Week | Work | Payoff |
|------|------|--------|
| 1 | 1A + 1B + 1C | Focus-aware everything, threads visible |
| 2 | 2A + 2B | Journey creation flow, JourneyPage live |
| 3 | 3A + 3B | Evening scores captured, trends computing |
| 4 | 3C + 4A + 4B | ProgressPage live, weekly summary surfaces |

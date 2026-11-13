# Bible study guide, growth profile and growth plans

Three connected features, all built on the journal:

| | What it is | Where |
|---|---|---|
| **Bible study guide** | A library of 48 short studies (about 200 lessons) for every age and circumstance, shown at your level and suggested from what you write. | Study |
| **Growth profile** | An honest, non-clinical picture of your walk with God and how you are doing inside, built from your own answers and activity. | More → My profile |
| **Growth plans** | Pick a characteristic to grow in; get short- and long-term goals, linked studies, weekly check-ins and a progress status. | More → Growth plans |

## The study library

Eight categories: **Peace, Refuge, Strength, Wisdom, Love, Foundations, Character, Seasons of life**. Topics range
from anxiety, grief and loneliness to marriage, parenting, work, money, doubt, prayer, aging and facing death.

Every lesson has the same five parts:

1. **Read** — one short passage (1-12 verses). The words are fetched from the Bible source (World English
   Bible, then KJV; Reina-Valera 1960 in Spanish). Lessons never contain scripture text of their own.
2. **Understand** — what the passage says and why it matters, in plain words.
3. **Reflect** — two or three questions, a place to say what stood out, and two 1-5 ratings: how well you
   understood it, and how much it speaks to where you are.
4. **Practice** — one small, concrete thing to do.
5. **Pray** — a short prayer starter.

### One library, five life stages

| Life stage | What changes |
|---|---|
| Child (6-11) | The simple explanation, a child's question and a child-sized practice. Marked "read this with a grown-up". Adult topics (marriage, addiction, money…) are not offered. |
| Teen | Standard explanation; questions about school, home and friends. |
| Young adult | Questions about decisions, relationships and direction. |
| Adult | Questions about work, home and responsibility. |
| Senior | Questions that look back, and at who needs to hear it from you. |

Each topic also carries a one-line note on how it meets each stage. Set your life stage on the Study page or
in your profile; you can still browse every study.

### How studies adapt to you

- **Suggestions** come from plain rules, not a model, and every suggestion shows its reasons:
  what you said you are looking for · characteristics you chose to grow in · your active growth plans ·
  themes in your recent journal feedback ("your recent entries mention 'work pressure' 3×") · words in recent
  entries · your walks of life · low self-ratings in the look inward · moods you have tagged.
  Code: `backend/apps/guides/recommend.py`.
- **"Explain it more simply"** switches a lesson to the simpler explanation and remembers it.
- **"Make it personal"** asks your AI provider to explain the passage for someone in your situation and to
  write three questions that connect it to your life. It is given the lesson's meaning (which it must keep),
  your life stage, walks of life, faith background, chosen characteristics, recent journal themes and
  anything you wrote in "about me". The standard lesson stays available beside it.
- **A reply to what you wrote.** When you save your answers, the app responds to them and may ask one
  deeper question. If AI is unavailable you get a built-in reply that says so and why.
- **Journal feedback** now also knows your life stage and the characteristics you are working on.

## The growth profile

Two layers, kept deliberately separate:

**1. The snapshot — arithmetic only, always available.**
Your answers to the "look inward" (14 statements rated 1-5: six about your walk with God, eight about how
you are doing inside), your self-ratings on characteristics, counts of studies and lessons, the themes and
moods from your journal, and the averages of your lesson ratings. Retaking the look inward keeps the earlier
one, so you can see change over time.

**2. "What the app notices" — written by AI, only when you ask.**
A short reflection with four to six observations. The rules it is held to:

- Every observation must list **what it is based on**. One with no evidence is discarded.
- **No diagnosis.** Clinical terms and personality labels are forbidden in the prompt, and any observation
  containing them is discarded by the code.
- Strengths at least as often as struggles; tentative language; nothing about causes in your past.
- You can mark any observation **"That's not me"** — it will not be repeated — and write corrections in
  "about me", which the AI is told to trust above the data.

**This is self-reflection, not assessment.** It is not a psychological evaluation, a diagnosis, or a
judgment of anyone's faith, and it can be wrong.

### Care and limits

- **When someone seems to be carrying a lot** (most recent entries tagged "struggling", or very low
  inner-life ratings) the profile shows a gentle note encouraging them to tell someone they trust.
  If recent writing contains language about self-harm, the note is direct: contact emergency services or a
  crisis line now (988 in the United States) and tell someone.
- **Sensitive studies** (despair, addiction, grief, illness, suffering, facing death) carry the same kind of
  note on every lesson, and at least one practice in each points to a pastor, doctor or counselor.
- **Children:** for the "child" life stage the app builds **no** profile — no look inward, no inner-life
  section, no AI observations — and a child's lesson answers are **never sent to a model**. Age is used only
  to choose gentler lessons. Switching a profile to "child" deletes any assessment and observations already
  stored.
- **Erase** removes the profile, every assessment and all observations. Studies, plans and journal entries
  are kept (delete those individually, or delete the account).

## Growth plans

Choose one of 24 characteristics (the fruit of the Spirit and others: humility, courage, wisdom, forgiveness,
gratitude, honesty, generosity, contentment, perseverance, compassion, hope, trust, purity, servanthood,
prayerfulness). A plan runs 90 days and contains:

- the characteristic's definition, key passages, and where Jesus showed it;
- **short-term goals** (7-14 days) and **long-term goals** (30-90 days) — small, countable practices;
- the studies that build it, to start from the plan;
- a **weekly check-in**: a 1-5 self-rating, one question, an optional note.

Goals come from the catalog, or — if you tick "tailor the goals to me" — your AI rewrites the practice goals
for your situation (falling back to the catalog, with the reason shown, if AI is unavailable). You can add,
edit, skip or remove goals.

### Progress status

| Shown | How it is worked out |
|---|---|
| Goal progress | Times done ÷ target. **Study goals count themselves** from lessons you complete in the linked studies after the plan began. |
| Percent | 40% short-term goals + 60% long-term goals (skipped goals are left out). |
| Stage | Getting started (<15%) · Building the habit (<50%) · Steady (<85%) · Well established. |
| Rating change | Your latest check-in rating compared with where you started. |
| Check-in due | Seven days since the last check-in (or since the plan began). |

Goals count faithful attempts, never perfection, and nothing is scored in a way meant to produce shame.

## Privacy

- Everything you write here, and everything the app writes about you — about me, assessment answers,
  observations, lesson answers and replies, personalised explanations, the "why" of a plan, goal titles,
  check-in notes — is **encrypted at rest** with your key, like journal entries.
- Stored unencrypted, because the app must query them: which studies you started, life stage, walks of life,
  chosen topics and characteristics, dates, counts and 1-5 ratings.
- AI is used only for: "Make it personal", the reply to your answers, "What the app notices", and tailored
  goals. All four go through the same gate as every other AI feature (`backend/shared/llm.py`): your own
  provider, or the server's — and a server-configured cloud AI only if you turned on consent. On a
  local-only server nothing leaves the network.
- All of it is included in **Settings → Export My Data** as `study-and-growth.json`.

## For developers

| Path | Purpose |
|---|---|
| `backend/apps/guides/content/*.py` | The library: topics, lessons, traits. Bilingual. References only. |
| `backend/apps/guides/catalog.py` | Life stages, walks of life, categories, trait and topic keys, assessment items. |
| `backend/apps/guides/library.py` | Loader and validator. `python -m apps.guides.library` reports every problem. |
| `backend/apps/guides/signals.py` | The single place that gathers what the app can see about a person. |
| `backend/apps/guides/recommend.py` | Suggestion rules and their reasons. |
| `backend/apps/guides/profile.py` | Snapshot, insights, support notes. |
| `backend/apps/guides/study.py` | Lessons, answers, replies, personalisation. |
| `backend/apps/guides/plans.py` | Plans, goals, check-ins, progress. |

**Adding or editing content:** edit a module in `content/`, then run the tests. `TestRealLibrary` fails if a
topic is missing, a field is malformed, a reference does not exist (checked against verse counts with
`pythonbible`), a lesson quotes scripture at length, or a sensitive topic has no practice pointing to real
help. The validator cannot judge whether a passage *means* what a lesson says — that needs a human reader.

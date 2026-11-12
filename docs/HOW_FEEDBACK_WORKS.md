# How feedback and scripture selection work

What happens when you save a journal entry and ask for feedback.

```
your entry ─► AI reads it (plus a little context) and returns:
                 themes · a reflection · 3 passage *references*, each with a reason
            ─► the app looks each reference up in the Bible source, in order
                 not a real reference?  recorded as "invalid" / "not found", skipped
                 first one that exists  ─► its text is fetched and shown
            ─► the whole decision is saved as an audit record
```

## Rules the code holds to

1. **The AI never writes scripture.** It suggests references only. The words
   shown come from the Bible source — the local database when a translation has
   been loaded, otherwise the Bolls API. If a reference does not exist there, it
   is not shown. (`backend/apps/bible/lookup.py`)
2. **Translations are public domain.** World English Bible (modern English)
   first, King James Version as fallback; Reina-Valera 1960 first for Spanish.
   Configurable with `SCRIPTURE_TRANSLATIONS`.
3. **Not every entry is spiritual, and that is fine.** The prompt tells the
   model to respond to what was actually written — work, family, tiredness —
   and to connect it to the character of Jesus without preaching.
4. **No pretending.** The AI is told never to claim experiences of its own.
   When the AI cannot be used, you still get a passage, chosen by plain keyword
   rules, and the screen says so and says why.
5. **Your text stays where you allow it.** One code path (`backend/shared/llm.py`)
   decides which AI handles a request: your own provider if you set one, else
   the server's. A server-configured cloud AI is used only if you switched on
   consent in Settings. With `AI_LOCAL_ONLY` cloud providers are refused outright.

## What the AI is given

| Input | When |
|---|---|
| The entry text (first 4,000 characters) | always |
| The mood you tagged | if set |
| Your current focus | if you have an active one |
| Themes from your last 8 entries with feedback | if any |
| Things you are working through (open threads) | if any |
| The last 5 passages you were given | if any — so it prefers something new |

Nothing else: not your name, email, or other entries' text.

## The audit record ("Why this scripture?")

Open it under any feedback, or see all of them at **Audit log** (`/audit`).
Each record holds:

- where the AI ran — provider, model, on your network or in the cloud;
- which inputs were used;
- every passage that was suggested, the reason given, and what happened to it
  (selected · not found in the Bible · invalid reference · not used);
- the rule that picked the winner;
- how long it took, and the prompt version;
- if the AI was not used: the error code and what to do about it.

Regenerating feedback keeps the earlier record, so the log shows every
decision ever made. Everything derived from your entry (themes, reflection,
reasons) is encrypted at rest with your key, like the entry itself. It is
included in **Settings → Export My Data** as `journal-feedback.json`.

## Growth over time

- **Themes** recur across entries and are fed back into the next prompt, so
  feedback can say "this is the third time this month…".
- **Threads**: if an entry mentions a struggle, commitment or decision worth
  asking about again, a thread is opened and you get a gentle check-in a few
  days later (Threads page; at most two at a time).
- **Reviews**: every Sunday evening (and on the 1st of the month) a short
  look-back is generated from that period's entries and saved to
  **Progress → Reviews**. You can also generate one on demand.

"""
Which studies to suggest to a person, and why.

Plain, inspectable rules - no model involved. Every point a topic earns
comes with a sentence the person can read, so a suggestion is never a
mystery.
"""

import re

from . import library
from .catalog import ASSESSMENT_ITEMS, SITUATIONS, L
from .render import tr
from .signals import Signals

# A low self-rating on an assessment item points toward these studies.
ASSESSMENT_TOPICS = {
    "prayer": ["prayer"],
    "scripture": ["scripture"],
    "community": ["friendship", "loneliness"],
    "serving": ["service"],
    "sabbath": ["rest"],
    "confession": ["grace", "forgiveness"],
    "calm": ["anxiety", "refuge"],
    "hopeful": ["hope"],
    "self_kind": ["identity", "grace"],
    "connected": ["loneliness", "friendship"],
    "purpose": ["work", "identity"],
    "release": ["waiting", "anxiety"],
    "rested": ["rest"],
    "honest_feelings": ["prayer", "suffering"],
}
MOOD_TOPICS = {
    "struggling": (
        ["refuge", "rest", "suffering"],
        L(
            "You have tagged several recent entries as struggling.",
            "Has marcado varias entradas recientes como de lucha.",
        ),
    ),
    "grateful": (
        ["gratitude", "joy"],
        L(
            "You have tagged several recent entries as grateful.",
            "Has marcado varias entradas recientes con gratitud.",
        ),
    ),
    "convicted": (
        ["grace", "forgiveness"],
        L(
            "You have tagged several recent entries as convicted.",
            "Has marcado varias entradas recientes con convicción.",
        ),
    ),
}
STARTERS = ["who_god_is", "jesus", "prayer", "anxiety", "identity", "gratitude"]

R = {
    "need": L(
        "You said you are looking for help with this.",
        "Dijiste que buscas ayuda con esto.",
    ),
    "trait": L(
        "It builds {trait}, which you chose to grow in.",
        "Desarrolla {trait}, algo en lo que elegiste crecer.",
    ),
    "plan": L(
        "It is part of your growth plan for {trait}.",
        "Es parte de tu plan de crecimiento en {trait}.",
    ),
    "theme": L(
        "Your recent entries mention “{theme}” ({count}×).",
        "Tus entradas recientes mencionan «{theme}» ({count}×).",
    ),
    "words": L(
        "A recent entry uses words like “{word}”.",
        "Una entrada reciente usa palabras como «{word}».",
    ),
    "words_many": L(
        "{count} of your recent entries use words like “{word}”.",
        "{count} de tus entradas recientes usan palabras como «{word}».",
    ),
    "situation": L(
        "It is written with this in mind: {situation}.",
        "Está pensado para esto: {situation}.",
    ),
    "assessment": L(
        "In your look inward you rated this low: “{item}”",
        "En tu mirada interior calificaste bajo esto: «{item}»",
    ),
    "foundation": L("A good place to begin.", "Un buen lugar para comenzar."),
    "starter": L(
        "A good first study while the app gets to know you.",
        "Un buen primer estudio mientras la app te conoce.",
    ),
}


def _matches(keyword: str, text: str) -> bool:
    """Single-word keywords match as word prefixes; phrases match as substrings."""
    if " " in keyword:
        return keyword in text
    return re.search(rf"(?<![a-záéíóúñ]){re.escape(keyword)}", text) is not None


def recommend(signals: Signals, lang: str, limit: int = 6) -> list:
    profile = signals.profile
    stage = signals.life_stage
    situation_titles = {s["key"]: tr(s["title"], lang) for s in SITUATIONS}
    item_text = {i["key"]: tr(i["text"], lang) for i in ASSESSMENT_ITEMS}
    answers = (signals.assessment or {}).get("answers", {})
    plan_topics = {}
    for plan in signals.plans:
        trait = library.get_trait(plan.trait_key)
        if trait:
            for key in trait["topics"]:
                plan_topics.setdefault(key, tr(trait["title"], lang))
    done_or_doing = signals.completed_topics | signals.active_topics

    results = []
    for key, topic in library.topics().items():
        if key in done_or_doing:
            continue
        if stage and stage not in topic["stages"]:
            continue
        if not stage and topic["stages"] == ["child"]:
            continue

        score, reasons = 0, []

        if profile and key in (profile.needs or []):
            score += 50
            reasons.append(tr(R["need"], lang))
        if key in plan_topics:
            score += 35
            reasons.append(tr(R["plan"], lang).format(trait=plan_topics[key]))
        if profile:
            for trait_key in profile.desired_traits or []:
                if trait_key in topic["traits"]:
                    trait = library.get_trait(trait_key)
                    score += 30
                    reasons.append(
                        tr(R["trait"], lang).format(
                            trait=(
                                tr(trait["title"], lang).lower() if trait else trait_key
                            )
                        )
                    )
                    break

        theme_hits = [
            (theme, count)
            for theme, count in signals.themes.most_common()
            if any(_matches(k, theme) for k in topic["keywords"])
        ]
        for theme, count in theme_hits[:2]:
            score += min(40, 12 * count)
            reasons.append(tr(R["theme"], lang).format(theme=theme, count=count))

        # The person's own words: how many recent entries use this topic's vocabulary.
        word, mentions = None, 0
        for text in signals.entry_texts:
            for keyword in topic["keywords"]:
                found = re.search(
                    rf"(?<![a-záéíóúñ]){re.escape(keyword)}[a-záéíóúñ]*", text
                )
                if found:
                    word = word or found.group(0)
                    mentions += 1
                    break
        if mentions:
            score += 14 + 6 * min(mentions - 1, 3)
            reasons.append(
                tr(R["words_many" if mentions > 1 else "words"], lang).format(
                    word=word, count=mentions
                )
            )

        if profile:
            shared = [s for s in (profile.situations or []) if s in topic["situations"]]
            for situation in shared[:2]:
                score += 10
                reasons.append(
                    tr(R["situation"], lang).format(
                        situation=situation_titles[situation].lower()
                    )
                )
            if topic["category"] == "foundations" and profile.faith_background in (
                "exploring",
                "new",
                "returning",
            ):
                score += 15
                reasons.append(tr(R["foundation"], lang))

        for item_key, topic_keys in ASSESSMENT_TOPICS.items():
            if (
                key in topic_keys
                and isinstance(answers.get(item_key), int)
                and answers[item_key] <= 2
            ):
                score += 20
                reasons.append(
                    tr(R["assessment"], lang).format(item=item_text[item_key])
                )
                break

        for mood, (topic_keys, reason) in MOOD_TOPICS.items():
            if key in topic_keys and signals.moods.get(mood, 0) >= 3:
                score += 10
                reasons.append(tr(reason, lang))

        if score > 0:
            results.append({"key": key, "score": score, "reasons": reasons[:3]})

    results.sort(key=lambda r: -r["score"])
    # Never leave someone with one lonely suggestion: fill up with good first studies.
    if len(results) < 3:
        chosen = {r["key"] for r in results}
        for key in STARTERS:
            topic = library.get_topic(key)
            if not topic or key in done_or_doing or key in chosen:
                continue
            if stage and stage not in topic["stages"]:
                continue
            results.append(
                {"key": key, "score": 1, "reasons": [tr(R["starter"], lang)]}
            )
            if len(results) >= 4:
                break
    return results[:limit]

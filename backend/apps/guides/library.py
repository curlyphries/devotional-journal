"""
Load and validate the study library (apps/guides/content).

    python -m apps.guides.library            # validate everything, print a report
    python -m apps.guides.library peace_refuge  # validate one content module

Validation needs `pythonbible` (a dev dependency) to confirm that every cited
chapter and verse exists. At runtime the library loads without it.
"""

import importlib
import re
import sys
from functools import lru_cache

from apps.bible.books import parse_reference

from .catalog import (
    ALL_TOPIC_KEYS,
    CATEGORY_KEYS,
    LANGS,
    LIFE_STAGE_KEYS,
    SITUATION_KEYS,
    TOPIC_KEYS,
    TRAIT_KEYS,
)

CONTENT_MODULES = [
    "peace_refuge",
    "strength_wisdom",
    "love_seasons",
    "foundations_character",
]
MAX_VERSES = 12
MIN_LESSONS = 4
LESSON_TEXT_FIELDS = (
    "title",
    "truth",
    "simple",
    "ask",
    "kid_ask",
    "do",
    "kid_do",
    "pray",
)
GOAL_KINDS = ("practice", "study", "reflection", "prayer")


def _bilingual(value, where, errors, max_len=700, min_len=3):
    if not isinstance(value, dict) or set(value) != set(LANGS):
        errors.append(f"{where}: must be {{'en': ..., 'es': ...}}")
        return
    for lang in LANGS:
        text = value[lang]
        if not isinstance(text, str) or not (min_len <= len(text.strip()) <= max_len):
            errors.append(
                f"{where}.{lang}: must be text of {min_len}-{max_len} characters"
            )


def check_reference(ref, where, errors, max_verses=MAX_VERSES):
    """A reference must parse, exist, and fit in one short reading."""
    parsed = parse_reference(ref) if isinstance(ref, str) else None
    if not parsed:
        errors.append(f"{where}: '{ref}' is not a recognisable reference")
        return
    if parsed.verse_start is None:
        errors.append(f"{where}: '{ref}' needs verses (e.g. 'Psalm 23:1-6')")
        return
    span = parsed.verse_end - parsed.verse_start + 1
    if span > max_verses:
        errors.append(
            f"{where}: '{ref}' is {span} verses; keep it to {max_verses} or fewer"
        )
    try:
        import pythonbible as pb
    except ImportError:  # runtime without the dev dependency: format check only
        return
    book = pb.Book(parsed.book.number)
    if parsed.chapter > pb.get_number_of_chapters(book):
        errors.append(
            f"{where}: '{ref}' - {parsed.book.name} has no chapter {parsed.chapter}"
        )
        return
    last = pb.get_number_of_verses(book, parsed.chapter)
    if parsed.verse_end > last:
        errors.append(
            f"{where}: '{ref}' - {parsed.book.name} {parsed.chapter} ends at verse {last}"
        )


def validate_topic(topic, errors):
    key = topic.get("key")
    where = f"topic '{key}'"
    if not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z_]*", key):
        errors.append(f"{where}: key must be lowercase letters/underscores")
        return
    if topic.get("category") not in CATEGORY_KEYS:
        errors.append(f"{where}: unknown category {topic.get('category')!r}")
    elif key not in TOPIC_KEYS[topic["category"]]:
        errors.append(
            f"{where}: is not listed under category '{topic['category']}' in catalog.TOPIC_KEYS"
        )
    _bilingual(topic.get("title"), f"{where}.title", errors, max_len=60)
    _bilingual(
        topic.get("summary"), f"{where}.summary", errors, max_len=260, min_len=20
    )

    keywords = topic.get("keywords")
    if (
        not isinstance(keywords, list)
        or len(keywords) < 6
        or any(
            not isinstance(k, str) or k != k.lower().strip() or len(k) < 3
            for k in keywords
        )
    ):
        errors.append(
            f"{where}.keywords: at least 6 lowercase words/stems (English and Spanish)"
        )

    for field, allowed in (
        ("situations", SITUATION_KEYS),
        ("traits", TRAIT_KEYS),
        ("stages", LIFE_STAGE_KEYS),
    ):
        values = topic.get(field)
        if not isinstance(values, list) or any(v not in allowed for v in values):
            errors.append(f"{where}.{field}: must be a list drawn from the catalog")
    stages = topic.get("stages") or []
    if not stages:
        errors.append(f"{where}.stages: list at least one life stage")
    if not topic.get("traits"):
        errors.append(f"{where}.traits: list at least one trait this study builds")
    notes = topic.get("stage_notes")
    if not isinstance(notes, dict) or set(notes) != set(stages):
        errors.append(
            f"{where}.stage_notes: one note for each stage in 'stages' (and no others)"
        )
    else:
        for stage, note in notes.items():
            _bilingual(
                note, f"{where}.stage_notes.{stage}", errors, max_len=260, min_len=20
            )
    if not isinstance(topic.get("sensitive"), bool):
        errors.append(f"{where}.sensitive: must be True or False")

    lessons = topic.get("lessons")
    if not isinstance(lessons, list) or len(lessons) < MIN_LESSONS:
        errors.append(f"{where}.lessons: at least {MIN_LESSONS} lessons")
        return
    seen_refs = set()
    for index, lesson in enumerate(lessons, start=1):
        lwhere = f"{where} lesson {index}"
        if lesson.get("key") != f"{key}-{index}":
            errors.append(f"{lwhere}: key must be '{key}-{index}'")
        check_reference(lesson.get("ref"), f"{lwhere}.ref", errors)
        if lesson.get("ref") in seen_refs:
            errors.append(
                f"{lwhere}.ref: '{lesson.get('ref')}' is used twice in this topic"
            )
        seen_refs.add(lesson.get("ref"))
        for field in LESSON_TEXT_FIELDS:
            limit = 80 if field == "title" else 700
            _bilingual(lesson.get(field), f"{lwhere}.{field}", errors, max_len=limit)
        extra = set(lesson) - {"key", "ref", *LESSON_TEXT_FIELDS}
        if extra:
            errors.append(f"{lwhere}: unexpected fields {sorted(extra)}")


def validate_trait(trait, errors, topic_keys=ALL_TOPIC_KEYS):
    key = trait.get("key")
    where = f"trait '{key}'"
    if key not in TRAIT_KEYS:
        errors.append(f"{where}: not in catalog.TRAIT_KEYS")
        return
    _bilingual(trait.get("title"), f"{where}.title", errors, max_len=40)
    _bilingual(
        trait.get("definition"), f"{where}.definition", errors, max_len=400, min_len=30
    )
    _bilingual(
        trait.get("check_in_question"),
        f"{where}.check_in_question",
        errors,
        max_len=200,
        min_len=10,
    )
    refs = trait.get("refs")
    if not isinstance(refs, list) or not (2 <= len(refs) <= 4):
        errors.append(f"{where}.refs: 2 to 4 references")
    else:
        for ref in refs:
            check_reference(ref, f"{where}.refs", errors)
    jesus = trait.get("jesus")
    if not isinstance(jesus, dict):
        errors.append(f"{where}.jesus: {{'ref': ..., 'note': {{en, es}}}}")
    else:
        check_reference(jesus.get("ref"), f"{where}.jesus.ref", errors)
        _bilingual(
            jesus.get("note"), f"{where}.jesus.note", errors, max_len=300, min_len=20
        )
    topics = trait.get("topics")
    if (
        not isinstance(topics, list)
        or not topics
        or any(t not in topic_keys for t in topics)
    ):
        errors.append(
            f"{where}.topics: 1-3 study topic keys from catalog.ALL_TOPIC_KEYS"
        )
    for field, days_allowed, count in (
        ("short_goals", (7, 14), 3),
        ("long_goals", (30, 60, 90), 3),
    ):
        goals = trait.get(field)
        if not isinstance(goals, list) or len(goals) != count:
            errors.append(f"{where}.{field}: exactly {count} goals")
            continue
        for i, goal in enumerate(goals, start=1):
            gwhere = f"{where}.{field}[{i}]"
            _bilingual(
                goal.get("title"), f"{gwhere}.title", errors, max_len=180, min_len=10
            )
            if goal.get("kind") not in GOAL_KINDS:
                errors.append(f"{gwhere}.kind: one of {GOAL_KINDS}")
            if not isinstance(goal.get("target_count"), int) or not (
                1 <= goal["target_count"] <= 90
            ):
                errors.append(f"{gwhere}.target_count: whole number 1-90")
            if goal.get("days") not in days_allowed:
                errors.append(f"{gwhere}.days: one of {days_allowed}")


def _load_module(name):
    return importlib.import_module(f"apps.guides.content.{name}")


def validate_module(name) -> list:
    errors = []
    module = _load_module(name)
    if name == "traits":
        for trait in module.TRAITS:
            validate_trait(trait, errors)
    else:
        for topic in module.TOPICS:
            validate_topic(topic, errors)
    return errors


def validate_library() -> list:
    """Every problem in the whole library, as readable strings (empty = good)."""
    errors = []
    seen = []
    for name in CONTENT_MODULES:
        try:
            module = _load_module(name)
        except Exception as exc:  # noqa: BLE001 - report, do not crash the report
            errors.append(f"content/{name}.py could not be loaded: {exc}")
            continue
        for topic in module.TOPICS:
            validate_topic(topic, errors)
            seen.append(topic.get("key"))
    missing = sorted(set(ALL_TOPIC_KEYS) - set(seen))
    duplicate = sorted({k for k in seen if seen.count(k) > 1})
    if missing:
        errors.append(f"topics missing from the library: {missing}")
    if duplicate:
        errors.append(f"topics defined more than once: {duplicate}")
    try:
        traits = _load_module("traits").TRAITS
    except Exception as exc:  # noqa: BLE001
        errors.append(f"content/traits.py could not be loaded: {exc}")
        return errors
    for trait in traits:
        validate_trait(trait, errors)
    trait_keys = [t.get("key") for t in traits]
    if sorted(trait_keys) != sorted(TRAIT_KEYS):
        errors.append(
            "content/traits.py must define each key in catalog.TRAIT_KEYS exactly once"
        )
    return errors


# --------------------------------------------------------------------------
# Runtime access
# --------------------------------------------------------------------------


@lru_cache(maxsize=1)
def topics() -> dict:
    """All topics by key, in catalog order."""
    loaded = {}
    for name in CONTENT_MODULES:
        for topic in _load_module(name).TOPICS:
            loaded[topic["key"]] = topic
    return {key: loaded[key] for key in ALL_TOPIC_KEYS if key in loaded}


@lru_cache(maxsize=1)
def traits() -> dict:
    loaded = {t["key"]: t for t in _load_module("traits").TRAITS}
    return {key: loaded[key] for key in TRAIT_KEYS if key in loaded}


def get_topic(key):
    return topics().get(key)


def get_trait(key):
    return traits().get(key)


if __name__ == "__main__":
    names = sys.argv[1:]
    problems = []
    if names:
        for module_name in names:
            problems += validate_module(module_name)
    else:
        problems = validate_library()
    for problem in problems:
        print("ERROR", problem)
    print(f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)

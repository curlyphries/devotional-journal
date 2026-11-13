"""
Turn library content into what one person sees: the right language, and the
right level for their stage of life.
"""

from apps.bible.lookup import fetch_reference, preferred_translations
from shared.errors import SUGGESTIONS

from . import library
from .catalog import LIFE_STAGE_KEYS, L


def lang_for(request) -> str:
    """?lang=en|es wins; otherwise the person's saved language."""
    requested = (request.query_params.get("lang") or "").lower()
    if requested in ("en", "es"):
        return requested
    return "es" if getattr(request.user, "language_preference", "en") == "es" else "en"


def tr(value, lang: str) -> str:
    if isinstance(value, dict):
        return value.get(lang) or value.get("en") or ""
    return value or ""


def stage_or_default(stage: str) -> str:
    return stage if stage in LIFE_STAGE_KEYS else "adult"


ABOUT_GOD = L(
    "What does this passage show you about God?",
    "¿Qué te muestra este pasaje acerca de Dios?",
)
KID_ABOUT_GOD = L(
    "What does this tell you about God?", "¿Qué te dice esto acerca de Dios?"
)
STAGE_QUESTION = {
    "teen": L(
        "Where does this show up at school, at home or with your friends this week?",
        "¿Dónde aparece esto en la escuela, en casa o con tus amigos esta semana?",
    ),
    "young_adult": L(
        "Which decision or relationship in front of you right now does this speak to?",
        "¿A qué decisión o relación que tienes delante ahora le habla esto?",
    ),
    "adult": L(
        "Where in your work, your home or your responsibilities does this press on you right now?",
        "¿Dónde, en tu trabajo, tu hogar o tus responsabilidades, te toca esto ahora mismo?",
    ),
    "senior": L(
        "Looking back over the years, where have you seen this to be true, and who needs to hear it from you?",
        "Mirando los años vividos, ¿dónde has visto que esto es verdad, y quién necesita oírlo de ti?",
    ),
}
SUPPORT_NOTE = L(
    "This is a heavy subject. You do not have to carry it alone: tell someone you trust how you are "
    "really doing, and if it is more than you can manage, a pastor, doctor or counselor can help. "
    "If you are in danger or thinking about harming yourself, contact emergency services or a crisis "
    "line now (in the United States, call or text 988).",
    "Este es un tema pesado. No tienes que cargarlo a solas: cuéntale a alguien de confianza cómo "
    "estás de verdad y, si es más de lo que puedes manejar, un pastor, médico o consejero puede "
    "ayudarte. Si estás en peligro o piensas en hacerte daño, comunícate ahora con los servicios de "
    "emergencia o una línea de crisis (en Estados Unidos, llama o escribe al 988).",
)


def topic_card(topic: dict, lang: str, stage: str = "", enrollment=None) -> dict:
    note = topic["stage_notes"].get(stage) if stage else None
    return {
        "key": topic["key"],
        "category": topic["category"],
        "title": tr(topic["title"], lang),
        "summary": tr(topic["summary"], lang),
        "lesson_count": len(topic["lessons"]),
        "stages": topic["stages"],
        "traits": topic["traits"],
        "sensitive": topic["sensitive"],
        "stage_note": tr(note, lang) if note else None,
        "enrollment": enrollment,
    }


def enrollment_brief(enrollment, completed_numbers) -> dict:
    return {
        "id": str(enrollment.id),
        "status": enrollment.status,
        "current_lesson": enrollment.current_lesson,
        "completed_lessons": sorted(completed_numbers),
    }


def lesson_questions(lesson: dict, stage: str, lang: str) -> list:
    if stage == "child":
        return [tr(lesson["kid_ask"], lang), tr(KID_ABOUT_GOD, lang)]
    return [
        tr(lesson["ask"], lang),
        tr(ABOUT_GOD, lang),
        tr(STAGE_QUESTION[stage], lang),
    ]


def render_lesson(
    topic: dict, number: int, stage: str, lang: str, level: str = "standard"
) -> dict:
    """The static (non-personal) parts of a lesson, with the passage fetched."""
    lesson = topic["lessons"][number - 1]
    stage = stage_or_default(stage)
    simple = stage == "child" or level == "simple"

    passage = fetch_reference(lesson["ref"], preferred_translations(lang))
    passage_error = None
    if passage is None:
        passage_error = {
            "code": "SCRIPTURE_UNAVAILABLE",
            "message": {
                "en": "The Bible text could not be loaded just now.",
                "es": "No se pudo cargar el texto bíblico en este momento.",
            }[lang],
            "suggestion": SUGGESTIONS["SCRIPTURE_UNAVAILABLE"],
        }

    count = len(topic["lessons"])
    return {
        "number": number,
        "lesson_count": count,
        "title": tr(lesson["title"], lang),
        "topic": {"key": topic["key"], "title": tr(topic["title"], lang)},
        "reference": passage.reference if passage else lesson["ref"],
        "passage": passage.to_dict() if passage else None,
        "passage_error": passage_error,
        "explanation": tr(lesson["simple"] if simple else lesson["truth"], lang),
        "explanation_level": "simple" if simple else "standard",
        "questions": lesson_questions(lesson, stage, lang),
        "practice": tr(lesson["kid_do"] if stage == "child" else lesson["do"], lang),
        "prayer": tr(lesson["pray"], lang),
        "with_grown_up": stage == "child",
        "support_note": (
            tr(SUPPORT_NOTE, lang) if topic["sensitive"] and stage != "child" else None
        ),
        "previous": {"number": number - 1} if number > 1 else None,
        "next": {"number": number + 1} if number < count else None,
    }


def trait_brief(key: str, lang: str):
    trait = library.get_trait(key)
    if not trait:
        return None
    return {
        "key": key,
        "title": tr(trait["title"], lang),
        "definition": tr(trait["definition"], lang),
    }

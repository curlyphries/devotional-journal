"""
Fixed vocabularies for the study guides: who a study is for, what it is
about, and the questions of the self-assessment.

Everything shown to a person is bilingual: {"en": ..., "es": ...}.
"""

LANGS = ("en", "es")


def L(en: str, es: str) -> dict:
    return {"en": en, "es": es}


# Order matters: it is the order shown in the UI.
LIFE_STAGES = [
    {
        "key": "child",
        "title": L(
            "Child (6-11), with a grown-up", "Niño o niña (6-11), con un adulto"
        ),
        "note": L(
            "Short, concrete lessons meant to be read together with a parent or guardian.",
            "Lecciones cortas y concretas para leer junto con un padre, madre o tutor.",
        ),
    },
    {
        "key": "teen",
        "title": L("Teen (12-17)", "Adolescente (12-17)"),
        "note": L(
            "Honest about pressure, identity and questions.",
            "Honesto sobre la presión, la identidad y las preguntas.",
        ),
    },
    {
        "key": "young_adult",
        "title": L("Young adult (18-29)", "Joven adulto (18-29)"),
        "note": L(
            "For years of big decisions: calling, relationships, direction.",
            "Para años de grandes decisiones: vocación, relaciones, rumbo.",
        ),
    },
    {
        "key": "adult",
        "title": L("Adult (30-59)", "Adulto (30-59)"),
        "note": L(
            "For full lives: work, family, responsibility, weariness.",
            "Para vidas llenas: trabajo, familia, responsabilidad, cansancio.",
        ),
    },
    {
        "key": "senior",
        "title": L("Senior (60+)", "Adulto mayor (60+)"),
        "note": L(
            "For a season of looking back, letting go and leaving a legacy.",
            "Para una etapa de mirar atrás, soltar y dejar un legado.",
        ),
    },
]
LIFE_STAGE_KEYS = [s["key"] for s in LIFE_STAGES]

SITUATIONS = [
    {"key": "student", "title": L("Student", "Estudiante")},
    {"key": "single", "title": L("Single", "Soltero o soltera")},
    {"key": "dating", "title": L("Dating or engaged", "En noviazgo o comprometido")},
    {"key": "married", "title": L("Married", "Casado o casada")},
    {"key": "parent", "title": L("Parent", "Padre o madre")},
    {"key": "single_parent", "title": L("Single parent", "Padre o madre soltera")},
    {"key": "grandparent", "title": L("Grandparent", "Abuelo o abuela")},
    {"key": "caregiver", "title": L("Caring for someone", "Cuidando a alguien")},
    {"key": "working", "title": L("Working", "Trabajando")},
    {
        "key": "job_seeking",
        "title": L("Out of work or changing jobs", "Sin trabajo o cambiando de empleo"),
    },
    {"key": "retired", "title": L("Retired", "Jubilado o jubilada")},
    {
        "key": "leader",
        "title": L("Leading or serving others", "Liderando o sirviendo a otros"),
    },
    {"key": "new_believer", "title": L("New to the faith", "Nuevo en la fe")},
    {"key": "exploring", "title": L("Exploring or doubting", "Explorando o con dudas")},
    {"key": "returning", "title": L("Coming back to faith", "Regresando a la fe")},
    {"key": "grieving", "title": L("Grieving", "En duelo")},
    {
        "key": "ill",
        "title": L("Living with illness or pain", "Viviendo con enfermedad o dolor"),
    },
    {"key": "recovery", "title": L("In recovery", "En recuperación")},
    {"key": "divorced", "title": L("Separated or divorced", "Separado o divorciado")},
    {"key": "widowed", "title": L("Widowed", "Viudo o viuda")},
    {
        "key": "military",
        "title": L("Military or first responder", "Militar o servicio de emergencias"),
    },
    {"key": "moving", "title": L("In a big transition", "En una gran transición")},
]
SITUATION_KEYS = [s["key"] for s in SITUATIONS]

CATEGORIES = [
    {
        "key": "peace",
        "title": L("Peace", "Paz"),
        "summary": L("When your mind will not rest.", "Cuando tu mente no descansa."),
    },
    {
        "key": "refuge",
        "title": L("Refuge", "Refugio"),
        "summary": L(
            "When life hurts and you need somewhere safe.",
            "Cuando la vida duele y necesitas un lugar seguro.",
        ),
    },
    {
        "key": "strength",
        "title": L("Strength", "Fortaleza"),
        "summary": L(
            "When you need to stand, resist or keep going.",
            "Cuando necesitas mantenerte firme, resistir o seguir.",
        ),
    },
    {
        "key": "wisdom",
        "title": L("Wisdom", "Sabiduría"),
        "summary": L("When you need to choose well.", "Cuando necesitas elegir bien."),
    },
    {
        "key": "love",
        "title": L("Love", "Amor"),
        "summary": L(
            "Loving God and the people in your life.",
            "Amar a Dios y a las personas de tu vida.",
        ),
    },
    {
        "key": "foundations",
        "title": L("Foundations", "Fundamentos"),
        "summary": L(
            "What Christians believe and why it matters.",
            "Lo que creen los cristianos y por qué importa.",
        ),
    },
    {
        "key": "character",
        "title": L("Character", "Carácter"),
        "summary": L("Becoming more like Jesus.", "Llegar a ser más como Jesús."),
    },
    {
        "key": "seasons",
        "title": L("Seasons of life", "Etapas de la vida"),
        "summary": L(
            "Scripture for where you are right now.",
            "La Escritura para donde estás ahora.",
        ),
    },
]
CATEGORY_KEYS = [c["key"] for c in CATEGORIES]

# Characteristics a person can choose to grow in (growth plans, self-rating).
TRAIT_KEYS = [
    "love",
    "joy",
    "peace",
    "patience",
    "kindness",
    "goodness",
    "faithfulness",
    "gentleness",
    "self_control",
    "humility",
    "courage",
    "wisdom",
    "forgiveness",
    "gratitude",
    "honesty",
    "generosity",
    "contentment",
    "perseverance",
    "compassion",
    "hope",
    "trust",
    "purity",
    "servanthood",
    "prayerfulness",
]

# Every study topic in the library, by category. content/*.py must provide
# exactly these keys (library.validate_library checks it).
TOPIC_KEYS = {
    "peace": ["anxiety", "fear", "rest", "contentment", "gratitude", "waiting"],
    "refuge": ["refuge", "suffering", "grief", "loneliness", "illness", "despair"],
    "strength": [
        "perseverance",
        "courage",
        "temptation",
        "addiction",
        "self_control",
        "anger",
    ],
    "wisdom": ["decisions", "work", "money", "words", "priorities", "humility"],
    "love": [
        "loving_god",
        "loving_others",
        "forgiveness",
        "marriage",
        "parenting",
        "family",
        "friendship",
        "conflict",
        "service",
    ],
    "foundations": [
        "who_god_is",
        "jesus",
        "grace",
        "prayer",
        "scripture",
        "holy_spirit",
        "doubt",
        "identity",
    ],
    "character": ["patience", "hope", "joy"],
    "seasons": ["singleness", "aging", "change", "eternity"],
}
ALL_TOPIC_KEYS = [key for keys in TOPIC_KEYS.values() for key in keys]

FAITH_BACKGROUNDS = [
    {
        "key": "exploring",
        "title": L(
            "Exploring - not sure what I believe",
            "Explorando: no estoy seguro de lo que creo",
        ),
    },
    {"key": "new", "title": L("New to following Jesus", "Nuevo siguiendo a Jesús")},
    {
        "key": "returning",
        "title": L(
            "Coming back after time away", "Regresando después de un tiempo lejos"
        ),
    },
    {
        "key": "growing",
        "title": L("Following Jesus and growing", "Siguiendo a Jesús y creciendo"),
    },
    {
        "key": "mature",
        "title": L(
            "Following Jesus for many years", "Siguiendo a Jesús por muchos años"
        ),
    },
]
FAITH_BACKGROUND_KEYS = [f["key"] for f in FAITH_BACKGROUNDS]

# Self-assessment. Every item is answered 1-5:
#   1 = rarely / not at all true ... 5 = almost always / very true.
# "area" groups items into the two halves of the profile.
SCALE = L(
    "1 = rarely true of me · 5 = almost always true of me",
    "1 = rara vez cierto en mí · 5 = casi siempre cierto en mí",
)

ASSESSMENT_ITEMS = [
    # --- Spiritual practices
    {
        "key": "prayer",
        "area": "practices",
        "text": L(
            "I talk with God most days.", "Hablo con Dios la mayoría de los días."
        ),
    },
    {
        "key": "scripture",
        "area": "practices",
        "text": L(
            "I read or listen to the Bible most weeks.",
            "Leo o escucho la Biblia la mayoría de las semanas.",
        ),
    },
    {
        "key": "community",
        "area": "practices",
        "text": L(
            "I have people I worship or talk about faith with.",
            "Tengo personas con quienes adoro o hablo de la fe.",
        ),
    },
    {
        "key": "serving",
        "area": "practices",
        "text": L(
            "I regularly do something for others that costs me something.",
            "Con frecuencia hago por otros algo que me cuesta.",
        ),
    },
    {
        "key": "sabbath",
        "area": "practices",
        "text": L(
            "I take real rest without guilt.", "Tomo descanso verdadero sin culpa."
        ),
    },
    {
        "key": "confession",
        "area": "practices",
        "text": L(
            "When I do wrong, I admit it to God and to the person I hurt.",
            "Cuando hago mal, lo reconozco ante Dios y ante quien lastimé.",
        ),
    },
    # --- Inner life (how I tend to think, feel and respond)
    {
        "key": "calm",
        "area": "inner",
        "text": L(
            "When something goes wrong, I can stay steady.",
            "Cuando algo sale mal, puedo mantenerme estable.",
        ),
    },
    {
        "key": "hopeful",
        "area": "inner",
        "text": L(
            "I expect good to come, even when things are hard.",
            "Espero que venga algo bueno, aun cuando las cosas son difíciles.",
        ),
    },
    {
        "key": "self_kind",
        "area": "inner",
        "text": L(
            "I speak to myself the way I would speak to a friend.",
            "Me hablo a mí mismo como le hablaría a un amigo.",
        ),
    },
    {
        "key": "connected",
        "area": "inner",
        "text": L(
            "There is someone I can tell the truth about how I am.",
            "Hay alguien a quien puedo decirle la verdad de cómo estoy.",
        ),
    },
    {
        "key": "purpose",
        "area": "inner",
        "text": L("My days feel like they matter.", "Siento que mis días importan."),
    },
    {
        "key": "release",
        "area": "inner",
        "text": L(
            "I can let go of what I cannot control.",
            "Puedo soltar lo que no puedo controlar.",
        ),
    },
    {
        "key": "rested",
        "area": "inner",
        "text": L(
            "I have energy for the people and work in front of me.",
            "Tengo energía para las personas y el trabajo que tengo delante.",
        ),
    },
    {
        "key": "honest_feelings",
        "area": "inner",
        "text": L(
            "I can name what I am feeling instead of pushing it down.",
            "Puedo nombrar lo que siento en lugar de reprimirlo.",
        ),
    },
]
ASSESSMENT_KEYS = [item["key"] for item in ASSESSMENT_ITEMS]

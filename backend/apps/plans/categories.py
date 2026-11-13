"""
Reading-plan categories: the one list every part of the app uses.

The plan builder, the plans filter, plan validation and the AI's category
suggestion all read from here. To add a category, add a line below (keys are
lowercase, at most 30 characters, and must never be renamed once plans use
them) and create a migration for the model's `choices`.
"""

GROUPS = [
    (
        "faith",
        {"en": "Faith", "es": "Fe"},
        [
            ("general", "General", "General"),
            ("faith", "Faith Foundations", "Fundamentos de la fe"),
            ("knowing_god", "Knowing God", "Conocer a Dios"),
            ("jesus", "Life and Teaching of Jesus", "Vida y enseñanza de Jesús"),
            ("prayer", "Prayer", "Oración"),
            ("worship", "Worship and Gratitude", "Adoración y gratitud"),
            ("holy_spirit", "The Holy Spirit", "El Espíritu Santo"),
            ("discipleship", "Following Jesus", "Seguir a Jesús"),
            ("doubt", "Doubt and Questions", "Dudas y preguntas"),
        ],
    ),
    (
        "scripture",
        {"en": "Through the Bible", "es": "A través de la Biblia"},
        [
            ("bible_book", "A Book of the Bible", "Un libro de la Biblia"),
            ("psalms_proverbs", "Psalms and Proverbs", "Salmos y Proverbios"),
            ("gospels", "The Gospels", "Los Evangelios"),
            ("old_testament", "Old Testament", "Antiguo Testamento"),
            ("new_testament", "New Testament Letters", "Cartas del Nuevo Testamento"),
            ("people", "People of the Bible", "Personajes de la Biblia"),
        ],
    ),
    (
        "heart",
        {"en": "Heart and Mind", "es": "Corazón y mente"},
        [
            ("anxiety", "Anxiety and Peace", "Ansiedad y paz"),
            ("fear", "Fear and Courage", "Temor y valentía"),
            ("grief", "Grief and Loss", "Duelo y pérdida"),
            ("suffering", "Hardship and Suffering", "Dificultad y sufrimiento"),
            ("healing", "Illness and Healing", "Enfermedad y sanidad"),
            ("hope", "Hope", "Esperanza"),
            ("identity", "Identity and Worth", "Identidad y valor"),
            ("forgiveness", "Forgiveness", "Perdón"),
            ("anger", "Anger and Conflict", "Enojo y conflicto"),
            ("temptation", "Temptation and Purity", "Tentación y pureza"),
            ("recovery", "Recovery", "Recuperación"),
            ("rest", "Rest and Burnout", "Descanso y agotamiento"),
        ],
    ),
    (
        "relationships",
        {"en": "Relationships and Family", "es": "Relaciones y familia"},
        [
            ("marriage", "Marriage", "Matrimonio"),
            ("parenting", "Parenting", "Crianza de los hijos"),
            ("fatherhood", "Fatherhood", "Paternidad"),
            ("motherhood", "Motherhood", "Maternidad"),
            ("family", "Family", "Familia"),
            ("singleness", "Singleness", "Soltería"),
            ("friendship", "Friendship and Community", "Amistad y comunidad"),
        ],
    ),
    (
        "calling",
        {"en": "Calling and Character", "es": "Vocación y carácter"},
        [
            ("character", "Character and Virtue", "Carácter y virtud"),
            ("wisdom", "Wisdom and Decisions", "Sabiduría y decisiones"),
            ("leadership", "Leadership", "Liderazgo"),
            ("work", "Work and Calling", "Trabajo y vocación"),
            ("money", "Money and Generosity", "Dinero y generosidad"),
            ("service", "Serving Others", "Servir a los demás"),
            ("justice", "Justice and Mercy", "Justicia y misericordia"),
        ],
    ),
    (
        "seasons",
        {"en": "Seasons of Life and the Year", "es": "Etapas de la vida y del año"},
        [
            ("kids", "Children and Families", "Niños y familias"),
            ("youth", "Teens and Young Adults", "Adolescentes y jóvenes"),
            ("later_years", "Later Years", "Adultos mayores"),
            (
                "new_beginnings",
                "Change and New Beginnings",
                "Cambios y nuevos comienzos",
            ),
            ("advent", "Advent and Christmas", "Adviento y Navidad"),
            ("lent", "Lent and Easter", "Cuaresma y Pascua"),
        ],
    ),
]

DEFAULT_CATEGORY = "general"

# (key, English label) pairs for the model field, in display order.
CATEGORY_CHOICES = [
    (key, en) for _group, _title, items in GROUPS for key, en, _es in items
]
CATEGORY_KEYS = [key for key, _label in CATEGORY_CHOICES]
_LABELS = {
    key: {"en": en, "es": es}
    for _group, _title, items in GROUPS
    for key, en, es in items
}


def is_category(value) -> bool:
    return isinstance(value, str) and value in _LABELS


def category_label(key: str, lang: str = "en") -> str:
    """The display name of a category; an unknown key is shown as written."""
    labels = _LABELS.get(key)
    if not labels:
        return str(key).replace("_", " ").title()
    return labels.get(lang) or labels["en"]


def grouped(lang: str = "en", counts=None) -> list:
    """Categories grouped for a picker, with how many plans the person can see in each."""
    counts = counts or {}
    return [
        {
            "key": group,
            "title": title.get(lang) or title["en"],
            "categories": [
                {
                    "value": key,
                    "label": es if lang == "es" else en,
                    "plan_count": counts.get(key, 0),
                }
                for key, en, es in items
            ],
        }
        for group, title, items in GROUPS
    ]

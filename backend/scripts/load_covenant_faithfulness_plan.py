"""
Management-style script to load the "Covenant Faithfulness — A 4-Week Deep Dive"
reading plan into the database.

Run from the backend directory:
    python manage.py shell < scripts/load_covenant_faithfulness_plan.py
"""

import django
import os
import sys

# Allow running directly via `python scripts/load_covenant_faithfulness_plan.py`
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
    django.setup()

from apps.plans.models import ReadingPlan, ReadingPlanDay

# ---------------------------------------------------------------------------
# Plan metadata
# ---------------------------------------------------------------------------
PLAN = {
    "title_en": "Covenant Faithfulness — A 4-Week Deep Dive",
    "title_es": "Fidelidad al Pacto — Un Estudio Profundo de 4 Semanas",
    "description_en": (
        "Based on the Four Keys Moses gave Israel in Deuteronomy 29: Remember, Obey, "
        "Focus, and Recall. Each week anchors on one key and moves through supporting "
        "passages, daily reflection prompts, and bilingual journaling exercises. "
        "Pairs well with My Utmost for His Highest (Oswald Chambers)."
    ),
    "description_es": (
        "Basado en las Cuatro Claves que Moisés dio a Israel en Deuteronomio 29: "
        "Recordar, Obedecer, Enfocarse y Rememorar. Cada semana ancla en una clave "
        "y avanza a través de pasajes de apoyo, preguntas de reflexión diarias y "
        "ejercicios de journaling bilingüe."
    ),
    "duration_days": 28,
    "category": "faith",
}

# ---------------------------------------------------------------------------
# Daily plan — 4 weeks × 7 days
# ---------------------------------------------------------------------------
DAYS = [
    # -----------------------------------------------------------------------
    # WEEK 1 — REMEMBER (Deuteronomy 8)
    # -----------------------------------------------------------------------
    {
        "day_number": 1,
        "passages": ["Deuteronomy 29:1-9"],
        "theme_en": "Week 1 — Remember: The Covenant Recalled",
        "theme_es": "Semana 1 — Recordar: El Pacto Recordado",
        "reflection_prompts_seed": (
            "Moses opens by recounting what God has done. "
            "What specific provision has God made in your life that you risk forgetting? "
            "Why do we lose sight of past faithfulness?"
        ),
    },
    {
        "day_number": 2,
        "passages": ["Deuteronomy 8:1-10"],
        "theme_en": "Week 1 — Remember: Bread in the Wilderness",
        "theme_es": "Semana 1 — Recordar: Pan en el Desierto",
        "reflection_prompts_seed": (
            "God humbled Israel to test what was in their heart. "
            "What wilderness season has God used to reveal something true about you? "
            "How did he provide even then?"
        ),
    },
    {
        "day_number": 3,
        "passages": ["Deuteronomy 8:11-20"],
        "theme_en": "Week 1 — Remember: The Danger of Forgetting",
        "theme_es": "Semana 1 — Recordar: El Peligro de Olvidar",
        "reflection_prompts_seed": (
            "Moses warns: when you prosper, do not forget the Lord. "
            "In what area of life are you most tempted to credit yourself instead of God?"
        ),
    },
    {
        "day_number": 4,
        "passages": ["Psalm 103:1-14"],
        "theme_en": "Week 1 — Remember: Bless the Lord, Forget Not",
        "theme_es": "Semana 1 — Recordar: Bendice al Señor, No Olvides",
        "reflection_prompts_seed": (
            "David commands his own soul to remember God's benefits. "
            "List three specific benefits from this psalm you have personally experienced. "
            "Which one do you most need to hold onto right now?"
        ),
    },
    {
        "day_number": 5,
        "passages": ["Isaiah 46:8-11"],
        "theme_en": "Week 1 — Remember: God Declares the End from the Beginning",
        "theme_es": "Semana 1 — Recordar: Dios Declara el Fin desde el Principio",
        "reflection_prompts_seed": (
            "God calls Israel to remember and consider. "
            "How does God's sovereignty over history give you confidence in your current uncertainty?"
        ),
    },
    {
        "day_number": 6,
        "passages": ["Lamentations 3:19-26"],
        "theme_en": "Week 1 — Remember: Great Is Your Faithfulness",
        "theme_es": "Semana 1 — Recordar: Grande Es Tu Fidelidad",
        "reflection_prompts_seed": (
            "Jeremiah moves from despair to hope by choosing to remember God's mercies. "
            "What grief or disappointment do you need to bring to the Lord this week? "
            "What truth about his character can anchor you?"
        ),
    },
    {
        "day_number": 7,
        "passages": ["Deuteronomy 8:1-20"],
        "theme_en": "Week 1 — Remember: Sabbath Review",
        "theme_es": "Semana 1 — Recordar: Revisión de Sábado",
        "reflection_prompts_seed": (
            "Review the week. What specific moment has God provided for you that you nearly forgot? "
            "Write a one-paragraph prayer of remembrance."
        ),
    },
    # -----------------------------------------------------------------------
    # WEEK 2 — OBEY (James 1:22–25)
    # -----------------------------------------------------------------------
    {
        "day_number": 8,
        "passages": ["James 1:22-25"],
        "theme_en": "Week 2 — Obey: Doers, Not Hearers",
        "theme_es": "Semana 2 — Obedecer: Hacedores, No Solo Oidores",
        "reflection_prompts_seed": (
            "James warns against deceiving yourself by only hearing the word. "
            "What is the last clear instruction from Scripture you have not yet acted on?"
        ),
    },
    {
        "day_number": 9,
        "passages": ["Deuteronomy 29:10-21"],
        "theme_en": "Week 2 — Obey: Standing Before the Lord",
        "theme_es": "Semana 2 — Obedecer: Estar Delante del Señor",
        "reflection_prompts_seed": (
            "The covenant stands for 'whoever is here today and whoever is not here today.' "
            "What area of disobedience are you rationalizing as acceptable or minor?"
        ),
    },
    {
        "day_number": 10,
        "passages": ["John 14:15-21"],
        "theme_en": "Week 2 — Obey: Love and Obedience",
        "theme_es": "Semana 2 — Obedecer: Amor y Obediencia",
        "reflection_prompts_seed": (
            "Jesus says 'if you love me, keep my commandments.' "
            "Is your obedience to God driven by love or by duty/fear? "
            "What's the difference in how that shows up daily?"
        ),
    },
    {
        "day_number": 11,
        "passages": ["Romans 6:15-23"],
        "theme_en": "Week 2 — Obey: Slaves to Righteousness",
        "theme_es": "Semana 2 — Obedecer: Esclavos de la Justicia",
        "reflection_prompts_seed": (
            "Paul says you present yourself as a slave to whom you obey. "
            "What habit or pattern in your life is demanding obedience right now — "
            "and who or what are you actually serving through it?"
        ),
    },
    {
        "day_number": 12,
        "passages": ["1 Samuel 15:20-23"],
        "theme_en": "Week 2 — Obey: Obedience Better Than Sacrifice",
        "theme_es": "Semana 2 — Obedecer: Mejor Es Obedecer que Sacrificar",
        "reflection_prompts_seed": (
            "Saul rationalized partial obedience as full obedience. "
            "Where are you offering God religious activity while withholding actual compliance?"
        ),
    },
    {
        "day_number": 13,
        "passages": ["Matthew 7:24-27"],
        "theme_en": "Week 2 — Obey: Building on the Rock",
        "theme_es": "Semana 2 — Obedecer: Edificar Sobre la Roca",
        "reflection_prompts_seed": (
            "The difference between the two builders is not what they hear but what they do. "
            "What storm in your life is currently testing the foundation of your obedience?"
        ),
    },
    {
        "day_number": 14,
        "passages": ["James 1:22-25", "1 Samuel 15:22"],
        "theme_en": "Week 2 — Obey: Sabbath Review",
        "theme_es": "Semana 2 — Obedecer: Revisión de Sábado",
        "reflection_prompts_seed": (
            "Review the week. What one specific act of obedience will you commit to this coming week? "
            "Write it as a concrete, measurable action."
        ),
    },
    # -----------------------------------------------------------------------
    # WEEK 3 — FOCUS (Colossians 3:1–10)
    # -----------------------------------------------------------------------
    {
        "day_number": 15,
        "passages": ["Colossians 3:1-10"],
        "theme_en": "Week 3 — Focus: Set Your Mind on Things Above",
        "theme_es": "Semana 3 — Enfocarse: Poned la Mira en las Cosas de Arriba",
        "reflection_prompts_seed": (
            "Paul commands us to set our minds — it is a deliberate act. "
            "What 'earthly thing' (distraction, habit, ambition, or idol) is currently pulling your focus away from Christ?"
        ),
    },
    {
        "day_number": 16,
        "passages": ["Deuteronomy 29:22-29"],
        "theme_en": "Week 3 — Focus: The Secret Things Belong to God",
        "theme_es": "Semana 3 — Enfocarse: Las Cosas Secretas Pertenecen a Dios",
        "reflection_prompts_seed": (
            "Moses says the secret things belong to God but the revealed things belong to us. "
            "Are you spending energy obsessing over what God has not revealed, "
            "while neglecting what he has clearly shown you?"
        ),
    },
    {
        "day_number": 17,
        "passages": ["Hebrews 12:1-3"],
        "theme_en": "Week 3 — Focus: Fixing Our Eyes on Jesus",
        "theme_es": "Semana 3 — Enfocarse: Puestos los Ojos en Jesús",
        "reflection_prompts_seed": (
            "The writer calls us to throw off everything that hinders and fix our eyes on Jesus. "
            "What 'weight' — not necessarily sinful, just heavy — do you need to lay down to run your race?"
        ),
    },
    {
        "day_number": 18,
        "passages": ["Philippians 4:4-9"],
        "theme_en": "Week 3 — Focus: Whatever Is True, Think on These Things",
        "theme_es": "Semana 3 — Enfocarse: Todo Lo Verdadero, en Esto Pensad",
        "reflection_prompts_seed": (
            "Paul gives a specific mental diet: true, honorable, just, pure, lovely, commendable. "
            "Audit your media and conversation diet this past week — how does it measure against this list?"
        ),
    },
    {
        "day_number": 19,
        "passages": ["Matthew 6:19-24"],
        "theme_en": "Week 3 — Focus: Where Your Treasure Is",
        "theme_es": "Semana 3 — Enfocarse: Donde Esté Tu Tesoro",
        "reflection_prompts_seed": (
            "Jesus says the eye is the lamp of the body — what you focus on fills you with light or darkness. "
            "What does your calendar and your spending reveal about what you actually treasure?"
        ),
    },
    {
        "day_number": 20,
        "passages": ["2 Corinthians 4:16-18"],
        "theme_en": "Week 3 — Focus: Eternal Weight of Glory",
        "theme_es": "Semana 3 — Enfocarse: Eterno Peso de Gloria",
        "reflection_prompts_seed": (
            "Paul calls present suffering 'light and momentary' compared to eternal glory. "
            "What present hardship are you struggling to see as temporary? "
            "How would an eternal perspective change how you carry it?"
        ),
    },
    {
        "day_number": 21,
        "passages": ["Colossians 3:1-10", "Hebrews 12:1-3"],
        "theme_en": "Week 3 — Focus: Sabbath Review",
        "theme_es": "Semana 3 — Enfocarse: Revisión de Sábado",
        "reflection_prompts_seed": (
            "Review the week. Name the one idol or distraction you identified. "
            "What practical boundary will you put in place to protect your focus this week?"
        ),
    },
    # -----------------------------------------------------------------------
    # WEEK 4 — RECALL (Psalm 77)
    # -----------------------------------------------------------------------
    {
        "day_number": 22,
        "passages": ["Psalm 77:1-12"],
        "theme_en": "Week 4 — Recall: I Will Remember Your Deeds",
        "theme_es": "Semana 4 — Rememorar: Recordaré las Obras del Señor",
        "reflection_prompts_seed": (
            "Asaph moves from anguished questioning to deliberate remembrance. "
            "What has God revealed to you in this 4-week study that you haven't yet acted on?"
        ),
    },
    {
        "day_number": 23,
        "passages": ["Psalm 77:13-20"],
        "theme_en": "Week 4 — Recall: Your Way Was Through the Sea",
        "theme_es": "Semana 4 — Rememorar: Tu Camino Estuvo en el Mar",
        "reflection_prompts_seed": (
            "God's footprints were unseen but his path was certain. "
            "Where in your past can you now see God's hand even though you couldn't at the time?"
        ),
    },
    {
        "day_number": 24,
        "passages": ["Joshua 4:1-9"],
        "theme_en": "Week 4 — Recall: Stones of Remembrance",
        "theme_es": "Semana 4 — Rememorar: Piedras de Recordatorio",
        "reflection_prompts_seed": (
            "God told Israel to set up stones so future generations could ask 'what do these mean?' "
            "What 'stone of remembrance' could you set up in your own life to mark what God has done?"
        ),
    },
    {
        "day_number": 25,
        "passages": ["1 Corinthians 11:23-26"],
        "theme_en": "Week 4 — Recall: Do This in Remembrance",
        "theme_es": "Semana 4 — Rememorar: Haced Esto en Memoria de Mí",
        "reflection_prompts_seed": (
            "Jesus instituted the Lord's Supper as a commanded act of recall. "
            "How do the rhythms of your week create space to remember what Christ has done — "
            "not just at communion, but daily?"
        ),
    },
    {
        "day_number": 26,
        "passages": ["2 Timothy 2:8-13"],
        "theme_en": "Week 4 — Recall: Remember Jesus Christ",
        "theme_es": "Semana 4 — Rememorar: Recuerda a Jesucristo",
        "reflection_prompts_seed": (
            "Paul, writing from prison, says 'remember Jesus Christ.' "
            "What suffering are you currently enduring? "
            "How does remembering the resurrection change how you hold that suffering?"
        ),
    },
    {
        "day_number": 27,
        "passages": ["Deuteronomy 29:1-29"],
        "theme_en": "Week 4 — Recall: The Whole Covenant Revisited",
        "theme_es": "Semana 4 — Rememorar: Todo el Pacto Revisitado",
        "reflection_prompts_seed": (
            "Read the full anchor passage from week 1. "
            "How does it read differently now? "
            "Which of the four keys — Remember, Obey, Focus, Recall — do you most need to return to?"
        ),
    },
    {
        "day_number": 28,
        "passages": [
            "Psalm 77:1-20",
            "Colossians 3:1-10",
            "James 1:22-25",
            "Deuteronomy 8:1-20",
        ],
        "theme_en": "Week 4 — Recall: Covenant Faithfulness — Final Review",
        "theme_es": "Semana 4 — Rememorar: Fidelidad al Pacto — Revisión Final",
        "reflection_prompts_seed": (
            "Final day. Look back across all 28 days. "
            "Write responses to all four core questions: "
            "(1) What specific moment has God provided that you nearly forgot? "
            "(2) What area of disobedience were you rationalizing? "
            "(3) What idol was pulling your focus? "
            "(4) What has God revealed that you haven't yet acted on?"
        ),
    },
]


def run():
    plan, created = ReadingPlan.objects.get_or_create(
        title_en=PLAN["title_en"],
        defaults={
            "title_es": PLAN["title_es"],
            "description_en": PLAN["description_en"],
            "description_es": PLAN["description_es"],
            "duration_days": PLAN["duration_days"],
            "category": PLAN["category"],
            "is_active": True,
            "is_premium": False,
        },
    )

    action = "Created" if created else "Found existing"
    print(f"{action} plan: {plan.title_en} (id={plan.id})")

    if not created:
        existing_count = plan.days.count()
        print(f"  Plan already has {existing_count} days — skipping day creation.")
        return

    for day_data in DAYS:
        ReadingPlanDay.objects.create(plan=plan, **day_data)

    print(f"  Created {len(DAYS)} days.")
    print("Done.")


run()

#!/usr/bin/env python
"""
Seed initial reading plans into the database.

Usage:
    python manage.py shell < scripts/seed_plans.py
    # OR
    python scripts/seed_plans.py  (if DJANGO_SETTINGS_MODULE is set)
"""
import os
import sys
from pathlib import Path

# Setup Django if running standalone
if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
    import django
    django.setup()

from apps.plans.models import ReadingPlan, ReadingPlanDay

# Seed reading plans
SEED_PLANS = [
    {
        'title_en': '30 Days in Psalms',
        'title_es': '30 Días en los Salmos',
        'description_en': 'A month-long journey through the Psalms, exploring themes of praise, lament, and trust in God.',
        'description_es': 'Un viaje de un mes a través de los Salmos, explorando temas de alabanza, lamento y confianza en Dios.',
        'duration_days': 30,
        'category': 'faith',
        'is_premium': False,
        'days': [
            {'day': 1, 'passages': [{'book': 'PSA', 'chapter': 1}], 'theme_en': 'The Blessed Man', 'theme_es': 'El Hombre Bienaventurado'},
            {'day': 2, 'passages': [{'book': 'PSA', 'chapter': 8}], 'theme_en': 'God\'s Glory in Creation', 'theme_es': 'La Gloria de Dios en la Creación'},
            {'day': 3, 'passages': [{'book': 'PSA', 'chapter': 19}], 'theme_en': 'The Heavens Declare', 'theme_es': 'Los Cielos Cuentan'},
            {'day': 4, 'passages': [{'book': 'PSA', 'chapter': 23}], 'theme_en': 'The Lord is My Shepherd', 'theme_es': 'El Señor es Mi Pastor'},
            {'day': 5, 'passages': [{'book': 'PSA', 'chapter': 27}], 'theme_en': 'Seeking God\'s Face', 'theme_es': 'Buscando el Rostro de Dios'},
            {'day': 6, 'passages': [{'book': 'PSA', 'chapter': 32}], 'theme_en': 'The Joy of Forgiveness', 'theme_es': 'El Gozo del Perdón'},
            {'day': 7, 'passages': [{'book': 'PSA', 'chapter': 34}], 'theme_en': 'Taste and See', 'theme_es': 'Gustad y Ved'},
            {'day': 8, 'passages': [{'book': 'PSA', 'chapter': 37}], 'theme_en': 'Trust in the Lord', 'theme_es': 'Confía en el Señor'},
            {'day': 9, 'passages': [{'book': 'PSA', 'chapter': 40}], 'theme_en': 'Waiting on God', 'theme_es': 'Esperando en Dios'},
            {'day': 10, 'passages': [{'book': 'PSA', 'chapter': 42}], 'theme_en': 'Thirsting for God', 'theme_es': 'Sed de Dios'},
            {'day': 11, 'passages': [{'book': 'PSA', 'chapter': 46}], 'theme_en': 'God is Our Refuge', 'theme_es': 'Dios es Nuestro Refugio'},
            {'day': 12, 'passages': [{'book': 'PSA', 'chapter': 51}], 'theme_en': 'A Contrite Heart', 'theme_es': 'Un Corazón Contrito'},
            {'day': 13, 'passages': [{'book': 'PSA', 'chapter': 63}], 'theme_en': 'Earnestly Seeking', 'theme_es': 'Buscando con Anhelo'},
            {'day': 14, 'passages': [{'book': 'PSA', 'chapter': 73}], 'theme_en': 'When the Wicked Prosper', 'theme_es': 'Cuando los Impíos Prosperan'},
            {'day': 15, 'passages': [{'book': 'PSA', 'chapter': 84}], 'theme_en': 'Longing for God\'s House', 'theme_es': 'Anhelo por la Casa de Dios'},
            {'day': 16, 'passages': [{'book': 'PSA', 'chapter': 90}], 'theme_en': 'Numbering Our Days', 'theme_es': 'Contando Nuestros Días'},
            {'day': 17, 'passages': [{'book': 'PSA', 'chapter': 91}], 'theme_en': 'Under His Wings', 'theme_es': 'Bajo Sus Alas'},
            {'day': 18, 'passages': [{'book': 'PSA', 'chapter': 100}], 'theme_en': 'Enter with Thanksgiving', 'theme_es': 'Entrad con Acción de Gracias'},
            {'day': 19, 'passages': [{'book': 'PSA', 'chapter': 103}], 'theme_en': 'Bless the Lord', 'theme_es': 'Bendice al Señor'},
            {'day': 20, 'passages': [{'book': 'PSA', 'chapter': 107}], 'theme_en': 'Give Thanks', 'theme_es': 'Dad Gracias'},
            {'day': 21, 'passages': [{'book': 'PSA', 'chapter': 119, 'verses': '1-32'}], 'theme_en': 'Delighting in God\'s Word', 'theme_es': 'Deleitándose en la Palabra'},
            {'day': 22, 'passages': [{'book': 'PSA', 'chapter': 119, 'verses': '33-72'}], 'theme_en': 'Walking in Truth', 'theme_es': 'Caminando en Verdad'},
            {'day': 23, 'passages': [{'book': 'PSA', 'chapter': 119, 'verses': '73-112'}], 'theme_en': 'Affliction and Comfort', 'theme_es': 'Aflicción y Consuelo'},
            {'day': 24, 'passages': [{'book': 'PSA', 'chapter': 119, 'verses': '113-152'}], 'theme_en': 'Sustaining Hope', 'theme_es': 'Esperanza que Sostiene'},
            {'day': 25, 'passages': [{'book': 'PSA', 'chapter': 119, 'verses': '153-176'}], 'theme_en': 'Longing for Salvation', 'theme_es': 'Anhelo de Salvación'},
            {'day': 26, 'passages': [{'book': 'PSA', 'chapter': 121}], 'theme_en': 'My Help Comes from the Lord', 'theme_es': 'Mi Socorro Viene del Señor'},
            {'day': 27, 'passages': [{'book': 'PSA', 'chapter': 139}], 'theme_en': 'Fearfully and Wonderfully Made', 'theme_es': 'Formidable y Maravillosamente Hecho'},
            {'day': 28, 'passages': [{'book': 'PSA', 'chapter': 145}], 'theme_en': 'Great is the Lord', 'theme_es': 'Grande es el Señor'},
            {'day': 29, 'passages': [{'book': 'PSA', 'chapter': 146}], 'theme_en': 'Praise the Lord', 'theme_es': 'Alabad al Señor'},
            {'day': 30, 'passages': [{'book': 'PSA', 'chapter': 150}], 'theme_en': 'Let Everything Praise', 'theme_es': 'Que Todo Alabe'},
        ],
    },
    {
        'title_en': 'Fatherhood in Scripture',
        'title_es': 'La Paternidad en las Escrituras',
        'description_en': 'A 14-day study on what the Bible teaches about being a godly father and raising children.',
        'description_es': 'Un estudio de 14 días sobre lo que la Biblia enseña acerca de ser un padre piadoso y criar hijos.',
        'duration_days': 14,
        'category': 'fatherhood',
        'is_premium': False,
        'days': [
            {'day': 1, 'passages': [{'book': 'DEU', 'chapter': 6, 'verses': '1-9'}], 'theme_en': 'Teaching Your Children', 'theme_es': 'Enseñando a Tus Hijos'},
            {'day': 2, 'passages': [{'book': 'PRO', 'chapter': 22, 'verses': '6'}], 'theme_en': 'Training Up a Child', 'theme_es': 'Instruye al Niño'},
            {'day': 3, 'passages': [{'book': 'EPH', 'chapter': 6, 'verses': '1-4'}], 'theme_en': 'Fathers, Do Not Provoke', 'theme_es': 'Padres, No Provoquéis'},
            {'day': 4, 'passages': [{'book': 'COL', 'chapter': 3, 'verses': '20-21'}], 'theme_en': 'Encouraging Your Children', 'theme_es': 'Animando a Tus Hijos'},
            {'day': 5, 'passages': [{'book': 'PSA', 'chapter': 127}], 'theme_en': 'Children Are a Heritage', 'theme_es': 'Los Hijos Son Herencia'},
            {'day': 6, 'passages': [{'book': 'PRO', 'chapter': 13, 'verses': '24'}], 'theme_en': 'Loving Discipline', 'theme_es': 'Disciplina con Amor'},
            {'day': 7, 'passages': [{'book': 'PRO', 'chapter': 20, 'verses': '7'}], 'theme_en': 'Walking in Integrity', 'theme_es': 'Caminando en Integridad'},
            {'day': 8, 'passages': [{'book': '1TI', 'chapter': 3, 'verses': '4-5'}], 'theme_en': 'Managing Your Household', 'theme_es': 'Gobernando Tu Casa'},
            {'day': 9, 'passages': [{'book': 'GEN', 'chapter': 18, 'verses': '17-19'}], 'theme_en': 'Abraham\'s Example', 'theme_es': 'El Ejemplo de Abraham'},
            {'day': 10, 'passages': [{'book': 'JOS', 'chapter': 24, 'verses': '14-15'}], 'theme_en': 'As for Me and My House', 'theme_es': 'Yo y Mi Casa'},
            {'day': 11, 'passages': [{'book': 'LUK', 'chapter': 15, 'verses': '11-32'}], 'theme_en': 'The Prodigal Father', 'theme_es': 'El Padre del Pródigo'},
            {'day': 12, 'passages': [{'book': 'HEB', 'chapter': 12, 'verses': '5-11'}], 'theme_en': 'God\'s Fatherly Discipline', 'theme_es': 'La Disciplina del Padre'},
            {'day': 13, 'passages': [{'book': 'MAL', 'chapter': 4, 'verses': '5-6'}], 'theme_en': 'Turning Hearts', 'theme_es': 'Volviendo los Corazones'},
            {'day': 14, 'passages': [{'book': '3JN', 'chapter': 1, 'verses': '4'}], 'theme_en': 'Walking in Truth', 'theme_es': 'Caminando en Verdad'},
        ],
    },
    {
        'title_en': 'Leadership Lessons from Nehemiah',
        'title_es': 'Lecciones de Liderazgo de Nehemías',
        'description_en': 'Learn leadership principles from Nehemiah\'s example of rebuilding Jerusalem\'s walls.',
        'description_es': 'Aprende principios de liderazgo del ejemplo de Nehemías al reconstruir los muros de Jerusalén.',
        'duration_days': 7,
        'category': 'leadership',
        'is_premium': False,
        'days': [
            {'day': 1, 'passages': [{'book': 'NEH', 'chapter': 1}], 'theme_en': 'A Leader\'s Heart', 'theme_es': 'El Corazón de un Líder'},
            {'day': 2, 'passages': [{'book': 'NEH', 'chapter': 2, 'verses': '1-10'}], 'theme_en': 'Courage to Ask', 'theme_es': 'Valor para Pedir'},
            {'day': 3, 'passages': [{'book': 'NEH', 'chapter': 2, 'verses': '11-20'}], 'theme_en': 'Assessing the Situation', 'theme_es': 'Evaluando la Situación'},
            {'day': 4, 'passages': [{'book': 'NEH', 'chapter': 4}], 'theme_en': 'Facing Opposition', 'theme_es': 'Enfrentando la Oposición'},
            {'day': 5, 'passages': [{'book': 'NEH', 'chapter': 5}], 'theme_en': 'Addressing Injustice', 'theme_es': 'Enfrentando la Injusticia'},
            {'day': 6, 'passages': [{'book': 'NEH', 'chapter': 6}], 'theme_en': 'Staying Focused', 'theme_es': 'Manteniéndose Enfocado'},
            {'day': 7, 'passages': [{'book': 'NEH', 'chapter': 8}], 'theme_en': 'Spiritual Renewal', 'theme_es': 'Renovación Espiritual'},
        ],
    },
]


def seed_plans():
    """Seed reading plans into database."""
    for plan_data in SEED_PLANS:
        days_data = plan_data.pop('days')
        
        plan, created = ReadingPlan.objects.get_or_create(
            title_en=plan_data['title_en'],
            defaults=plan_data
        )
        
        if created:
            print(f"Created plan: {plan.title_en}")
            
            for day_data in days_data:
                ReadingPlanDay.objects.create(
                    plan=plan,
                    day_number=day_data['day'],
                    passages=day_data['passages'],
                    theme_en=day_data['theme_en'],
                    theme_es=day_data['theme_es'],
                    reflection_prompts_seed=f"Reflect on {day_data['theme_en']}",
                )
            
            print(f"  Added {len(days_data)} days")
        else:
            print(f"Plan already exists: {plan.title_en}")


if __name__ == '__main__':
    seed_plans()

"""
Migration: expand category choices and add curated reflection prompts.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plans", "0003_add_is_public_to_reading_plan"),
    ]

    operations = [
        migrations.AlterField(
            model_name="readingplan",
            name="category",
            field=models.CharField(
                choices=[
                    ("general", "General"),
                    ("faith", "Faith Foundations"),
                    ("disciplines", "Spiritual Disciplines"),
                    ("young_men", "Young Men"),
                    ("young_women", "Young Women"),
                    ("dating", "Single & Dating"),
                    ("marriage", "Marriage"),
                    ("husband_new", "New Husband"),
                    ("fatherhood", "Fatherhood"),
                    ("father_new", "New Father"),
                    ("motherhood", "Motherhood"),
                    ("parenting_teens", "Parenting Teens"),
                    ("leadership", "Leadership"),
                    ("work", "Workplace & Provision"),
                    ("recovery", "Recovery"),
                    ("anxiety", "Anxiety & Mental Health"),
                    ("anger", "Anger & Self-Control"),
                    ("grief", "Grief & Loss"),
                ],
                default="general",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="readingplanday",
            name="reflection_prompts",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="Curated reflection prompts shown to the user (English).",
            ),
        ),
        migrations.AddField(
            model_name="readingplanday",
            name="reflection_prompts_es",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="Curated reflection prompts shown to the user (Spanish).",
            ),
        ),
    ]

"""
Data migration: flip is_public=True on the four originally-seeded reading
plans so they appear in the public library. This is safe to re-run; it only
touches plans whose canonical titles match the seed.
"""

from django.db import migrations


SEEDED_TITLES = [
    "30 Days for Beginning Your Walk with Christ",
    "60-Day Overview of the Bible",
    "30 Famous Battles",
    "Not-So-Famous Bible Stories",
]


def publish_seeded(apps, schema_editor):
    ReadingPlan = apps.get_model("plans", "ReadingPlan")
    ReadingPlan.objects.filter(title_en__in=SEEDED_TITLES, is_public=False).update(
        is_public=True
    )


def noop(apps, schema_editor):
    # Reverse is intentionally a no-op; we don't want to hide plans on rollback.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("plans", "0004_expand_categories_and_prompts"),
    ]

    operations = [
        migrations.RunPython(publish_seeded, noop),
    ]

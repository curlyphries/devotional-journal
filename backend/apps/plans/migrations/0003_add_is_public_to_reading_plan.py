from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plans", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="readingplan",
            name="is_public",
            field=models.BooleanField(
                default=False,
                help_text="Public plans appear in the library for all users. Personal plans are only visible to their creator.",
            ),
        ),
    ]

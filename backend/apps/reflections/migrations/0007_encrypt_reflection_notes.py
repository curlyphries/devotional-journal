"""
Migration: Replace plaintext gratitude_note, struggle_note, tomorrow_intention
with encrypted BinaryField equivalents.

Data migration note: Any existing plaintext data in these columns will not be
automatically migrated (the old columns are dropped, new encrypted columns are
added as null). Existing rows will have null encrypted fields until the user
re-submits their reflections or a separate data migration is run.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reflections', '0006_studyguidesession'),
    ]

    operations = [
        # Remove the old plaintext columns
        migrations.RemoveField(
            model_name='dailyreflection',
            name='gratitude_note',
        ),
        migrations.RemoveField(
            model_name='dailyreflection',
            name='struggle_note',
        ),
        migrations.RemoveField(
            model_name='dailyreflection',
            name='tomorrow_intention',
        ),
        # Add encrypted replacements
        migrations.AddField(
            model_name='dailyreflection',
            name='encrypted_gratitude',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dailyreflection',
            name='encrypted_struggle',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dailyreflection',
            name='encrypted_tomorrow_intention',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]

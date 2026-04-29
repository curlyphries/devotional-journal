"""
Link journal entries to the user's active focus intention at time of writing.
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_initial'),
        ('reflections', '0007_encrypt_reflection_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentry',
            name='focus_intention',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='journal_entries',
                to='reflections.focusintention',
            ),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='focus_themes',
            field=models.JSONField(blank=True, default=list),
        ),
    ]

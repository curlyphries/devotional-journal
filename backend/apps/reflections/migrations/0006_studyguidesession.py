# Generated migration for StudyGuideSession model

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journal', '0003_initial'),
        ('reflections', '0005_devotionalaudit'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyGuideSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('source_type', models.CharField(choices=[('devotional_passage', 'Devotional Passage'), ('journal_entry', 'Journal Entry')], max_length=30)),
                ('source_reference', models.CharField(max_length=255)),
                ('guide_data', models.JSONField(default=dict)),
                ('completed_days', models.JSONField(blank=True, default=list)),
                ('day_notes', models.JSONField(blank=True, default=dict)),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('archived', 'Archived')], default='active', max_length=20)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('last_activity_at', models.DateTimeField(auto_now=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('source_journal_entry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_sessions', to='journal.journalentry')),
                ('source_passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_sessions', to='reflections.devotionalpassage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_guide_sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'study_guide_sessions',
                'ordering': ['-last_activity_at', '-started_at'],
            },
        ),
        migrations.AddIndex(
            model_name='studyguidesession',
            index=models.Index(fields=['user', 'status'], name='study_sessions_user_status_idx'),
        ),
        migrations.AddIndex(
            model_name='studyguidesession',
            index=models.Index(fields=['user', 'source_type'], name='study_sessions_user_source_idx'),
        ),
    ]

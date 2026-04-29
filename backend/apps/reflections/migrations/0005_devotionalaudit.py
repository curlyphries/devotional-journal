# Generated migration for DevotionalAudit model

import uuid

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reflections', '0004_scriptureinsight'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevotionalAudit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('scripture_accuracy_score', models.FloatField(blank=True, help_text='0.0-1.0 score from automated scripture verification', null=True)),
                ('scripture_warnings', models.JSONField(default=list, help_text='Warnings from scripture verification')),
                ('relevance_score', models.FloatField(blank=True, help_text="0.0-1.0 score for relevance to user's intention", null=True)),
                ('theological_accuracy', models.BooleanField(help_text='Manual review of theological accuracy', null=True)),
                ('user_rating', models.IntegerField(blank=True, help_text='User rating 1-5', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('user_feedback', models.TextField(blank=True)),
                ('reported_issue', models.TextField(blank=True)),
                ('audit_status', models.CharField(choices=[('pending', 'Pending Review'), ('verified', 'Verified Accurate'), ('flagged', 'Flagged for Issues'), ('corrected', 'Manually Corrected')], default='pending', max_length=20)),
                ('review_notes', models.TextField(blank=True)),
                ('corrected_content', models.JSONField(blank=True, help_text='Manually corrected devotional content', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('devotional_passage', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='audit', to='reflections.devotionalpassage')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devotional_reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Devotional Audit',
                'verbose_name_plural': 'Devotional Audits',
                'db_table': 'devotional_audits',
                'ordering': ['-created_at'],
            },
        ),
    ]

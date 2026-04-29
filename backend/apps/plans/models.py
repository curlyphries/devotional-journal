"""
Reading plan models.
"""
import uuid

from django.conf import settings
from django.db import models


class ReadingPlan(models.Model):
    """
    A structured Bible reading plan.
    """
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('fatherhood', 'Fatherhood'),
        ('leadership', 'Leadership'),
        ('recovery', 'Recovery'),
        ('marriage', 'Marriage'),
        ('faith', 'Faith Foundations'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_en = models.CharField(max_length=200)
    title_es = models.CharField(max_length=200, blank=True)
    description_en = models.TextField()
    description_es = models.TextField(blank=True)
    duration_days = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_plans'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reading_plans'

    def __str__(self):
        return self.title_en

    def get_title(self, language='en'):
        if language == 'es' and self.title_es:
            return self.title_es
        return self.title_en

    def get_description(self, language='en'):
        if language == 'es' and self.description_es:
            return self.description_es
        return self.description_en


class ReadingPlanDay(models.Model):
    """
    A single day within a reading plan.
    """
    plan = models.ForeignKey(ReadingPlan, on_delete=models.CASCADE, related_name='days')
    day_number = models.PositiveIntegerField()
    passages = models.JSONField(help_text="List of passage references")
    theme_en = models.CharField(max_length=200, blank=True)
    theme_es = models.CharField(max_length=200, blank=True)
    reflection_prompts_seed = models.TextField(
        blank=True,
        help_text="Seed prompt for LLM generation"
    )

    class Meta:
        db_table = 'reading_plan_days'
        unique_together = ['plan', 'day_number']
        ordering = ['day_number']

    def __str__(self):
        return f"{self.plan.title_en} - Day {self.day_number}"

    def get_theme(self, language='en'):
        if language == 'es' and self.theme_es:
            return self.theme_es
        return self.theme_en


class UserPlanEnrollment(models.Model):
    """
    Tracks a user's progress through a reading plan.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='plan_enrollments'
    )
    plan = models.ForeignKey(ReadingPlan, on_delete=models.CASCADE, related_name='enrollments')
    started_at = models.DateTimeField(auto_now_add=True)
    current_day = models.PositiveIntegerField(default=1)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_plan_enrollments'

    def __str__(self):
        return f"PlanEnrollment({self.id}) - {self.plan.title_en}"

    @property
    def is_completed(self):
        return self.completed_at is not None

    @property
    def progress_percentage(self):
        return round((self.current_day / self.plan.duration_days) * 100, 1)

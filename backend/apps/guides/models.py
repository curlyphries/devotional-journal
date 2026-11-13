"""
Models for Bible study guides, the growth profile and growth plans.

Anything a person wrote, and anything the app wrote *about* them, is stored
encrypted with their key (shared.encryption). Plain columns hold only what is
needed to query: keys from the catalog, dates, counts and 1-5 ratings.
"""

import json
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from shared.encryption import decrypt_content, encrypt_content


class EncryptedJSONMixin:
    """Helpers for models whose owner is reachable as `self._owner()`."""

    def _owner(self):
        return self.user

    def _encrypt(self, value) -> bytes:
        return encrypt_content(json.dumps(value), self._owner().encryption_key_salt)

    def _decrypt(self, blob, default):
        if not blob:
            return default
        return json.loads(
            decrypt_content(bytes(blob), self._owner().encryption_key_salt)
        )


class GrowthProfile(EncryptedJSONMixin, models.Model):
    """
    What a person has told the app about themselves, plus (optionally) the
    reflection the app wrote from their activity. One per person; they can
    edit it, correct it and erase it.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="growth_profile",
    )
    life_stage = models.CharField(max_length=20, blank=True)
    situations = models.JSONField(default=list, blank=True)
    faith_background = models.CharField(max_length=20, blank=True)
    needs = models.JSONField(default=list, blank=True)  # topic keys
    desired_traits = models.JSONField(default=list, blank=True)  # trait keys (max 3)

    encrypted_about_me = models.BinaryField(null=True, blank=True)
    # {"summary", "items": [{id, area, title, text, evidence, accurate}],
    #  "encouragement", "suggested_topics", "suggested_traits"}
    encrypted_insights = models.BinaryField(null=True, blank=True)
    insights_generated_at = models.DateTimeField(null=True, blank=True)
    insights_provider = models.CharField(max_length=30, blank=True)
    insights_model = models.CharField(max_length=100, blank=True)
    insights_local = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "growth_profiles"

    def __str__(self):
        return f"GrowthProfile({self.user_id})"

    @property
    def profiling_enabled(self) -> bool:
        """No inner-life profile or AI insight is ever built for a child."""
        return self.life_stage != "child"

    def set_about_me(self, text: str):
        text = (text or "").strip()
        self.encrypted_about_me = (
            encrypt_content(text, self.user.encryption_key_salt) if text else None
        )

    def get_about_me(self) -> str:
        if not self.encrypted_about_me:
            return ""
        return decrypt_content(
            bytes(self.encrypted_about_me), self.user.encryption_key_salt
        )

    def set_insights(self, insights):
        self.encrypted_insights = self._encrypt(insights) if insights else None

    def get_insights(self):
        return self._decrypt(self.encrypted_insights, None)


class ProfileAssessment(EncryptedJSONMixin, models.Model):
    """One sitting of the self-assessment. Kept as history to show change."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile_assessments",
    )
    # {"answers": {item: 1-5}, "trait_ratings": {trait: 1-5}}
    encrypted_payload = models.BinaryField()
    taken_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "profile_assessments"
        ordering = ["-taken_at"]

    def set_payload(self, payload: dict):
        self.encrypted_payload = self._encrypt(payload)

    def get_payload(self) -> dict:
        return self._decrypt(
            self.encrypted_payload, {"answers": {}, "trait_ratings": {}}
        )


class StudyEnrollment(models.Model):
    """A person working through one study topic from the library."""

    STATUS_CHOICES = [("active", "Active"), ("completed", "Completed")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="study_enrollments",
    )
    topic_key = models.CharField(max_length=40)
    life_stage = models.CharField(max_length=20, default="adult")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    current_lesson = models.PositiveIntegerField(default=1)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "study_enrollments"
        ordering = ["-started_at"]
        indexes = [models.Index(fields=["user", "topic_key"])]

    def __str__(self):
        return f"StudyEnrollment({self.topic_key}, {self.status})"


class LessonResponse(EncryptedJSONMixin, models.Model):
    """A person's answers to one lesson, and how the lesson was shown to them."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.ForeignKey(
        StudyEnrollment, on_delete=models.CASCADE, related_name="responses"
    )
    lesson_number = models.PositiveIntegerField()
    explanation_level = models.CharField(max_length=10, default="standard")
    # {"answers": [{question, answer}], "stood_out": str, "reply": {...}}
    encrypted_payload = models.BinaryField(null=True, blank=True)
    # {"connection", "explanation", "questions", "provider", "model", "local", "created_at"}
    encrypted_personal = models.BinaryField(null=True, blank=True)
    understanding = models.PositiveSmallIntegerField(null=True, blank=True)
    resonance = models.PositiveSmallIntegerField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lesson_responses"
        unique_together = ["enrollment", "lesson_number"]
        ordering = ["lesson_number"]

    def _owner(self):
        return self.enrollment.user

    def set_payload(self, payload):
        self.encrypted_payload = self._encrypt(payload) if payload else None

    def get_payload(self) -> dict:
        return self._decrypt(self.encrypted_payload, {})

    def set_personal(self, personal):
        self.encrypted_personal = self._encrypt(personal) if personal else None

    def get_personal(self):
        return self._decrypt(self.encrypted_personal, None)


class GrowthPlan(models.Model):
    """A characteristic a person has chosen to grow in, with goals and check-ins."""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="growth_plans"
    )
    trait_key = models.CharField(max_length=40)
    encrypted_why = models.BinaryField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    baseline_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    target_date = models.DateField()
    goal_source = models.CharField(max_length=10, default="catalog")
    personalize_error = models.JSONField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "growth_plans"
        ordering = ["-started_at"]

    def __str__(self):
        return f"GrowthPlan({self.trait_key}, {self.status})"

    def set_why(self, text: str):
        text = (text or "").strip()
        self.encrypted_why = (
            encrypt_content(text, self.user.encryption_key_salt) if text else None
        )

    def get_why(self) -> str:
        if not self.encrypted_why:
            return ""
        return decrypt_content(bytes(self.encrypted_why), self.user.encryption_key_salt)


class GrowthGoal(models.Model):
    HORIZON_CHOICES = [("short", "Short term"), ("long", "Long term")]
    STATUS_CHOICES = [("active", "Active"), ("done", "Done"), ("skipped", "Skipped")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(GrowthPlan, on_delete=models.CASCADE, related_name="goals")
    horizon = models.CharField(max_length=10, choices=HORIZON_CHOICES)
    encrypted_title = models.BinaryField()
    kind = models.CharField(max_length=20, default="practice")
    target_count = models.PositiveIntegerField(default=1)
    progress_count = models.PositiveIntegerField(default=0)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    # Study goals from the catalog are counted from completed lessons.
    auto = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "growth_goals"
        ordering = ["horizon", "order", "created_at"]

    def set_title(self, text: str):
        self.encrypted_title = encrypt_content(
            text.strip(), self.plan.user.encryption_key_salt
        )

    def get_title(self) -> str:
        return decrypt_content(
            bytes(self.encrypted_title), self.plan.user.encryption_key_salt
        )


class GrowthCheckIn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(
        GrowthPlan, on_delete=models.CASCADE, related_name="checkins"
    )
    date = models.DateField(default=timezone.localdate)
    rating = models.PositiveSmallIntegerField()
    encrypted_note = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "growth_checkins"
        ordering = ["-date", "-created_at"]

    def set_note(self, text: str):
        text = (text or "").strip()
        self.encrypted_note = (
            encrypt_content(text, self.plan.user.encryption_key_salt) if text else None
        )

    def get_note(self) -> str:
        if not self.encrypted_note:
            return ""
        return decrypt_content(
            bytes(self.encrypted_note), self.plan.user.encryption_key_salt
        )

"""
Life Reflection models for the devotional system.
Tracks user journeys, daily reflections, and life area assessments.
"""

import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from shared.encryption import decrypt_content, encrypt_content


class LifeArea(models.Model):
    """
    Core life domains for self-assessment.
    Pre-seeded reference data, not user-editable.
    """

    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="circle")
    scripture_tags = models.JSONField(
        default=list, help_text="Keywords that map to this area"
    )
    reflection_prompts = models.JSONField(
        default=list, help_text="Default prompts for this area"
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "life_areas"
        ordering = ["display_order"]
        verbose_name = "Life Area"
        verbose_name_plural = "Life Areas"

    def __str__(self):
        return self.name


class UserJourney(models.Model):
    """
    User's personal journey with their own goals.
    Supports flexible duration (7, 14, 21, 30, 90 days).
    """

    GOAL_CATEGORY_CHOICES = [
        ("breaking_habit", "Breaking a Habit"),
        ("building_habit", "Building a Habit"),
        ("healing", "Healing/Recovery"),
        ("relationship", "Relationship Repair"),
        ("purpose", "Identity/Purpose"),
        ("leadership", "Leadership Growth"),
        ("foundation", "Spiritual Foundation"),
    ]

    READING_MODE_CHOICES = [
        ("ai_suggested", "AI Suggested"),
        ("self_directed", "Self Directed"),
        ("hybrid", "Hybrid"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
        ("abandoned", "Abandoned"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="journeys"
    )

    title = models.CharField(max_length=200)
    duration_days = models.PositiveIntegerField(default=30)
    started_at = models.DateTimeField(default=timezone.now)

    goal_categories = models.JSONField(default=list)
    goal_statement = models.TextField(
        help_text="User's own words describing their goal"
    )
    success_definition = models.TextField(help_text="What does success look like?")
    focus_areas = models.JSONField(default=list, help_text="List of LifeArea codes")

    encrypted_specific_struggle = models.BinaryField(null=True, blank=True)

    reading_mode = models.CharField(
        max_length=20, choices=READING_MODE_CHOICES, default="hybrid"
    )
    reading_plan = models.ForeignKey(
        "plans.ReadingPlan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="journeys",
    )
    custom_readings = models.JSONField(default=list)

    current_day = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    completed_at = models.DateTimeField(null=True, blank=True)

    completion_reflection = models.TextField(blank=True)
    next_journey = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="previous_journey",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_journeys"
        ordering = ["-started_at"]
        verbose_name = "User Journey"
        verbose_name_plural = "User Journeys"

    def __str__(self):
        return f"Journey({self.id}) - {self.title}"

    def set_specific_struggle(self, content: str):
        """Encrypt and store specific struggle."""
        if content:
            self.encrypted_specific_struggle = encrypt_content(
                content, self.user.encryption_key_salt
            )
        else:
            self.encrypted_specific_struggle = None

    def get_specific_struggle(self) -> str:
        """Decrypt and return specific struggle."""
        if not self.encrypted_specific_struggle:
            return ""
        return decrypt_content(
            bytes(self.encrypted_specific_struggle), self.user.encryption_key_salt
        )

    @property
    def progress_percentage(self):
        if self.duration_days == 0:
            return 0
        return round((self.current_day / self.duration_days) * 100, 1)

    @property
    def is_completed(self):
        return self.status == "completed"

    @property
    def days_remaining(self):
        return max(0, self.duration_days - self.current_day)


class DailyReflection(models.Model):
    """
    User's end-of-day reflection tied to their scripture reading.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reflections"
    )
    journey = models.ForeignKey(
        UserJourney,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reflections",
    )
    date = models.DateField()

    scripture_reference = models.CharField(max_length=200)
    scripture_themes = models.JSONField(default=list, help_text="AI-extracted themes")

    encrypted_reflection = models.BinaryField(null=True, blank=True)

    area_scores = models.JSONField(
        default=dict, help_text="Life area scores: {'integrity': 4, 'faith': 3}"
    )

    encrypted_gratitude = models.BinaryField(null=True, blank=True)
    encrypted_struggle = models.BinaryField(null=True, blank=True)
    encrypted_tomorrow_intention = models.BinaryField(null=True, blank=True)

    ai_insight = models.TextField(blank=True)
    ai_provider_used = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "daily_reflections"
        ordering = ["-date", "-created_at"]
        unique_together = ["user", "date"]
        verbose_name = "Daily Reflection"
        verbose_name_plural = "Daily Reflections"

    def __str__(self):
        return f"Reflection({self.id}) - {self.date}"

    def set_reflection(self, content: str):
        """Encrypt and store reflection content."""
        if content:
            self.encrypted_reflection = encrypt_content(
                content, self.user.encryption_key_salt
            )
        else:
            self.encrypted_reflection = None

    def get_reflection(self) -> str:
        """Decrypt and return reflection content."""
        if not self.encrypted_reflection:
            return ""
        return decrypt_content(
            bytes(self.encrypted_reflection), self.user.encryption_key_salt
        )

    @property
    def reflection_content(self):
        return self.get_reflection()

    def set_gratitude_note(self, content: str):
        """Encrypt and store gratitude note."""
        if content:
            self.encrypted_gratitude = encrypt_content(
                content, self.user.encryption_key_salt
            )
        else:
            self.encrypted_gratitude = None

    def get_gratitude_note(self) -> str:
        """Decrypt and return gratitude note."""
        if not self.encrypted_gratitude:
            return ""
        return decrypt_content(
            bytes(self.encrypted_gratitude), self.user.encryption_key_salt
        )

    def set_struggle_note(self, content: str):
        """Encrypt and store struggle note."""
        if content:
            self.encrypted_struggle = encrypt_content(
                content, self.user.encryption_key_salt
            )
        else:
            self.encrypted_struggle = None

    def get_struggle_note(self) -> str:
        """Decrypt and return struggle note."""
        if not self.encrypted_struggle:
            return ""
        return decrypt_content(
            bytes(self.encrypted_struggle), self.user.encryption_key_salt
        )

    def set_tomorrow_intention(self, content: str):
        """Encrypt and store tomorrow intention."""
        if content:
            self.encrypted_tomorrow_intention = encrypt_content(
                content, self.user.encryption_key_salt
            )
        else:
            self.encrypted_tomorrow_intention = None

    def get_tomorrow_intention(self) -> str:
        """Decrypt and return tomorrow intention."""
        if not self.encrypted_tomorrow_intention:
            return ""
        return decrypt_content(
            bytes(self.encrypted_tomorrow_intention), self.user.encryption_key_salt
        )


class AlignmentTrend(models.Model):
    """
    Weekly/monthly aggregated alignment scores per life area.
    Computed by Celery task, not real-time.
    """

    PERIOD_TYPE_CHOICES = [
        ("week", "Week"),
        ("month", "Month"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="alignment_trends",
    )
    journey = models.ForeignKey(
        UserJourney,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alignment_trends",
    )

    period_type = models.CharField(max_length=10, choices=PERIOD_TYPE_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()

    area_averages = models.JSONField(
        default=dict, help_text="Average scores: {'integrity': 3.5, 'faith': 4.2}"
    )
    area_deltas = models.JSONField(
        default=dict,
        help_text="Change from previous: {'integrity': 0.3, 'faith': -0.1}",
    )

    ai_summary = models.TextField(blank=True)
    patterns = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "alignment_trends"
        ordering = ["-period_start"]
        unique_together = ["user", "period_type", "period_start"]
        verbose_name = "Alignment Trend"
        verbose_name_plural = "Alignment Trends"

    def __str__(self):
        return f"AlignmentTrend({self.id}) - {self.period_type} {self.period_start}"


class OpenThread(models.Model):
    """
    Tracks unresolved topics, struggles, or commitments the user has mentioned.
    The AI detects these and follows up to ensure nothing falls through the cracks.
    """

    THREAD_TYPE_CHOICES = [
        ("struggle", "Struggle/Challenge"),
        ("commitment", "Commitment Made"),
        ("question", "Unanswered Question"),
        ("relationship", "Relationship Issue"),
        ("decision", "Pending Decision"),
        ("confession", "Something Shared"),
    ]

    STATUS_CHOICES = [
        ("open", "Open - Active"),
        ("following_up", "Following Up"),
        ("progressing", "User Reports Progress"),
        ("resolved", "Resolved"),
        ("deferred", "User Chose to Defer"),
        ("dropped", "User Chose to Drop"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="open_threads"
    )
    journey = models.ForeignKey(
        UserJourney,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="open_threads",
    )
    source_reflection = models.ForeignKey(
        DailyReflection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="detected_threads",
    )

    thread_type = models.CharField(max_length=20, choices=THREAD_TYPE_CHOICES)
    encrypted_summary = models.BinaryField()
    encrypted_original_context = models.BinaryField(null=True, blank=True)
    related_life_area = models.CharField(max_length=20, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    last_mentioned_at = models.DateTimeField(auto_now_add=True)
    last_followup_at = models.DateTimeField(null=True, blank=True)

    followup_after_days = models.PositiveIntegerField(default=3)
    followup_count = models.PositiveIntegerField(default=0)
    max_followups = models.PositiveIntegerField(default=3)
    skip_count = models.PositiveIntegerField(default=0)

    resolved_at = models.DateTimeField(null=True, blank=True)
    encrypted_resolution_note = models.BinaryField(null=True, blank=True)

    class Meta:
        db_table = "open_threads"
        ordering = ["-created_at"]
        verbose_name = "Open Thread"
        verbose_name_plural = "Open Threads"

    def __str__(self):
        return f"OpenThread({self.id}) - {self.thread_type} ({self.status})"

    def set_summary(self, content: str):
        """Encrypt and store thread summary."""
        self.encrypted_summary = encrypt_content(content, self.user.encryption_key_salt)

    def get_summary(self) -> str:
        """Decrypt and return thread summary."""
        if not self.encrypted_summary:
            return ""
        return decrypt_content(
            bytes(self.encrypted_summary), self.user.encryption_key_salt
        )

    def set_original_context(self, content: str):
        """Encrypt and store original context."""
        if content:
            self.encrypted_original_context = encrypt_content(
                content, self.user.encryption_key_salt
            )

    def get_original_context(self) -> str:
        """Decrypt and return original context."""
        if not self.encrypted_original_context:
            return ""
        return decrypt_content(
            bytes(self.encrypted_original_context), self.user.encryption_key_salt
        )

    def set_resolution_note(self, content: str):
        """Encrypt and store resolution note."""
        if content:
            self.encrypted_resolution_note = encrypt_content(
                content, self.user.encryption_key_salt
            )

    def get_resolution_note(self) -> str:
        """Decrypt and return resolution note."""
        if not self.encrypted_resolution_note:
            return ""
        return decrypt_content(
            bytes(self.encrypted_resolution_note), self.user.encryption_key_salt
        )

    @property
    def days_since_mentioned(self):
        return (timezone.now() - self.last_mentioned_at).days

    @property
    def needs_followup(self):
        """Check if this thread needs a follow-up prompt."""
        if self.status not in ["open", "following_up"]:
            return False
        if self.followup_count >= self.max_followups:
            return False
        if self.skip_count >= 3:
            return False
        return self.days_since_mentioned >= self.followup_after_days

    def mark_mentioned(self):
        """Update last_mentioned_at when user references this thread."""
        self.last_mentioned_at = timezone.now()
        self.save(update_fields=["last_mentioned_at"])

    def record_followup(self):
        """Record that a follow-up was shown."""
        self.followup_count += 1
        self.last_followup_at = timezone.now()
        self.status = "following_up"
        self.save(update_fields=["followup_count", "last_followup_at", "status"])

    def record_skip(self):
        """Record that user skipped the follow-up."""
        self.skip_count += 1
        if self.skip_count >= 3:
            self.status = "deferred"
        self.save(update_fields=["skip_count", "status"])

    def mark_resolved(self, resolution_note: str = ""):
        """Mark thread as resolved."""
        self.status = "resolved"
        self.resolved_at = timezone.now()
        if resolution_note:
            self.set_resolution_note(resolution_note)
        self.save()

    def mark_progressing(self):
        """Mark thread as progressing (user reports improvement)."""
        self.status = "progressing"
        self.last_mentioned_at = timezone.now()
        self.save(update_fields=["status", "last_mentioned_at"])

    def defer(self, days: int = 14):
        """Defer thread for specified days."""
        self.status = "deferred"
        self.followup_after_days = days
        self.last_mentioned_at = timezone.now()
        self.save(update_fields=["status", "followup_after_days", "last_mentioned_at"])


class ThreadPrompt(models.Model):
    """
    Quick check-in prompts shown to user during journal entry.
    Tracks responses to thread follow-ups.
    """

    RESPONSE_CHOICES = [
        ("better", "Better"),
        ("same", "Same"),
        ("worse", "Worse"),
        ("yes", "Yes"),
        ("no", "No"),
        ("skipped", "Skipped"),
        ("resolved", "Resolved"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(
        OpenThread, on_delete=models.CASCADE, related_name="prompts"
    )
    reflection = models.ForeignKey(
        DailyReflection, on_delete=models.CASCADE, related_name="thread_prompts"
    )

    prompt_text = models.CharField(max_length=200)
    response = models.CharField(
        max_length=20, choices=RESPONSE_CHOICES, null=True, blank=True
    )

    expanded = models.BooleanField(default=False)
    encrypted_expanded_response = models.BinaryField(null=True, blank=True)

    shown_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "thread_prompts"
        ordering = ["-shown_at"]
        verbose_name = "Thread Prompt"
        verbose_name_plural = "Thread Prompts"

    def __str__(self):
        return f"{self.thread} - {self.response or 'pending'}"

    def set_expanded_response(self, content: str):
        """Encrypt and store expanded response."""
        if content:
            self.encrypted_expanded_response = encrypt_content(
                content, self.thread.user.encryption_key_salt
            )

    def get_expanded_response(self) -> str:
        """Decrypt and return expanded response."""
        if not self.encrypted_expanded_response:
            return ""
        return decrypt_content(
            bytes(self.encrypted_expanded_response),
            self.thread.user.encryption_key_salt,
        )

    def record_response(self, response: str, expanded_text: str = ""):
        """Record user's response to the prompt."""
        self.response = response
        self.responded_at = timezone.now()

        if expanded_text:
            self.expanded = True
            self.set_expanded_response(expanded_text)

        self.save()

        # Update thread based on response
        if response == "better":
            self.thread.mark_progressing()
        elif response == "resolved":
            self.thread.mark_resolved()
        elif response == "skipped":
            self.thread.record_skip()
        elif response in ["same", "worse", "yes", "no"]:
            self.thread.mark_mentioned()


class FocusIntention(models.Model):
    """
    User's focus intention for a specific time period (day, week, month).
    The AI uses this to curate relevant scripture passages and devotional content.
    """

    PERIOD_CHOICES = [
        ("day", "Daily"),
        ("week", "Weekly"),
        ("month", "Monthly"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("expired", "Expired"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="focus_intentions",
    )
    journey = models.ForeignKey(
        UserJourney,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="focus_intentions",
    )

    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()

    encrypted_intention = models.BinaryField()
    themes = models.JSONField(
        default=list, help_text="AI-extracted themes from intention"
    )
    related_life_areas = models.JSONField(default=list, help_text="Life area codes")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    passages_generated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "focus_intentions"
        ordering = ["-period_start"]
        verbose_name = "Focus Intention"
        verbose_name_plural = "Focus Intentions"

    def __str__(self):
        return f"FocusIntention({self.id}) - {self.period_type} ({self.period_start})"

    def set_intention(self, content: str):
        """Encrypt and store intention content."""
        self.encrypted_intention = encrypt_content(
            content, self.user.encryption_key_salt
        )

    def get_intention(self) -> str:
        """Decrypt and return intention content."""
        if not self.encrypted_intention:
            return ""
        return decrypt_content(
            bytes(self.encrypted_intention), self.user.encryption_key_salt
        )

    @property
    def intention_text(self):
        return self.get_intention()

    @property
    def is_active(self):
        today = timezone.now().date()
        return self.status == "active" and self.period_start <= today <= self.period_end

    def mark_completed(self):
        """Mark intention as completed."""
        self.status = "completed"
        self.save(update_fields=["status", "updated_at"])

    def check_expiration(self):
        """Check and update status if expired."""
        if self.status == "active" and timezone.now().date() > self.period_end:
            self.status = "expired"
            self.save(update_fields=["status", "updated_at"])
            return True
        return False


class DevotionalPassage(models.Model):
    """
    AI-curated scripture passage with stylized quote and reflection prompts.
    Linked to a focus intention for contextual relevance.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    focus_intention = models.ForeignKey(
        FocusIntention, on_delete=models.CASCADE, related_name="passages"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="devotional_passages",
    )

    sequence_number = models.PositiveIntegerField(default=1)
    scheduled_date = models.DateField()

    scripture_reference = models.CharField(max_length=200)
    scripture_text = models.TextField()
    translation = models.CharField(max_length=20, default="NIV")

    stylized_quote = models.TextField(help_text="Formatted quote for display")
    context_note = models.TextField(blank=True, help_text="Historical/cultural context")
    connection_to_focus = models.TextField(help_text="How this relates to user's focus")

    reflection_prompts = models.JSONField(
        default=list, help_text="Questions for reflection"
    )
    application_suggestions = models.JSONField(
        default=list, help_text="Practical applications"
    )

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    encrypted_user_reflection = models.BinaryField(null=True, blank=True)
    reflection_saved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "devotional_passages"
        ordering = ["scheduled_date", "sequence_number"]
        unique_together = ["focus_intention", "sequence_number"]
        verbose_name = "Devotional Passage"
        verbose_name_plural = "Devotional Passages"

    def __str__(self):
        return f"{self.scripture_reference} - {self.scheduled_date}"

    def set_user_reflection(self, content: str):
        """Encrypt and store user's reflection on this passage."""
        if content:
            self.encrypted_user_reflection = encrypt_content(
                content, self.user.encryption_key_salt
            )
            self.reflection_saved_at = timezone.now()

    def get_user_reflection(self) -> str:
        """Decrypt and return user's reflection."""
        if not self.encrypted_user_reflection:
            return ""
        return decrypt_content(
            bytes(self.encrypted_user_reflection), self.user.encryption_key_salt
        )

    def mark_read(self):
        """Mark passage as read."""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at"])

    @property
    def user_reflection_text(self):
        return self.get_user_reflection()


class StudyGuideSession(models.Model):
    """
    Persistent study tracker for AI-generated deep-dive guides.
    """

    SOURCE_TYPE_CHOICES = [
        ("devotional_passage", "Devotional Passage"),
        ("journal_entry", "Journal Entry"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("archived", "Archived"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="study_guide_sessions",
    )

    source_type = models.CharField(max_length=30, choices=SOURCE_TYPE_CHOICES)
    source_reference = models.CharField(max_length=255)
    source_passage = models.ForeignKey(
        DevotionalPassage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="study_sessions",
    )
    source_journal_entry = models.ForeignKey(
        "journal.JournalEntry",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="study_sessions",
    )

    guide_data = models.JSONField(default=dict)
    completed_days = models.JSONField(default=list, blank=True)
    day_notes = models.JSONField(default=dict, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "study_guide_sessions"
        ordering = ["-last_activity_at", "-started_at"]
        indexes = [
            models.Index(
                fields=["user", "status"], name="study_sessions_user_status_idx"
            ),
            models.Index(
                fields=["user", "source_type"], name="study_sessions_user_source_idx"
            ),
        ]

    def __str__(self):
        return f"StudyGuideSession({self.id}) - {self.source_reference}"

    @property
    def total_days(self):
        study_plan = (
            self.guide_data.get("study_plan", [])
            if isinstance(self.guide_data, dict)
            else []
        )
        if not isinstance(study_plan, list):
            return 0
        return len(study_plan)

    @property
    def progress_percentage(self):
        total = self.total_days
        if total == 0:
            return 0
        completed = {
            int(day)
            for day in (self.completed_days or [])
            if isinstance(day, int) or (isinstance(day, str) and day.isdigit())
        }
        completed_in_range = len([day for day in completed if 1 <= day <= total])
        return round((completed_in_range / total) * 100, 1)

    @property
    def next_day(self):
        total = self.total_days
        if total == 0:
            return None
        completed = {
            int(day)
            for day in (self.completed_days or [])
            if isinstance(day, int) or (isinstance(day, str) and day.isdigit())
        }
        for day in range(1, total + 1):
            if day not in completed:
                return day
        return None

    def mark_day(self, day: int, completed: bool = True, note: str = ""):
        completed_set = {
            int(value)
            for value in (self.completed_days or [])
            if isinstance(value, int) or (isinstance(value, str) and value.isdigit())
        }

        if completed:
            completed_set.add(day)
        else:
            completed_set.discard(day)

        notes = dict(self.day_notes or {})
        if note:
            notes[str(day)] = note
        elif not completed:
            notes.pop(str(day), None)

        self.completed_days = sorted(completed_set)
        self.day_notes = notes

        total = self.total_days
        done_count = (
            len([value for value in completed_set if 1 <= value <= total])
            if total
            else 0
        )
        if total and done_count >= total:
            self.status = "completed"
            if not self.completed_at:
                self.completed_at = timezone.now()
        elif self.status == "completed":
            self.status = "active"
            self.completed_at = None

        self.save()


class DevotionalAudit(models.Model):
    """
    Audit trail for AI-generated devotional content.
    Tracks accuracy, user feedback, and manual reviews.
    """

    AUDIT_STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("verified", "Verified Accurate"),
        ("flagged", "Flagged for Issues"),
        ("corrected", "Manually Corrected"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    devotional_passage = models.OneToOneField(
        DevotionalPassage, on_delete=models.CASCADE, related_name="audit"
    )

    # Automated accuracy checks
    scripture_accuracy_score = models.FloatField(
        null=True,
        blank=True,
        help_text="0.0-1.0 score from automated scripture verification",
    )
    scripture_warnings = models.JSONField(
        default=list, help_text="Warnings from scripture verification"
    )

    # Content quality metrics
    relevance_score = models.FloatField(
        null=True,
        blank=True,
        help_text="0.0-1.0 score for relevance to user's intention",
    )
    theological_accuracy = models.BooleanField(
        null=True, help_text="Manual review of theological accuracy"
    )

    # User feedback
    user_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="User rating 1-5",
    )
    user_feedback = models.TextField(blank=True)
    reported_issue = models.TextField(blank=True)

    # Manual review
    audit_status = models.CharField(
        max_length=20, choices=AUDIT_STATUS_CHOICES, default="pending"
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="devotional_reviews",
    )
    review_notes = models.TextField(blank=True)
    corrected_content = models.JSONField(
        null=True, blank=True, help_text="Manually corrected devotional content"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "devotional_audits"
        ordering = ["-created_at"]
        verbose_name = "Devotional Audit"
        verbose_name_plural = "Devotional Audits"

    def __str__(self):
        return f"Audit for {self.devotional_passage.scripture_reference} - {self.audit_status}"

    def calculate_overall_score(self):
        """Calculate overall quality score based on available metrics."""
        scores = []
        if self.scripture_accuracy_score is not None:
            scores.append(self.scripture_accuracy_score)
        if self.relevance_score is not None:
            scores.append(self.relevance_score)
        if self.user_rating is not None:
            # Normalize user rating to 0-1 scale
            scores.append((self.user_rating - 1) / 4)

        if scores:
            return sum(scores) / len(scores)
        return None

    def flag_for_review(self, reason: str):
        """Flag this devotional for manual review."""
        self.audit_status = "flagged"
        if reason:
            self.review_notes = f"Flagged: {reason}\n{self.review_notes}"
        self.save(update_fields=["audit_status", "review_notes"])


class ScriptureInsight(models.Model):
    """Cache for AI-generated scripture insights to avoid regenerating the same content."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scripture_insights",
    )
    scripture_reference = models.CharField(max_length=200)
    translation = models.CharField(max_length=20)
    theme = models.CharField(max_length=500, blank=True, null=True)
    focus_intention = models.CharField(max_length=500, blank=True, null=True)
    focus_themes = models.JSONField(default=list, blank=True, null=True)
    insight_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    accessed_at = models.DateTimeField(auto_now=True)
    access_count = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["user", "scripture_reference", "translation", "theme"],
                name="reflections_user_ref_idx",
            ),
            models.Index(
                fields=["user", "scripture_reference", "focus_intention"],
                name="reflections_user_focus_idx",
            ),
        ]

    def __str__(self):
        return f"DevotionalPassage({self.id}) - {self.scripture_reference}"

    def increment_access(self):
        """Increment access count when insight is retrieved from cache."""
        self.access_count += 1
        self.save(update_fields=["access_count", "accessed_at"])

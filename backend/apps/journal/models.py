"""
Journal entry models with encryption.
"""
import uuid

from django.conf import settings
from django.db import models

from shared.encryption import encrypt_content, decrypt_content


class JournalEntry(models.Model):
    """
    Encrypted journal entry tied to a user and optionally a reading plan day.
    """
    MOOD_CHOICES = [
        ('grateful', 'Grateful'),
        ('struggling', 'Struggling'),
        ('convicted', 'Convicted'),
        ('peaceful', 'Peaceful'),
        ('fired_up', 'Fired Up'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='journal_entries'
    )
    date = models.DateField()
    plan_enrollment = models.ForeignKey(
        'plans.UserPlanEnrollment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='journal_entries'
    )
    plan_day = models.ForeignKey(
        'plans.ReadingPlanDay',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='journal_entries'
    )
    focus_intention = models.ForeignKey(
        'reflections.FocusIntention',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='journal_entries'
    )
    focus_themes = models.JSONField(default=list, blank=True)
    encrypted_content = models.BinaryField()
    reflection_prompts_used = models.JSONField(default=list, blank=True)
    mood_tag = models.CharField(max_length=20, choices=MOOD_CHOICES, blank=True)
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'journal_entries'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"JournalEntry({self.id}) - {self.date}"

    def set_content(self, content: str):
        """Encrypt and store content."""
        self.encrypted_content = encrypt_content(content, self.user.encryption_key_salt)

    def get_content(self) -> str:
        """Decrypt and return content."""
        if not self.encrypted_content:
            return ""
        return decrypt_content(bytes(self.encrypted_content), self.user.encryption_key_salt)

    @property
    def content(self):
        return self.get_content()

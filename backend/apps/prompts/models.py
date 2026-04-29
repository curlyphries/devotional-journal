"""
Models for prompt generation and exploration history.
"""
import uuid
from django.conf import settings
from django.db import models


class ExplorationHistory(models.Model):
    """
    Persists each AI Bible exploration so users can revisit past searches.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='explorations',
    )
    user_input = models.TextField(help_text='The freeform text the user submitted')
    summary = models.TextField(blank=True, default='')
    category = models.CharField(max_length=30, blank=True, default='general')
    passages = models.JSONField(
        default=list,
        help_text='Hydrated passage objects with reference, text, and reason',
    )
    prompts = models.JSONField(
        default=list,
        help_text='AI-generated reflection prompts',
    )
    plans = models.JSONField(
        default=list,
        help_text='Recommended reading plans at the time of search',
    )
    is_bookmarked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exploration_history'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} — {self.user_input[:60]}"

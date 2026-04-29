"""
Streak tracking models.
"""
from django.conf import settings
from django.db import models
from django.utils import timezone


class UserStreak(models.Model):
    """
    Tracks user's journaling streak.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='streak'
    )
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_entry_date = models.DateField(null=True, blank=True)
    total_entries = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'user_streaks'

    def __str__(self):
        return f"UserStreak({self.id}) - {self.current_streak} day streak"

    def record_entry(self, entry_date=None):
        """
        Record a journal entry and update streak.
        """
        if entry_date is None:
            entry_date = timezone.now().date()

        self.total_entries += 1

        if self.last_entry_date is None:
            self.current_streak = 1
        elif entry_date == self.last_entry_date:
            pass
        elif (entry_date - self.last_entry_date).days == 1:
            self.current_streak += 1
        elif (entry_date - self.last_entry_date).days > 1:
            self.current_streak = 1

        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        self.last_entry_date = entry_date
        self.save()

    @classmethod
    def get_or_create_for_user(cls, user):
        streak, _ = cls.objects.get_or_create(user=user)
        return streak

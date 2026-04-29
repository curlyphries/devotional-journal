"""
Group and church management models (Phase 2).
"""
import secrets
import uuid

from django.conf import settings
from django.db import models


def generate_invite_code():
    """Generate a short alphanumeric invite code."""
    return secrets.token_urlsafe(6)[:8].upper()


class Group(models.Model):
    """
    A men's group for shared reading plans and accountability.
    """
    TIER_CHOICES = [
        ('free', 'Free'),
        ('church', 'Church'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_groups'
    )
    invite_code = models.CharField(
        max_length=8,
        unique=True,
        default=generate_invite_code
    )
    active_plan = models.ForeignKey(
        'plans.ReadingPlan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='active_groups'
    )
    max_members = models.PositiveIntegerField(default=25)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default='free')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'groups'

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.memberships.filter(is_active=True).count()

    def regenerate_invite_code(self):
        self.invite_code = generate_invite_code()
        self.save(update_fields=['invite_code'])


class GroupMembership(models.Model):
    """
    Tracks user membership in a group.
    """
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('leader', 'Leader'),
        ('admin', 'Admin'),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='group_memberships'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'group_memberships'
        unique_together = ['group', 'user']

    def __str__(self):
        return f"GroupMembership({self.id}) - {self.group.name} ({self.role})"

    @property
    def is_leader(self):
        return self.role in ('leader', 'admin')


class GroupEngagementSnapshot(models.Model):
    """
    Daily aggregate engagement metrics for a group.
    Privacy: Only aggregate data, never individual member details.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='engagement_snapshots')
    date = models.DateField()
    total_members = models.PositiveIntegerField()
    members_active_today = models.PositiveIntegerField()
    avg_streak = models.FloatField(default=0.0)
    plan_completion_pct = models.FloatField(default=0.0)

    class Meta:
        db_table = 'group_engagement_snapshots'
        unique_together = ['group', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.group.name} - {self.date}"

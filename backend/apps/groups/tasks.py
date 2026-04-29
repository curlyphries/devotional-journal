"""
Celery tasks for group engagement tracking.
"""

from celery import shared_task
from django.db.models import Avg
from django.utils import timezone


@shared_task
def calculate_daily_engagement():
    """
    Calculate and store daily engagement snapshots for all groups.
    Run this task daily via Celery Beat.
    """
    from apps.groups.models import Group, GroupEngagementSnapshot, GroupMembership
    from apps.journal.models import JournalEntry
    from apps.streaks.models import UserStreak

    today = timezone.now().date()

    for group in Group.objects.all():
        active_memberships = GroupMembership.objects.filter(
            group=group, is_active=True
        ).select_related("user")

        member_ids = [m.user_id for m in active_memberships]
        total_members = len(member_ids)

        if total_members == 0:
            continue

        members_active_today = (
            JournalEntry.objects.filter(user_id__in=member_ids, date=today)
            .values("user_id")
            .distinct()
            .count()
        )

        avg_streak = (
            UserStreak.objects.filter(user_id__in=member_ids).aggregate(
                avg=Avg("current_streak")
            )["avg"]
            or 0.0
        )

        plan_completion_pct = 0.0
        if group.active_plan:
            from apps.plans.models import UserPlanEnrollment

            enrollments = UserPlanEnrollment.objects.filter(
                user_id__in=member_ids, plan=group.active_plan, is_active=True
            )
            if enrollments.exists():
                total_progress = sum(e.progress_percentage for e in enrollments)
                plan_completion_pct = total_progress / enrollments.count()

        GroupEngagementSnapshot.objects.update_or_create(
            group=group,
            date=today,
            defaults={
                "total_members": total_members,
                "members_active_today": members_active_today,
                "avg_streak": round(avg_streak, 1),
                "plan_completion_pct": round(plan_completion_pct, 1),
            },
        )

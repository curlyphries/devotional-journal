"""
Celery tasks for the Life Reflection system.

Scheduled tasks:
- Daily: Thread detection scan (lightweight)
- Weekly (Sunday): Full crew review generation
- Monthly (1st): Monthly recap generation
- Weekly: Alignment trend computation
"""

import logging
from datetime import date, timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task(name="reflections.compute_weekly_trends")
def compute_weekly_trends():
    """
    Compute weekly alignment trends for all users with reflections.
    Runs every Monday to summarize the previous week.
    """
    from .models import AlignmentTrend, DailyReflection

    logger.info("Starting weekly trend computation")

    # Get the previous week's date range
    today = date.today()
    week_end = today - timedelta(days=today.weekday())  # Last Monday
    week_start = week_end - timedelta(days=7)

    # Get all users with reflections in the past week
    users_with_reflections = (
        DailyReflection.objects.filter(date__gte=week_start, date__lt=week_end)
        .values_list("user_id", flat=True)
        .distinct()
    )

    trends_created = 0

    for user_id in users_with_reflections:
        reflections = DailyReflection.objects.filter(
            user_id=user_id, date__gte=week_start, date__lt=week_end
        )

        if not reflections.exists():
            continue

        # Calculate area averages
        area_averages = {}
        area_scores_list = {}

        for reflection in reflections:
            for area, score in reflection.area_scores.items():
                if area not in area_scores_list:
                    area_scores_list[area] = []
                area_scores_list[area].append(score)

        for area, scores in area_scores_list.items():
            area_averages[area] = round(sum(scores) / len(scores), 2) if scores else 0

        # Calculate deltas from previous week
        previous_trend = AlignmentTrend.objects.filter(
            user_id=user_id, period_type="week", period_end=week_start
        ).first()

        area_deltas = {}
        if previous_trend:
            for area, avg in area_averages.items():
                prev_avg = previous_trend.area_averages.get(area, avg)
                area_deltas[area] = round(avg - prev_avg, 2)

        # Calculate overall average
        overall_average = (
            round(sum(area_averages.values()) / len(area_averages), 2)
            if area_averages
            else 0
        )

        # Create or update trend
        trend, created = AlignmentTrend.objects.update_or_create(
            user_id=user_id,
            period_type="week",
            period_start=week_start,
            defaults={
                "period_end": week_end,
                "area_averages": area_averages,
                "area_deltas": area_deltas,
                "overall_average": overall_average,
                "reflection_count": reflections.count(),
            },
        )

        if created:
            trends_created += 1

    logger.info(
        f"Weekly trend computation complete. Created {trends_created} new trends."
    )
    return {
        "trends_created": trends_created,
        "users_processed": len(users_with_reflections),
    }


@shared_task(name="reflections.compute_monthly_trends")
def compute_monthly_trends():
    """
    Compute monthly alignment trends for all users.
    Runs on the 1st of each month.
    """
    from .models import AlignmentTrend, DailyReflection

    logger.info("Starting monthly trend computation")

    today = date.today()
    # Previous month
    if today.month == 1:
        month_start = date(today.year - 1, 12, 1)
    else:
        month_start = date(today.year, today.month - 1, 1)
    month_end = date(today.year, today.month, 1)

    users_with_reflections = (
        DailyReflection.objects.filter(date__gte=month_start, date__lt=month_end)
        .values_list("user_id", flat=True)
        .distinct()
    )

    trends_created = 0

    for user_id in users_with_reflections:
        reflections = DailyReflection.objects.filter(
            user_id=user_id, date__gte=month_start, date__lt=month_end
        )

        if not reflections.exists():
            continue

        # Calculate area averages
        area_averages = {}
        area_scores_list = {}

        for reflection in reflections:
            for area, score in reflection.area_scores.items():
                if area not in area_scores_list:
                    area_scores_list[area] = []
                area_scores_list[area].append(score)

        for area, scores in area_scores_list.items():
            area_averages[area] = round(sum(scores) / len(scores), 2) if scores else 0

        # Calculate deltas from previous month
        previous_trend = AlignmentTrend.objects.filter(
            user_id=user_id, period_type="month", period_end=month_start
        ).first()

        area_deltas = {}
        if previous_trend:
            for area, avg in area_averages.items():
                prev_avg = previous_trend.area_averages.get(area, avg)
                area_deltas[area] = round(avg - prev_avg, 2)

        overall_average = (
            round(sum(area_averages.values()) / len(area_averages), 2)
            if area_averages
            else 0
        )

        trend, created = AlignmentTrend.objects.update_or_create(
            user_id=user_id,
            period_type="month",
            period_start=month_start,
            defaults={
                "period_end": month_end,
                "area_averages": area_averages,
                "area_deltas": area_deltas,
                "overall_average": overall_average,
                "reflection_count": reflections.count(),
            },
        )

        if created:
            trends_created += 1

    logger.info(
        f"Monthly trend computation complete. Created {trends_created} new trends."
    )
    return {
        "trends_created": trends_created,
        "users_processed": len(users_with_reflections),
    }


def _generate_reviews(period_type: str) -> dict:
    """Generate and store a review for everyone who journaled in the period."""
    from django.contrib.auth import get_user_model

    from apps.journal.models import JournalEntry
    from shared.errors import AppError

    from .reviews import PERIOD_DAYS, generate_review

    since = date.today() - timedelta(days=PERIOD_DAYS[period_type] - 1)
    user_ids = (
        JournalEntry.objects.filter(date__gte=since)
        .values_list("user_id", flat=True)
        .distinct()
    )
    generated = skipped = errors = 0
    for user in get_user_model().objects.filter(id__in=list(user_ids), is_active=True):
        try:
            generate_review(user, period_type)
            generated += 1
        except AppError as exc:
            # Expected: AI not available / not allowed for this person. The
            # code says why; the person can generate it on demand later.
            logger.info(
                "Skipped %s review for user %s: %s", period_type, user.id, exc.code
            )
            skipped += 1
        except Exception:
            logger.exception(
                "Failed to generate %s review for user %s", period_type, user.id
            )
            errors += 1
    logger.info(
        "%s reviews complete. Generated: %d, skipped: %d, errors: %d",
        period_type,
        generated,
        skipped,
        errors,
    )
    return {"reviews_generated": generated, "skipped": skipped, "errors": errors}


@shared_task(name="reflections.generate_weekly_reviews")
def generate_weekly_reviews():
    """Generate and store weekly growth reviews. Runs every Sunday evening."""
    return _generate_reviews("week")


@shared_task(name="reflections.generate_monthly_recaps")
def generate_monthly_recaps():
    """Generate and store monthly growth reviews. Runs on the 1st of each month."""
    return _generate_reviews("month")


@shared_task(name="reflections.process_thread_followups")
def process_thread_followups():
    """
    Check for threads needing follow-up and prepare prompts.
    Runs daily in the evening before typical reflection time.
    """
    from .models import OpenThread
    from .services import get_thread_followup_service

    logger.info("Starting thread follow-up processing")

    # Get all threads needing follow-up
    threads_needing_followup = OpenThread.objects.filter(
        status__in=["open", "following_up"],
    ).select_related("user")

    threads_processed = 0
    auto_deferred = 0

    get_thread_followup_service()

    for thread in threads_needing_followup:
        # Check if thread needs follow-up based on days since mentioned
        if not thread.needs_followup:
            continue

        # Auto-defer threads with too many skips
        if thread.skip_count >= 3:
            thread.status = "deferred"
            thread.save(update_fields=["status"])
            auto_deferred += 1
            logger.info(f"Auto-deferred thread {thread.id} due to skip count")
            continue

        # Auto-defer threads with max follow-ups reached
        if thread.followup_count >= thread.max_followups:
            thread.status = "deferred"
            thread.save(update_fields=["status"])
            auto_deferred += 1
            logger.info(f"Auto-deferred thread {thread.id} due to max follow-ups")
            continue

        # Mark as following_up if still open
        if thread.status == "open":
            thread.status = "following_up"
            thread.save(update_fields=["status"])

        threads_processed += 1

    logger.info(
        f"Thread follow-up processing complete. Processed: {threads_processed}, Auto-deferred: {auto_deferred}"
    )
    return {"threads_processed": threads_processed, "auto_deferred": auto_deferred}


@shared_task(name="reflections.advance_journey_days")
def advance_journey_days():
    """
    Advance the day counter for active journeys.
    Runs daily at midnight.
    """
    from .models import DailyReflection, UserJourney

    logger.info("Starting journey day advancement")

    yesterday = date.today() - timedelta(days=1)

    active_journeys = UserJourney.objects.filter(status="active")

    advanced = 0
    completed = 0

    for journey in active_journeys:
        # Check if user had a reflection yesterday
        had_reflection = DailyReflection.objects.filter(
            user=journey.user, date=yesterday
        ).exists()

        if had_reflection:
            journey.current_day += 1

            # Check if journey is complete
            if journey.current_day >= journey.duration_days:
                journey.status = "completed"
                journey.completed_at = timezone.now()
                completed += 1
                logger.info(
                    f"Journey {journey.id} completed for user {journey.user_id}"
                )

            journey.save()
            advanced += 1

    logger.info(
        f"Journey advancement complete. Advanced: {advanced}, Completed: {completed}"
    )
    return {"advanced": advanced, "completed": completed}


@shared_task(name="reflections.cleanup_old_trends")
def cleanup_old_trends():
    """
    Clean up old alignment trends to prevent database bloat.
    Keeps last 12 weeks and 12 months of trends.
    Runs monthly.
    """
    from .models import AlignmentTrend

    logger.info("Starting trend cleanup")

    today = date.today()

    # Keep last 12 weeks
    weekly_cutoff = today - timedelta(weeks=12)
    weekly_deleted = AlignmentTrend.objects.filter(
        period_type="week", period_end__lt=weekly_cutoff
    ).delete()[0]

    # Keep last 12 months
    monthly_cutoff = today - timedelta(days=365)
    monthly_deleted = AlignmentTrend.objects.filter(
        period_type="month", period_end__lt=monthly_cutoff
    ).delete()[0]

    logger.info(
        f"Trend cleanup complete. Weekly deleted: {weekly_deleted}, Monthly deleted: {monthly_deleted}"
    )
    return {"weekly_deleted": weekly_deleted, "monthly_deleted": monthly_deleted}


@shared_task(name="reflections.health_check")
def health_check():
    """
    Health check task to verify the reflection system is working.
    """
    from .crew import get_crew
    from .models import LifeArea

    results = {
        "database": False,
        "crew": False,
        "life_areas": 0,
    }

    try:
        # Check database
        results["life_areas"] = LifeArea.objects.count()
        results["database"] = True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")

    try:
        # Check crew/Ollama
        crew = get_crew()
        health = crew.health_check()
        results["crew"] = health.get("status") == "healthy"
        results["crew_details"] = health
    except Exception as e:
        logger.error(f"Crew health check failed: {e}")

    logger.info(f"Health check results: {results}")
    return results


@shared_task(name="reflections.generate_daily_devotionals")
def generate_daily_devotionals():
    """
    Make sure every active focus intention has a passage for today.
    Runs every morning at 5 AM. Uses each person's own AI provider settings;
    the verse text comes from the Bible source, never from the model.
    """
    from shared.errors import AppError

    from .crew.agents import DevotionalCurator
    from .models import DevotionalPassage, FocusIntention
    from .serializers import create_devotional_passage

    logger.info("Starting daily devotional generation")

    today = date.today()
    active_intentions = FocusIntention.objects.filter(
        status="active", period_start__lte=today, period_end__gte=today
    ).select_related("user")

    devotionals_generated = skipped = errors = 0

    for intention in active_intentions:
        existing = DevotionalPassage.objects.filter(focus_intention=intention)
        if existing.filter(scheduled_date=today).exists():
            continue

        try:
            passages_data = DevotionalCurator(user=intention.user).curate_passages(
                intention=intention.get_intention(),
                period_type="day",
                themes=intention.themes,
                num_passages=1,
                avoid=list(existing.values_list("scripture_reference", flat=True)),
            )
            if not passages_data:
                skipped += 1
                continue

            last = existing.order_by("-sequence_number").first()
            create_devotional_passage(
                user=intention.user,
                focus_intention=intention,
                sequence_number=(last.sequence_number + 1) if last else 1,
                scheduled_date=today,
                data=passages_data[0],
            )
            if not intention.passages_generated:
                intention.passages_generated = True
                intention.save(update_fields=["passages_generated"])
            devotionals_generated += 1
        except AppError as exc:
            logger.info(
                "Skipped daily devotional for user %s: %s", intention.user_id, exc.code
            )
            skipped += 1
        except Exception:
            logger.exception(
                "Failed to generate daily devotional for user %s", intention.user_id
            )
            errors += 1

    logger.info(
        "Daily devotional generation complete. Generated: %d, skipped: %d, errors: %d",
        devotionals_generated,
        skipped,
        errors,
    )
    return {
        "devotionals_generated": devotionals_generated,
        "skipped": skipped,
        "errors": errors,
    }


@shared_task(name="reflections.audit_devotional_accuracy")
def audit_devotional_accuracy():
    """
    Re-check yesterday's devotional passages against the Bible source.

    Passage text is fetched from that source when the passage is created, so
    this is a safety net: it flags any stored passage whose text no longer
    matches (or whose reference cannot be found at all).
    """
    from difflib import SequenceMatcher

    from apps.bible.lookup import fetch_reference

    from .models import DevotionalAudit, DevotionalPassage

    logger.info("Starting devotional accuracy audit")

    yesterday = date.today() - timedelta(days=1)
    passages_to_audit = DevotionalPassage.objects.filter(
        created_at__date=yesterday, audit__isnull=True
    )[:100]

    audited = issues_found = 0

    for passage in passages_to_audit:
        try:
            audit, _created = DevotionalAudit.objects.get_or_create(
                devotional_passage=passage
            )
            source = fetch_reference(
                passage.scripture_reference, [passage.translation, "WEB", "KJV"]
            )
            if source is None:
                audit.scripture_accuracy_score = 0.0
                audit.scripture_warnings = [
                    "Reference could not be found in the Bible source"
                ]
                audit.audit_status = "flagged"
                issues_found += 1
            else:
                score = SequenceMatcher(
                    None, passage.scripture_text.strip(), source.text.strip()
                ).ratio()
                audit.scripture_accuracy_score = round(score, 4)
                if source.translation == passage.translation and score < 0.98:
                    audit.scripture_warnings = [
                        f"Stored text differs from {source.translation} "
                        f"({score * 100:.1f}% match)"
                    ]
                    audit.audit_status = "flagged"
                    issues_found += 1
                else:
                    audit.scripture_warnings = []
                    audit.audit_status = "verified"
            audit.save()
            audited += 1
        except Exception:
            logger.exception("Failed to audit passage %s", passage.id)

    logger.info(
        "Devotional accuracy audit complete. Audited: %d, Issues: %d",
        audited,
        issues_found,
    )
    return {"audited": audited, "issues_found": issues_found}

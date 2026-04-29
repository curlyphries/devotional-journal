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
from django.db.models import Avg
from django.utils import timezone

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task(name='reflections.compute_weekly_trends')
def compute_weekly_trends():
    """
    Compute weekly alignment trends for all users with reflections.
    Runs every Monday to summarize the previous week.
    """
    from .models import DailyReflection, AlignmentTrend, LifeArea
    
    logger.info("Starting weekly trend computation")
    
    # Get the previous week's date range
    today = date.today()
    week_end = today - timedelta(days=today.weekday())  # Last Monday
    week_start = week_end - timedelta(days=7)
    
    # Get all users with reflections in the past week
    users_with_reflections = DailyReflection.objects.filter(
        date__gte=week_start,
        date__lt=week_end
    ).values_list('user_id', flat=True).distinct()
    
    trends_created = 0
    
    for user_id in users_with_reflections:
        reflections = DailyReflection.objects.filter(
            user_id=user_id,
            date__gte=week_start,
            date__lt=week_end
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
            user_id=user_id,
            period_type='week',
            period_end=week_start
        ).first()
        
        area_deltas = {}
        if previous_trend:
            for area, avg in area_averages.items():
                prev_avg = previous_trend.area_averages.get(area, avg)
                area_deltas[area] = round(avg - prev_avg, 2)
        
        # Calculate overall average
        overall_average = round(
            sum(area_averages.values()) / len(area_averages), 2
        ) if area_averages else 0
        
        # Create or update trend
        trend, created = AlignmentTrend.objects.update_or_create(
            user_id=user_id,
            period_type='week',
            period_start=week_start,
            defaults={
                'period_end': week_end,
                'area_averages': area_averages,
                'area_deltas': area_deltas,
                'overall_average': overall_average,
                'reflection_count': reflections.count(),
            }
        )
        
        if created:
            trends_created += 1
    
    logger.info(f"Weekly trend computation complete. Created {trends_created} new trends.")
    return {'trends_created': trends_created, 'users_processed': len(users_with_reflections)}


@shared_task(name='reflections.compute_monthly_trends')
def compute_monthly_trends():
    """
    Compute monthly alignment trends for all users.
    Runs on the 1st of each month.
    """
    from .models import DailyReflection, AlignmentTrend
    
    logger.info("Starting monthly trend computation")
    
    today = date.today()
    # Previous month
    if today.month == 1:
        month_start = date(today.year - 1, 12, 1)
    else:
        month_start = date(today.year, today.month - 1, 1)
    month_end = date(today.year, today.month, 1)
    
    users_with_reflections = DailyReflection.objects.filter(
        date__gte=month_start,
        date__lt=month_end
    ).values_list('user_id', flat=True).distinct()
    
    trends_created = 0
    
    for user_id in users_with_reflections:
        reflections = DailyReflection.objects.filter(
            user_id=user_id,
            date__gte=month_start,
            date__lt=month_end
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
            user_id=user_id,
            period_type='month',
            period_end=month_start
        ).first()
        
        area_deltas = {}
        if previous_trend:
            for area, avg in area_averages.items():
                prev_avg = previous_trend.area_averages.get(area, avg)
                area_deltas[area] = round(avg - prev_avg, 2)
        
        overall_average = round(
            sum(area_averages.values()) / len(area_averages), 2
        ) if area_averages else 0
        
        trend, created = AlignmentTrend.objects.update_or_create(
            user_id=user_id,
            period_type='month',
            period_start=month_start,
            defaults={
                'period_end': month_end,
                'area_averages': area_averages,
                'area_deltas': area_deltas,
                'overall_average': overall_average,
                'reflection_count': reflections.count(),
            }
        )
        
        if created:
            trends_created += 1
    
    logger.info(f"Monthly trend computation complete. Created {trends_created} new trends.")
    return {'trends_created': trends_created, 'users_processed': len(users_with_reflections)}


@shared_task(name='reflections.generate_weekly_reviews')
def generate_weekly_reviews():
    """
    Generate weekly reviews for all active users.
    Runs every Sunday evening.
    """
    from .models import UserJourney
    from .crew import get_crew
    
    logger.info("Starting weekly review generation")
    
    # Get users with active journeys
    active_journeys = UserJourney.objects.filter(status='active').select_related('user')
    
    reviews_generated = 0
    errors = 0
    
    for journey in active_journeys:
        user = journey.user
        
        try:
            crew = get_crew(user)
            review = crew.generate_weekly_review(user)
            
            if review:
                # Store the review (could be in a new model or notification)
                # For now, we'll log it and could send as notification
                logger.info(f"Generated weekly review for user {user.id}")
                reviews_generated += 1
                
                # TODO: Send notification or store in WeeklyReview model
                # notification_service.send_weekly_review(user, review)
            else:
                logger.warning(f"Empty weekly review for user {user.id}")
                
        except Exception as e:
            logger.error(f"Failed to generate weekly review for user {user.id}: {e}")
            errors += 1
    
    logger.info(f"Weekly review generation complete. Generated: {reviews_generated}, Errors: {errors}")
    return {'reviews_generated': reviews_generated, 'errors': errors}


@shared_task(name='reflections.generate_monthly_recaps')
def generate_monthly_recaps():
    """
    Generate monthly recaps for all active users.
    Runs on the 1st of each month.
    """
    from .models import UserJourney
    from .crew import get_crew
    
    logger.info("Starting monthly recap generation")
    
    active_journeys = UserJourney.objects.filter(status='active').select_related('user')
    
    recaps_generated = 0
    errors = 0
    
    for journey in active_journeys:
        user = journey.user
        
        try:
            crew = get_crew(user)
            recap = crew.generate_monthly_recap(user)
            
            if recap:
                logger.info(f"Generated monthly recap for user {user.id}")
                recaps_generated += 1
                
                # TODO: Send notification or store in MonthlyRecap model
            else:
                logger.warning(f"Empty monthly recap for user {user.id}")
                
        except Exception as e:
            logger.error(f"Failed to generate monthly recap for user {user.id}: {e}")
            errors += 1
    
    logger.info(f"Monthly recap generation complete. Generated: {recaps_generated}, Errors: {errors}")
    return {'recaps_generated': recaps_generated, 'errors': errors}


@shared_task(name='reflections.process_thread_followups')
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
        status__in=['open', 'following_up'],
    ).select_related('user')
    
    threads_processed = 0
    auto_deferred = 0
    
    followup_service = get_thread_followup_service()
    
    for thread in threads_needing_followup:
        # Check if thread needs follow-up based on days since mentioned
        if not thread.needs_followup:
            continue
        
        # Auto-defer threads with too many skips
        if thread.skip_count >= 3:
            thread.status = 'deferred'
            thread.save(update_fields=['status'])
            auto_deferred += 1
            logger.info(f"Auto-deferred thread {thread.id} due to skip count")
            continue
        
        # Auto-defer threads with max follow-ups reached
        if thread.followup_count >= thread.max_followups:
            thread.status = 'deferred'
            thread.save(update_fields=['status'])
            auto_deferred += 1
            logger.info(f"Auto-deferred thread {thread.id} due to max follow-ups")
            continue
        
        # Mark as following_up if still open
        if thread.status == 'open':
            thread.status = 'following_up'
            thread.save(update_fields=['status'])
        
        threads_processed += 1
    
    logger.info(f"Thread follow-up processing complete. Processed: {threads_processed}, Auto-deferred: {auto_deferred}")
    return {'threads_processed': threads_processed, 'auto_deferred': auto_deferred}


@shared_task(name='reflections.advance_journey_days')
def advance_journey_days():
    """
    Advance the day counter for active journeys.
    Runs daily at midnight.
    """
    from .models import UserJourney, DailyReflection
    
    logger.info("Starting journey day advancement")
    
    yesterday = date.today() - timedelta(days=1)
    
    active_journeys = UserJourney.objects.filter(status='active')
    
    advanced = 0
    completed = 0
    
    for journey in active_journeys:
        # Check if user had a reflection yesterday
        had_reflection = DailyReflection.objects.filter(
            user=journey.user,
            date=yesterday
        ).exists()
        
        if had_reflection:
            journey.current_day += 1
            
            # Check if journey is complete
            if journey.current_day >= journey.duration_days:
                journey.status = 'completed'
                journey.completed_at = timezone.now()
                completed += 1
                logger.info(f"Journey {journey.id} completed for user {journey.user_id}")
            
            journey.save()
            advanced += 1
    
    logger.info(f"Journey advancement complete. Advanced: {advanced}, Completed: {completed}")
    return {'advanced': advanced, 'completed': completed}


@shared_task(name='reflections.cleanup_old_trends')
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
        period_type='week',
        period_end__lt=weekly_cutoff
    ).delete()[0]
    
    # Keep last 12 months
    monthly_cutoff = today - timedelta(days=365)
    monthly_deleted = AlignmentTrend.objects.filter(
        period_type='month',
        period_end__lt=monthly_cutoff
    ).delete()[0]
    
    logger.info(f"Trend cleanup complete. Weekly deleted: {weekly_deleted}, Monthly deleted: {monthly_deleted}")
    return {'weekly_deleted': weekly_deleted, 'monthly_deleted': monthly_deleted}


@shared_task(name='reflections.health_check')
def health_check():
    """
    Health check task to verify the reflection system is working.
    """
    from .models import LifeArea, DailyReflection
    from .crew import get_crew
    
    results = {
        'database': False,
        'crew': False,
        'life_areas': 0,
    }
    
    try:
        # Check database
        results['life_areas'] = LifeArea.objects.count()
        results['database'] = True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
    
    try:
        # Check crew/Ollama
        crew = get_crew()
        health = crew.health_check()
        results['crew'] = health.get('status') == 'healthy'
        results['crew_details'] = health
    except Exception as e:
        logger.error(f"Crew health check failed: {e}")
    
    logger.info(f"Health check results: {results}")
    return results


@shared_task(name='reflections.generate_daily_devotionals')
def generate_daily_devotionals():
    """
    Generate daily devotionals for users who have opted in to daily generation.
    Runs every morning at 5 AM.
    """
    from .models import FocusIntention, DevotionalPassage
    from .crew.agents import DevotionalCurator
    
    logger.info("Starting daily devotional generation")
    
    today = date.today()
    
    # Get all active focus intentions that need devotionals for today
    active_intentions = FocusIntention.objects.filter(
        status='active',
        period_start__lte=today,
        period_end__gte=today
    ).select_related('user')
    
    devotionals_generated = 0
    errors = 0
    
    curator = DevotionalCurator()
    
    for intention in active_intentions:
        # Check if devotional already exists for today
        existing = DevotionalPassage.objects.filter(
            focus_intention=intention,
            scheduled_date=today
        ).exists()
        
        if existing:
            continue
        
        try:
            # Generate devotional for today
            passages_data = curator.curate_passages(
                intention=intention.get_intention(),
                period_type='day',
                themes=intention.themes,
                num_passages=1
            )
            
            if passages_data:
                passage_data = passages_data[0]
                
                # Find the next sequence number
                last_passage = DevotionalPassage.objects.filter(
                    focus_intention=intention
                ).order_by('-sequence_number').first()
                
                next_sequence = (last_passage.sequence_number + 1) if last_passage else 1
                
                DevotionalPassage.objects.create(
                    focus_intention=intention,
                    user=intention.user,
                    sequence_number=next_sequence,
                    scheduled_date=today,
                    scripture_reference=passage_data.get('scripture_reference', 'Unknown'),
                    scripture_text=passage_data.get('scripture_text', ''),
                    translation=passage_data.get('translation', 'NIV'),
                    stylized_quote=passage_data.get('stylized_quote', ''),
                    context_note=passage_data.get('context_note', ''),
                    connection_to_focus=passage_data.get('connection_to_focus', ''),
                    reflection_prompts=passage_data.get('reflection_prompts', []),
                    application_suggestions=passage_data.get('application_suggestions', [])
                )
                
                devotionals_generated += 1
                logger.info(f"Generated daily devotional for user {intention.user.id}")
            
        except Exception as e:
            logger.error(f"Failed to generate daily devotional for user {intention.user.id}: {e}")
            errors += 1
    
    logger.info(f"Daily devotional generation complete. Generated: {devotionals_generated}, Errors: {errors}")
    return {'devotionals_generated': devotionals_generated, 'errors': errors}


@shared_task(name='reflections.audit_devotional_accuracy')
def audit_devotional_accuracy():
    """
    Audit the accuracy of generated devotionals by verifying scripture references.
    Runs daily at 11 PM.
    """
    from .models import DevotionalPassage, DevotionalAudit
    from ..bible.text_verifier import verify_verse
    import re
    
    logger.info("Starting devotional accuracy audit")
    
    # Get devotionals from the past day that haven't been audited
    yesterday = date.today() - timedelta(days=1)
    passages_to_audit = DevotionalPassage.objects.filter(
        created_at__date=yesterday
    ).exclude(
        audit__isnull=False  # Exclude already audited passages
    )[:100]  # Limit to 100 per run
    
    audited = 0
    issues_found = 0
    
    for passage in passages_to_audit:
        try:
            # Create or get audit record
            audit, created = DevotionalAudit.objects.get_or_create(
                devotional_passage=passage
            )
            
            # Parse scripture reference (e.g., "John 3:16" or "Romans 8:28-30")
            ref_pattern = r'(\w+)\s+(\d+):(\d+)(?:-(\d+))?'
            match = re.match(ref_pattern, passage.scripture_reference)
            
            if not match:
                logger.warning(f"Could not parse reference: {passage.scripture_reference}")
                audit.scripture_warnings = ["Could not parse scripture reference"]
                audit.audit_status = 'flagged'
                audit.save()
                continue
            
            book = match.group(1)
            chapter = int(match.group(2))
            verse_start = int(match.group(3))
            
            # Verify the scripture text
            verification = verify_verse(
                translation=passage.translation,
                book=book,
                chapter=chapter,
                verse=verse_start,
                text=passage.scripture_text
            )
            
            # Update audit record with verification results
            audit.scripture_accuracy_score = verification['overall_confidence']
            audit.scripture_warnings = verification['warnings']
            
            if not verification['overall_verified']:
                issues_found += 1
                audit.audit_status = 'flagged'
                logger.warning(
                    f"Accuracy issue in passage {passage.id}: "
                    f"{passage.scripture_reference} - "
                    f"Confidence: {verification['overall_confidence']}"
                )
            else:
                audit.audit_status = 'verified'
            
            # Calculate relevance score based on themes matching
            if passage.focus_intention and passage.focus_intention.themes:
                theme_words = set(' '.join(passage.focus_intention.themes).lower().split())
                content_words = set(passage.connection_to_focus.lower().split())
                if theme_words and content_words:
                    relevance = len(theme_words & content_words) / len(theme_words)
                    audit.relevance_score = min(1.0, relevance * 2)  # Scale up
            
            audit.save()
            audited += 1
            
        except Exception as e:
            logger.error(f"Failed to audit passage {passage.id}: {e}")
    
    logger.info(f"Devotional accuracy audit complete. Audited: {audited}, Issues: {issues_found}")
    return {'audited': audited, 'issues_found': issues_found}

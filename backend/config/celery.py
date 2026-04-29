"""
Celery configuration for Devotional Journal project.
"""
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('devotional_journal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Daily devotional generation - Every day at 5:00 AM
    'generate-daily-devotionals': {
        'task': 'reflections.generate_daily_devotionals',
        'schedule': crontab(hour=5, minute=0),
    },
    # Weekly trend computation - Monday 1:00 AM
    'compute-weekly-trends': {
        'task': 'reflections.compute_weekly_trends',
        'schedule': crontab(hour=1, minute=0, day_of_week=1),
    },
    # Monthly trend computation - 1st of month at 2:00 AM
    'compute-monthly-trends': {
        'task': 'reflections.compute_monthly_trends',
        'schedule': crontab(hour=2, minute=0, day_of_month=1),
    },
    # Weekly reviews - Sunday 7:00 PM
    'generate-weekly-reviews': {
        'task': 'reflections.generate_weekly_reviews',
        'schedule': crontab(hour=19, minute=0, day_of_week=0),
    },
    # Monthly recaps - 1st of month at 8:00 AM
    'generate-monthly-recaps': {
        'task': 'reflections.generate_monthly_recaps',
        'schedule': crontab(hour=8, minute=0, day_of_month=1),
    },
    # Thread follow-up processing - Daily at 5:00 PM
    'process-thread-followups': {
        'task': 'reflections.process_thread_followups',
        'schedule': crontab(hour=17, minute=0),
    },
    # Journey day advancement - Daily at midnight
    'advance-journey-days': {
        'task': 'reflections.advance_journey_days',
        'schedule': crontab(hour=0, minute=5),
    },
    # Trend cleanup - 1st of month at 3:00 AM
    'cleanup-old-trends': {
        'task': 'reflections.cleanup_old_trends',
        'schedule': crontab(hour=3, minute=0, day_of_month=1),
    },
    # Health check - Every 6 hours
    'reflections-health-check': {
        'task': 'reflections.health_check',
        'schedule': crontab(hour='*/6', minute=0),
    },
    # Devotional accuracy audit - Daily at 11:00 PM
    'audit-devotional-accuracy': {
        'task': 'reflections.audit_devotional_accuracy',
        'schedule': crontab(hour=23, minute=0),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

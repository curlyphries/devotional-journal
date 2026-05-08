"""
Signal handlers for the journal app.

Currently fires the asynchronous thread-detection task whenever a fresh
journal entry is created so the user never waits on the LLM during save.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import JournalEntry

logger = logging.getLogger(__name__)


@receiver(post_save, sender=JournalEntry)
def queue_thread_detection(sender, instance, created, **kwargs):
    if not created:
        return

    # Lazy-import the task so importing models in management commands /
    # migrations does not pull in Celery wiring.
    try:
        from apps.reflections.tasks import detect_threads_from_journal_entry

        detect_threads_from_journal_entry.delay(str(instance.id))
    except Exception as e:
        # Never let a detection-queue failure break the save path.
        logger.warning(
            f"queue_thread_detection: failed to queue task for entry "
            f"{instance.id}: {e}"
        )

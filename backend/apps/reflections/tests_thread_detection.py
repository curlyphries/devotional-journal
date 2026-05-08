"""
Tests for the journal-entry → thread detection flow.

We mock the LLM service rather than calling real Ollama/Anthropic so the tests
are hermetic and fast. Each test asserts one specific contract of the
`detect_threads_from_journal_entry` Celery task.
"""

from unittest.mock import patch

import pytest
from django.utils import timezone

from apps.journal.models import JournalEntry
from apps.reflections.models import OpenThread
from apps.reflections.tasks import detect_threads_from_journal_entry


def _make_entry(user, content: str) -> JournalEntry:
    entry = JournalEntry.objects.create(user=user, date=timezone.now().date())
    entry.set_content(content)
    entry.save()
    return entry


@pytest.mark.django_db
class TestDetectThreadsTask:
    def test_creates_threads_from_detected_items(self, user):
        text = (
            "I've been struggling with anxiety about work this week. "
            "I keep waking up at 3am and replaying tomorrow in my head. "
            "I'm going to start praying through Philippians 4 every morning."
        )
        entry = _make_entry(user, text)

        with patch(
            "apps.reflections.tasks.get_thread_detection_service"
        ) as mock_factory:
            service = mock_factory.return_value
            service.detect_threads.return_value = [
                {
                    "type": "struggle",
                    "summary": "anxiety about work",
                    "life_area": "work",
                    "quote": "struggling with anxiety about work",
                },
                {
                    "type": "commitment",
                    "summary": "pray Phil 4 each morning",
                    "life_area": "faith",
                    "quote": "going to start praying through Philippians 4",
                },
            ]

            result = detect_threads_from_journal_entry(str(entry.id))

        assert result["created"] == 2
        threads = list(OpenThread.objects.filter(user=user).order_by("created_at"))
        assert len(threads) == 2
        assert threads[0].thread_type == "struggle"
        assert threads[0].related_life_area == "work"
        assert threads[0].status == "open"
        # Encrypted summary round-trips correctly
        assert threads[0].get_summary() == "anxiety about work"
        assert threads[1].thread_type == "commitment"
        assert threads[1].get_summary() == "pray Phil 4 each morning"

    def test_skips_entries_under_30_words(self, user):
        entry = _make_entry(user, "Short entry. Nothing much to say today.")

        with patch(
            "apps.reflections.tasks.get_thread_detection_service"
        ) as mock_factory:
            result = detect_threads_from_journal_entry(str(entry.id))
            mock_factory.assert_not_called()

        assert result == {"created": 0, "skipped": "too_short", "words": 7}
        assert OpenThread.objects.filter(user=user).count() == 0

    def test_strips_metadata_block_before_detection(self, user):
        # Frontend prepends a metadata block in HTML comments. We must not pass
        # it to the LLM — the user's actual prose comes after the block.
        meta = (
            "<!-- DJ_META_START -->\n"
            '{"planTitle":"Anxiety","dayNumber":"2","passage":"Phil 4"}\n'
            "<!-- DJ_META_END -->\n\n"
        )
        body = (
            "I keep coming back to verse 6. "
            "It's hard to feel peace when my chest is tight at night. "
            "I want to actually try the supplication-with-thanksgiving thing this week."
        )
        entry = _make_entry(user, meta + body)

        captured = {}

        def fake_detect(reflection_text, struggle_note=""):
            captured["text"] = reflection_text
            return []

        with patch(
            "apps.reflections.tasks.get_thread_detection_service"
        ) as mock_factory:
            mock_factory.return_value.detect_threads.side_effect = fake_detect
            detect_threads_from_journal_entry(str(entry.id))

        assert "DJ_META_START" not in captured["text"]
        assert "Phil 4" not in captured["text"]
        assert "supplication" in captured["text"]

    def test_handles_missing_entry_gracefully(self, db):
        from uuid import uuid4

        result = detect_threads_from_journal_entry(str(uuid4()))
        assert result == {"created": 0, "skipped": "entry_missing"}

    def test_zero_threads_when_llm_returns_empty(self, user):
        entry = _make_entry(
            user,
            "I had a great day at work, kids were happy, made dinner, read a "
            "chapter of Mark before bed. Quiet and good, nothing pressing.",
        )

        with patch(
            "apps.reflections.tasks.get_thread_detection_service"
        ) as mock_factory:
            mock_factory.return_value.detect_threads.return_value = []
            result = detect_threads_from_journal_entry(str(entry.id))

        assert result["created"] == 0
        assert OpenThread.objects.filter(user=user).count() == 0

    def test_signal_fires_only_on_create(self, user):
        # Saving a fresh entry should queue exactly one detection task.
        # Saving the same entry again (update) should not.
        with patch("apps.reflections.tasks.detect_threads_from_journal_entry.delay") as mock_delay:
            entry = _make_entry(
                user,
                "I've been wrestling with how to talk to my dad about money. "
                "He's still bitter about something from years ago and it leaks out.",
            )
            assert mock_delay.call_count == 1
            assert mock_delay.call_args[0][0] == str(entry.id)

            # Update path
            entry.set_content("Edited.")
            entry.save()
            assert mock_delay.call_count == 1  # still 1 — no second call

"""
Tests for journal feedback: the reflection + verified scripture + audit record
a person receives after writing an entry.
"""

import pytest
from django.utils import timezone

from apps.journal.feedback import generate_feedback, strip_metadata
from apps.journal.models import JournalEntry, JournalFeedback
from apps.reflections.models import OpenThread
from shared.llm import LLMConsentRequired, LLMUnavailable

GOOD_REPLY = {
    "is_spiritual": False,
    "themes": ["Work Stress", "patience"],
    "reflection": "You carried a lot at work today and still made it home for dinner.",
    "passages": [
        {
            "reference": "Philippians 4:6-7",
            "why": "You wrote about the deadline keeping you up at night.",
            "meditation": "Notice the order. What will you hand over?",
        },
        {
            "reference": "Matthew 11:28-30",
            "why": "You are tired.",
            "meditation": "Rest.",
        },
    ],
    "christlike_step": "Thank one coworker by name tomorrow.",
    "growth_note": "",
    "threads": [
        {
            "type": "struggle",
            "summary": "Deadline pressure at work",
            "life_area": "work",
        }
    ],
}


def make_entry(user, text="Work was brutal today. The deadline keeps me up.", mood=""):
    entry = JournalEntry(user=user, date=timezone.now().date(), mood_tag=mood)
    entry.set_content(text)
    entry.save()
    return entry


@pytest.mark.django_db
class TestGenerateFeedback:
    def test_scripture_text_comes_from_the_bible_source_not_the_model(
        self, user, web_bible, fake_llm
    ):
        reply = {
            **GOOD_REPLY,
            "passages": [
                {
                    "reference": "Phil 4:6-7",
                    "why": "why",
                    "meditation": "meditate",
                    # A model that ignores instructions and writes its own "verse":
                    "text": "Do not be anxious about anything (invented wording).",
                }
            ],
        }
        fake_llm(reply=reply)
        feedback = generate_feedback(make_entry(user))

        assert feedback.status == "ok"
        assert feedback.scripture_reference == "Philippians 4:6-7"
        assert feedback.scripture_translation == "WEB"
        assert feedback.scripture_text.startswith("In nothing be anxious")
        assert "invented wording" not in feedback.scripture_text

    def test_hallucinated_reference_is_recorded_and_skipped(
        self, user, web_bible, fake_llm
    ):
        reply = {
            **GOOD_REPLY,
            "passages": [
                {
                    "reference": "Hezekiah 3:16",
                    "why": "made up book",
                    "meditation": "x",
                },
                {
                    "reference": "Philippians 99:1",
                    "why": "no such chapter",
                    "meditation": "x",
                },
                {
                    "reference": "Matthew 11:28-30",
                    "why": "You are tired.",
                    "meditation": "Rest.",
                },
            ],
        }
        fake_llm(reply=reply)
        feedback = generate_feedback(make_entry(user))
        payload = feedback.get_payload()

        assert feedback.scripture_reference == "Matthew 11:28-30"
        assert [c["outcome"] for c in payload["candidates"]] == [
            "invalid",
            "not_found",
            "selected",
        ]
        assert payload["why_this_passage"] == "You are tired."

    def test_ai_unavailable_falls_back_and_says_so(self, user, web_bible, fake_llm):
        fake_llm(error=LLMUnavailable("Could not reach Ollama."))
        feedback = generate_feedback(make_entry(user, "I am so anxious about money."))
        payload = feedback.get_payload()

        assert feedback.status == "fallback"
        assert feedback.provider == "none"
        assert feedback.scripture_reference == "Philippians 4:6-7"
        assert payload["fallback_reason"]["code"] == "AI_UNAVAILABLE"
        assert payload["fallback_reason"]["suggestion"]
        assert "not a personal response" in payload["reflection"]
        assert "anxious" in payload["reflection"]  # says which keyword matched

    def test_consent_required_is_reported_as_the_reason(
        self, user, web_bible, fake_llm
    ):
        fake_llm(error=LLMConsentRequired("Cloud AI not allowed."))
        feedback = generate_feedback(make_entry(user, "A quiet, ordinary day."))

        assert feedback.status == "fallback"
        assert (
            feedback.get_payload()["fallback_reason"]["code"] == "AI_CONSENT_REQUIRED"
        )
        assert feedback.scripture_reference == "Lamentations 3:22-23"

    def test_fallback_uses_mood_when_no_keyword_matches(
        self, user, web_bible, fake_llm
    ):
        fake_llm(error=LLMUnavailable("down"))
        feedback = generate_feedback(
            make_entry(user, "Nothing much.", mood="struggling")
        )
        assert feedback.scripture_reference == "Matthew 11:28-30"

    def test_no_bible_source_means_no_passage_and_a_clear_reason(self, user, fake_llm):
        fake_llm(reply=GOOD_REPLY)  # no web_bible fixture, network blocked
        feedback = generate_feedback(make_entry(user))
        payload = feedback.get_payload()

        assert feedback.scripture_reference == ""
        assert feedback.scripture_text == ""
        assert payload["fallback_reason"]["code"] == "SCRIPTURE_UNAVAILABLE"
        assert payload["reflection"]  # the reflection is still delivered

    def test_everything_derived_from_the_entry_is_encrypted(
        self, user, web_bible, fake_llm
    ):
        fake_llm(reply=GOOD_REPLY)
        feedback = generate_feedback(make_entry(user))
        raw = bytes(feedback.encrypted_payload)

        assert b"deadline" not in raw
        assert b"work stress" not in raw.lower()
        assert feedback.get_payload()["themes"] == ["work stress", "patience"]

    def test_threads_are_created_once(self, user, web_bible, fake_llm):
        fake_llm(reply=GOOD_REPLY)
        generate_feedback(make_entry(user))
        generate_feedback(make_entry(user, "Same deadline, still worried."))

        threads = OpenThread.objects.filter(user=user)
        assert threads.count() == 1
        assert threads.first().get_summary() == "Deadline pressure at work"

    def test_recent_themes_and_passages_feed_the_next_prompt(
        self, user, web_bible, fake_llm
    ):
        llm = fake_llm(reply=GOOD_REPLY)
        generate_feedback(make_entry(user))
        second = generate_feedback(make_entry(user, "Another long day."))

        assert "work stress" in llm.prompts[-1]
        assert "Philippians 4:6-7" in llm.prompts[-1]
        assert "recent_themes" in second.inputs_used

    def test_metadata_block_is_not_sent_to_the_model(self, user, web_bible, fake_llm):
        llm = fake_llm(reply=GOOD_REPLY)
        text = '<!-- DJ_META_START -->{"theme":"secret-meta"}<!-- DJ_META_END -->\nReal words.'
        generate_feedback(make_entry(user, text))

        assert "secret-meta" not in llm.prompts[-1]
        assert "Real words." in llm.prompts[-1]
        assert strip_metadata(text) == "Real words."

    def test_regenerate_keeps_the_old_record_for_the_audit_log(
        self, user, web_bible, fake_llm
    ):
        fake_llm(reply=GOOD_REPLY)
        entry = make_entry(user)
        first = generate_feedback(entry)
        assert generate_feedback(entry).id == first.id  # idempotent without regenerate
        second = generate_feedback(entry, regenerate=True)

        assert second.id != first.id
        assert JournalFeedback.objects.filter(entry=entry).count() == 2
        assert JournalFeedback.objects.filter(entry=entry, is_current=True).count() == 1


@pytest.mark.django_db
class TestFeedbackAPI:
    def test_get_before_generation_is_a_coded_404(self, authenticated_client, user):
        entry = make_entry(user)
        response = authenticated_client.get(f"/api/v1/journal/{entry.id}/feedback/")
        assert response.status_code == 404
        assert response.json()["code"] == "NOT_FOUND"
        assert response.json()["suggestion"]

    def test_generate_then_fetch(self, authenticated_client, user, web_bible, fake_llm):
        fake_llm(reply=GOOD_REPLY)
        entry = make_entry(user)

        response = authenticated_client.post(
            f"/api/v1/journal/{entry.id}/feedback/", {}, format="json"
        )
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert body["scripture"]["reference"] == "Philippians 4:6-7"
        assert body["scripture"]["verified"] is True
        assert body["scripture"]["translation_name"] == "World English Bible"
        assert body["scripture"]["source"] == "local"
        assert body["why_this_passage"]
        assert body["meditation_prompt"]
        assert body["christlike_step"]
        audit = body["audit"]
        assert audit["provider"] == "ollama" and audit["model"] == "test-model"
        assert audit["local"] is True
        assert audit["prompt_version"]
        assert audit["candidates"][0]["outcome"] == "selected"
        assert audit["candidates"][1]["outcome"] == "not_used"
        assert "entry_text" in audit["inputs_used"]
        assert audit["threads_detected"][0]["summary"] == "Deadline pressure at work"

        fetched = authenticated_client.get(f"/api/v1/journal/{entry.id}/feedback/")
        assert fetched.status_code == 200 and fetched.json()["id"] == body["id"]

    def test_ai_down_still_returns_200_with_fallback(
        self, authenticated_client, user, web_bible, fake_llm
    ):
        fake_llm(error=LLMUnavailable("Could not reach Ollama."))
        entry = make_entry(user, "So tired and worn out.")
        response = authenticated_client.post(
            f"/api/v1/journal/{entry.id}/feedback/", {}, format="json"
        )
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "fallback"
        assert body["audit"]["fallback_reason"]["code"] == "AI_UNAVAILABLE"
        assert body["scripture"]["reference"] == "Matthew 11:28-30"

    def test_empty_entry_is_rejected_with_a_suggestion(
        self, authenticated_client, user, fake_llm
    ):
        fake_llm(reply=GOOD_REPLY)
        entry = make_entry(user, "  ")
        response = authenticated_client.post(
            f"/api/v1/journal/{entry.id}/feedback/", {}, format="json"
        )
        assert response.status_code == 400
        assert response.json()["code"] == "VALIDATION_ERROR"
        assert response.json()["suggestion"]

    def test_cannot_touch_another_persons_entry_or_feedback(
        self, authenticated_client, user_factory, web_bible, fake_llm
    ):
        fake_llm(reply=GOOD_REPLY)
        other = user_factory()
        entry = make_entry(other)
        feedback = generate_feedback(entry)

        assert (
            authenticated_client.get(
                f"/api/v1/journal/{entry.id}/feedback/"
            ).status_code
            == 404
        )
        assert (
            authenticated_client.post(
                f"/api/v1/journal/{entry.id}/feedback/", {}, format="json"
            ).status_code
            == 404
        )
        assert (
            authenticated_client.post(
                f"/api/v1/journal/feedback/{feedback.id}/rate/",
                {"helpful": True},
                format="json",
            ).status_code
            == 404
        )
        assert (
            authenticated_client.get("/api/v1/journal/feedback/").json()["count"] == 0
        )

    def test_feedback_endpoints_require_sign_in(self, api_client, user):
        entry = make_entry(user)
        assert api_client.get(f"/api/v1/journal/{entry.id}/feedback/").status_code in (
            401,
            403,
        )
        assert api_client.get(f"/api/v1/journal/{entry.id}/").status_code in (401, 403)
        assert api_client.get("/api/v1/journal/feedback/").status_code in (401, 403)

    def test_rate_and_audit_log_and_themes(
        self, authenticated_client, user, web_bible, fake_llm
    ):
        fake_llm(reply=GOOD_REPLY)
        entry = make_entry(user)
        feedback = generate_feedback(entry)
        generate_feedback(entry, regenerate=True)

        rated = authenticated_client.post(
            f"/api/v1/journal/feedback/{feedback.id}/rate/",
            {"helpful": True},
            format="json",
        )
        assert rated.status_code == 200 and rated.json()["helpful"] is True
        bad = authenticated_client.post(
            f"/api/v1/journal/feedback/{feedback.id}/rate/",
            {"helpful": "yes"},
            format="json",
        )
        assert bad.status_code == 400

        log = authenticated_client.get("/api/v1/journal/feedback/").json()
        assert log["count"] == 2  # the replaced record stays in the audit log
        assert log["results"][0]["is_current"] is True

        themes = authenticated_client.get("/api/v1/journal/themes/").json()
        assert themes["entries_with_feedback"] == 1
        assert {
            "theme": "work stress",
            "count": 1,
            "last_seen": str(entry.date),
        } in themes["themes"]

    def test_journal_list_is_paginated_and_hides_metadata(
        self, authenticated_client, user, web_bible, fake_llm
    ):
        fake_llm(reply=GOOD_REPLY)
        entry = make_entry(
            user,
            '<!-- DJ_META_START -->{"theme":"x"}<!-- DJ_META_END -->\nMy real entry.',
        )
        generate_feedback(entry)
        make_entry(user, "No feedback on this one.")

        body = authenticated_client.get("/api/v1/journal/").json()
        assert body["count"] == 2
        by_id = {row["id"]: row for row in body["results"]}
        row = by_id[str(entry.id)]
        assert row["content_preview"] == "My real entry."
        assert row["has_feedback"] is True
        assert row["scripture_reference"] == "Philippians 4:6-7"
        other = next(r for r in body["results"] if r["id"] != str(entry.id))
        assert other["has_feedback"] is False and other["scripture_reference"] is None

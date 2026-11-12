"""
Tests for the reflections app.

Most of these pin endpoints that used to return 500 (field-name drift, wrong
call signatures, shadowed routes) so they cannot silently break again.
"""

from datetime import date, timedelta

import pytest
from django.utils import timezone

from apps.journal.models import JournalEntry
from apps.reflections.models import (
    DailyReflection,
    DevotionalPassage,
    FocusIntention,
    GrowthReview,
    OpenThread,
    ThreadPrompt,
    UserJourney,
)
from shared.llm import LLMUnavailable


def make_reflection(user, **kwargs):
    reflection = DailyReflection.objects.create(
        user=user, date=kwargs.pop("date", date.today()), scripture_reference="Psalm 23"
    )
    reflection.set_reflection("A long day, but I kept my word.")
    reflection.set_gratitude_note("My family")
    reflection.set_struggle_note("Impatience with the kids")
    reflection.save()
    return reflection


def make_thread(user, summary="Impatience with the kids", days_old=5, **kwargs):
    thread = OpenThread(
        user=user, thread_type=kwargs.pop("thread_type", "struggle"), **kwargs
    )
    thread.set_summary(summary)
    thread.save()
    OpenThread.objects.filter(id=thread.id).update(
        last_mentioned_at=timezone.now() - timedelta(days=days_old)
    )
    thread.refresh_from_db()
    return thread


def make_journey(user):
    return UserJourney.objects.create(
        user=user,
        title="Thirty days",
        goal_statement="Be present",
        success_definition="x",
    )


CURATED = {
    "passages": [
        {
            "scripture_reference": "Philippians 4:6-7",
            "context_note": "Written from prison.",
            "connection_to_focus": "Speaks to anxious seasons.",
            "reflection_prompts": ["What are you carrying?"],
            "application_suggestions": ["Pray before email."],
            "scripture_text": "INVENTED TEXT THE MODEL SHOULD NOT SUPPLY",
        },
        {
            "scripture_reference": "Hezekiah 9:9",
            "connection_to_focus": "not a real book",
        },
        {"scripture_reference": "James 1:5", "connection_to_focus": "Ask for wisdom."},
    ]
}


@pytest.mark.django_db
class TestDailyReflections:
    def test_today_is_404_when_absent_and_200_when_present(
        self, authenticated_client, user
    ):
        assert authenticated_client.get("/api/v1/reflections/today/").status_code == 404
        make_reflection(user)
        response = authenticated_client.get("/api/v1/reflections/today/")
        assert response.status_code == 200

    def test_by_date(self, authenticated_client, user):
        make_reflection(user, date=date(2026, 1, 2))
        assert (
            authenticated_client.get(
                "/api/v1/reflections/by-date/2026-01-02/"
            ).status_code
            == 200
        )
        assert (
            authenticated_client.get(
                "/api/v1/reflections/by-date/2026-01-03/"
            ).status_code
            == 404
        )
        assert (
            authenticated_client.get(
                "/api/v1/reflections/by-date/2026-13-99/"
            ).status_code
            == 400
        )

    def test_generate_insight_stores_it(self, authenticated_client, user, fake_llm):
        fake_llm(text="You kept your word on a hard day. Start tomorrow slower.")
        reflection = make_reflection(user)
        response = authenticated_client.post(
            f"/api/v1/reflections/{reflection.id}/generate_insight/"
        )
        assert response.status_code == 200
        reflection.refresh_from_db()
        assert reflection.ai_insight.startswith("You kept your word")
        assert reflection.ai_provider_used == "ollama"

    def test_generate_insight_reports_ai_outage_with_a_suggestion(
        self, authenticated_client, user, fake_llm
    ):
        fake_llm(error=LLMUnavailable("Could not reach Ollama."))
        reflection = make_reflection(user)
        response = authenticated_client.post(
            f"/api/v1/reflections/{reflection.id}/generate_insight/"
        )
        assert response.status_code == 503
        body = response.json()
        assert body["code"] == "AI_UNAVAILABLE" and body["suggestion"]

    def test_cannot_attach_a_reflection_to_someone_elses_journey(
        self, authenticated_client, user_factory
    ):
        journey = make_journey(user_factory())
        response = authenticated_client.post(
            "/api/v1/reflections/",
            {"date": "2026-01-02", "journey": str(journey.id)},
            format="json",
        )
        assert response.status_code == 400
        assert DailyReflection.objects.count() == 0


@pytest.mark.django_db
class TestThreads:
    def test_create_returns_the_thread(self, authenticated_client):
        response = authenticated_client.post(
            "/api/v1/threads/",
            {"thread_type": "commitment", "summary": "Call my brother"},
            format="json",
        )
        assert response.status_code == 201
        assert response.json()["summary"] == "Call my brother"

    def test_create_rejects_someone_elses_journey(
        self, authenticated_client, user_factory
    ):
        journey = make_journey(user_factory())
        response = authenticated_client.post(
            "/api/v1/threads/",
            {"thread_type": "struggle", "summary": "x", "journey_id": str(journey.id)},
            format="json",
        )
        assert response.status_code == 400

    def test_respond_via_threads_endpoint(
        self, authenticated_client, user, user_factory
    ):
        thread = make_thread(user)
        response = authenticated_client.post(
            "/api/v1/threads/respond/",
            {"thread_id": str(thread.id), "response": "better"},
            format="json",
        )
        assert response.status_code == 200
        assert response.json()["thread_status"] == "progressing"

        foreign = make_thread(user_factory())
        response = authenticated_client.post(
            "/api/v1/threads/respond/",
            {"thread_id": str(foreign.id), "response": "better"},
            format="json",
        )
        assert response.status_code == 404

    def test_pending_prompts_and_check_in(self, authenticated_client, user):
        due = make_thread(user, days_old=5)
        make_thread(user, summary="Too recent", days_old=0)

        pending = authenticated_client.get("/api/v1/thread-prompts/pending/")
        assert pending.status_code == 200
        assert [p["thread_id"] for p in pending.json()] == [str(due.id)]
        assert pending.json()[0]["summary"] == "Impatience with the kids"

        response = authenticated_client.post(
            f"/api/v1/thread-prompts/{due.id}/respond/",
            {"response": "same", "expanded_text": "Still hard in the evenings."},
            format="json",
        )
        assert response.status_code == 200
        assert response.json()["thread_status"] == "following_up"
        prompt = ThreadPrompt.objects.get(thread=due)
        assert prompt.response == "same"
        assert prompt.get_expanded_response() == "Still hard in the evenings."
        assert b"evenings" not in bytes(prompt.encrypted_expanded_response)

        # Answered today, so it is not asked again today.
        assert authenticated_client.get("/api/v1/thread-prompts/pending/").json() == []

    def test_check_in_validation_and_resolve(self, authenticated_client, user):
        thread = make_thread(user)
        bad = authenticated_client.post(
            f"/api/v1/thread-prompts/{thread.id}/respond/",
            {"response": "meh"},
            format="json",
        )
        assert bad.status_code == 400
        done = authenticated_client.post(
            f"/api/v1/thread-prompts/{thread.id}/respond/",
            {"response": "resolved"},
            format="json",
        )
        assert done.json()["thread_status"] == "resolved"

    def test_thread_prompt_list_and_recent(self, authenticated_client, user):
        thread = make_thread(user)
        ThreadPrompt.objects.create(thread=thread, prompt_text="How is it going?")
        assert authenticated_client.get("/api/v1/thread-prompts/").json()["count"] == 1
        assert (
            len(authenticated_client.get("/api/v1/thread-prompts/recent/").json()) == 1
        )


@pytest.mark.django_db
class TestRoutesThatWereShadowedOrBroken:
    def test_growth_milestones_dashboard_and_trends(self, authenticated_client):
        for path in (
            "/api/v1/trends/growth/",
            "/api/v1/milestones/",
            "/api/v1/dashboard/stats/",
            "/api/v1/trends/weekly/",
            "/api/v1/trends/by-area/faith/",
        ):
            assert authenticated_client.get(path).status_code == 200, path

    def test_crew_health_reports_provider(
        self, authenticated_client, settings, monkeypatch
    ):
        from shared.llm import LLMClient

        monkeypatch.setattr(
            LLMClient,
            "health",
            lambda self: {**self.config.public(), "reachable": True, "detail": ""},
        )
        body = authenticated_client.get("/api/v1/crew/health/").json()
        assert body["status"] == "healthy" and body["provider"] == "ollama"

    def test_ai_status_endpoint(self, authenticated_client, settings):
        settings.LLM_BACKEND = "anthropic"
        settings.ANTHROPIC_API_KEY = "sk-ant-server-key"
        body = authenticated_client.get("/api/v1/prompts/ai-status/").json()
        assert body["consent_required"] is True and body["reachable"] is False


@pytest.mark.django_db
class TestDevotionalGeneration:
    def test_focus_creates_passages_with_text_from_the_bible_source(
        self, authenticated_client, user, web_bible, fake_llm
    ):
        fake_llm(
            reply=lambda prompt: CURATED if "passages" in prompt else ["trust", "peace"]
        )
        response = authenticated_client.post(
            "/api/v1/focus/",
            {"period_type": "week", "intention": "Stop carrying anxiety about work"},
            format="json",
        )
        assert response.status_code == 201
        assert response.json()["generation_warning"] is None

        passages = list(
            DevotionalPassage.objects.filter(user=user).order_by("sequence_number")
        )
        assert [p.scripture_reference for p in passages] == [
            "Philippians 4:6-7",
            "James 1:5",
        ]
        assert passages[0].translation == "WEB"
        assert passages[0].scripture_text.startswith("In nothing be anxious")
        assert "INVENTED" not in passages[0].scripture_text
        assert passages[0].scheduled_date == date.today()
        assert FocusIntention.objects.get(user=user).passages_generated is True

    def test_focus_is_saved_and_warns_when_ai_is_down(
        self, authenticated_client, user, fake_llm
    ):
        fake_llm(error=LLMUnavailable("Could not reach Ollama."))
        response = authenticated_client.post(
            "/api/v1/focus/",
            {"period_type": "week", "intention": "Pray daily"},
            format="json",
        )
        assert response.status_code == 201
        warning = response.json()["generation_warning"]
        assert warning["code"] == "AI_UNAVAILABLE" and warning["suggestion"]
        focus = FocusIntention.objects.get(user=user)
        assert focus.passages_generated is False
        assert DevotionalPassage.objects.count() == 0

    def test_on_demand_passage(self, authenticated_client, user, web_bible, fake_llm):
        fake_llm(reply=lambda prompt: CURATED if "passages" in prompt else ["peace"])
        response = authenticated_client.post(
            "/api/v1/passages/generate_on_demand/", {"topic": "anxiety"}, format="json"
        )
        assert response.status_code == 201
        assert response.json()["scripture_reference"] == "Philippians 4:6-7"
        assert DevotionalPassage.objects.get(user=user).focus_intention is None

        missing = authenticated_client.post(
            "/api/v1/passages/generate_on_demand/", {}, format="json"
        )
        assert missing.status_code == 400

    def test_on_demand_reports_ai_outage(self, authenticated_client, fake_llm):
        fake_llm(error=LLMUnavailable("down"))
        response = authenticated_client.post(
            "/api/v1/passages/generate_on_demand/",
            {"topic": "anxiety", "themes": ["peace"]},
            format="json",
        )
        assert response.status_code == 503
        assert response.json()["code"] == "AI_UNAVAILABLE"

    def test_daily_task_fills_today_and_skips_when_ai_is_down(
        self, user, web_bible, fake_llm
    ):
        from apps.reflections.tasks import generate_daily_devotionals

        focus = FocusIntention(
            user=user,
            period_type="week",
            period_start=date.today(),
            period_end=date.today() + timedelta(days=6),
        )
        focus.set_intention("Pray daily")
        focus.save()

        fake_llm(error=LLMUnavailable("down"))
        assert generate_daily_devotionals() == {
            "devotionals_generated": 0,
            "skipped": 1,
            "errors": 0,
        }

        fake_llm(reply=CURATED)
        assert generate_daily_devotionals()["devotionals_generated"] == 1
        assert (
            generate_daily_devotionals()["devotionals_generated"] == 0
        )  # already has today's
        passage = DevotionalPassage.objects.get(focus_intention=focus)
        assert passage.scripture_text.startswith("In nothing be anxious")


REVIEW_REPLY = {
    "summary": "A heavy week at work.",
    "growth": "You apologised to your son the same day.",
    "pattern": "Evenings are the hard hour.",
    "invitation": "Ten quiet minutes before you walk in the door.",
    "passage_reference": "Matthew 11:28-30",
}


@pytest.mark.django_db
class TestGrowthReviews:
    def _entry(self, user, text="Snapped at my son, then apologised."):
        entry = JournalEntry(user=user, date=date.today())
        entry.set_content(text)
        entry.save()
        return entry

    def test_generate_stores_an_encrypted_review_with_real_scripture(
        self, authenticated_client, user, web_bible, fake_llm
    ):
        llm = fake_llm(reply=REVIEW_REPLY)
        self._entry(user)
        response = authenticated_client.post(
            "/api/v1/reviews/generate/", {"period_type": "week"}, format="json"
        )
        assert response.status_code == 201
        body = response.json()
        assert "Where you grew" in body["content"]
        assert "Come to me, all you who labor" in body["content"]
        assert body["provider"] == "ollama"
        assert "apologised" in llm.prompts[-1]

        review = GrowthReview.objects.get(user=user)
        assert b"apologised" not in bytes(review.encrypted_content)

        listing = authenticated_client.get("/api/v1/reviews/").json()
        assert listing["count"] == 1 and listing["results"][0]["id"] == body["id"]

        # Regenerating the same period updates rather than duplicates.
        authenticated_client.post("/api/v1/reviews/generate/", {}, format="json")
        assert GrowthReview.objects.filter(user=user).count() == 1

    def test_nothing_to_review_and_bad_period(self, authenticated_client, fake_llm):
        fake_llm(reply=REVIEW_REPLY)
        empty = authenticated_client.post(
            "/api/v1/reviews/generate/", {}, format="json"
        )
        assert empty.status_code == 400 and empty.json()["suggestion"]
        bad = authenticated_client.post(
            "/api/v1/reviews/generate/", {"period_type": "year"}, format="json"
        )
        assert bad.status_code == 400

    def test_ai_outage_is_reported(self, authenticated_client, user, fake_llm):
        fake_llm(error=LLMUnavailable("down"))
        self._entry(user)
        response = authenticated_client.post(
            "/api/v1/reviews/generate/", {}, format="json"
        )
        assert (
            response.status_code == 503 and response.json()["code"] == "AI_UNAVAILABLE"
        )

    def test_weekly_task_stores_reviews_and_counts_skips(
        self, user, user_factory, fake_llm
    ):
        from apps.reflections.tasks import generate_weekly_reviews

        self._entry(user)
        self._entry(user_factory())
        fake_llm(reply=REVIEW_REPLY)
        assert generate_weekly_reviews() == {
            "reviews_generated": 2,
            "skipped": 0,
            "errors": 0,
        }
        assert GrowthReview.objects.count() == 2

        GrowthReview.objects.all().delete()
        fake_llm(error=LLMUnavailable("down"))
        assert generate_weekly_reviews() == {
            "reviews_generated": 0,
            "skipped": 2,
            "errors": 0,
        }


@pytest.mark.django_db
def test_private_plans_cannot_be_enrolled_in_by_others(
    authenticated_client, user_factory
):
    from apps.plans.models import ReadingPlan

    plan = ReadingPlan.objects.create(
        title_en="Private",
        title_es="Privado",
        description_en="x",
        description_es="x",
        duration_days=3,
        category="faith",
        is_public=False,
        created_by=user_factory(),
    )
    response = authenticated_client.post(f"/api/v1/plans/{plan.id}/enroll/")
    assert response.status_code == 404

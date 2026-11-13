"""
Tests for Bible study guides, the growth profile and growth plans.

Behaviour is tested against a small stand-in library so the tests do not
depend on the wording of real lessons. The real library is checked separately
by TestRealLibrary: every topic present, every field valid, every reference
a passage that exists.
"""

from datetime import timedelta

import pytest
from django.utils import timezone

from apps.guides import library
from apps.guides.catalog import ALL_TOPIC_KEYS, L, TRAIT_KEYS
from apps.guides.models import (
    GrowthGoal,
    GrowthPlan,
    GrowthProfile,
    LessonResponse,
    ProfileAssessment,
    StudyEnrollment,
)
from apps.journal.models import JournalEntry, JournalFeedback
from shared.llm import LLMUnavailable

ALL_STAGES = ["child", "teen", "young_adult", "adult", "senior"]


def _lesson(topic, n, ref):
    return {
        "key": f"{topic}-{n}",
        "ref": ref,
        "title": L(f"{topic} lesson {n}", f"{topic} lección {n}"),
        "truth": L(f"Adult truth {topic} {n}.", f"Verdad adulta {topic} {n}."),
        "simple": L(f"Simple truth {topic} {n}.", f"Verdad sencilla {topic} {n}."),
        "ask": L(f"Adult question {topic} {n}?", f"¿Pregunta adulta {topic} {n}?"),
        "kid_ask": L(f"Kid question {topic} {n}?", f"¿Pregunta niño {topic} {n}?"),
        "do": L(f"Adult practice {topic} {n}.", f"Práctica adulta {topic} {n}."),
        "kid_do": L(f"Kid practice {topic} {n}.", f"Práctica niño {topic} {n}."),
        "pray": L(f"Prayer {topic} {n}.", f"Oración {topic} {n}."),
    }


def _topic(
    key, category, stages, keywords, traits, situations=(), sensitive=False, refs=None
):
    refs = refs or ["Philippians 4:6-7", "Matthew 11:28-30"]
    return {
        "key": key,
        "category": category,
        "title": L(key.title(), key.title() + " ES"),
        "summary": L(f"Summary of {key}.", f"Resumen de {key}."),
        "keywords": keywords,
        "situations": list(situations),
        "traits": traits,
        "stages": stages,
        "stage_notes": {s: L(f"{key} for {s}", f"{key} para {s}") for s in stages},
        "sensitive": sensitive,
        "lessons": [_lesson(key, i, ref) for i, ref in enumerate(refs, start=1)],
    }


FAKE_TOPICS = {
    t["key"]: t
    for t in [
        _topic(
            "anxiety",
            "peace",
            ALL_STAGES,
            ["anxi", "worr", "work pressure"],
            ["peace"],
            ["parent"],
        ),
        _topic("rest", "peace", ALL_STAGES[1:], ["tired", "exhaust"], ["peace"]),
        _topic(
            "marriage",
            "love",
            ["young_adult", "adult", "senior"],
            ["marri", "spouse"],
            ["love"],
            ["married"],
        ),
        _topic("prayer", "foundations", ALL_STAGES, ["pray"], ["prayerfulness"]),
        _topic(
            "despair",
            "refuge",
            ["teen", "young_adult", "adult", "senior"],
            ["hopeless"],
            ["hope"],
            sensitive=True,
        ),
        _topic("who_god_is", "foundations", ALL_STAGES, ["who is god"], ["trust"]),
    ]
}


def _goal(en, kind, count, days):
    return {
        "title": L(en, en + " (es)"),
        "kind": kind,
        "target_count": count,
        "days": days,
    }


FAKE_TRAITS = {
    "peace": {
        "key": "peace",
        "title": L("Peace", "Paz"),
        "definition": L(
            "Peace is steadiness that does not depend on circumstances.",
            "La paz es firmeza.",
        ),
        "refs": ["Philippians 4:6-7", "John 14:27"],
        "jesus": {
            "ref": "Mark 4:37-40",
            "note": L("Jesus sleeps in the storm.", "Jesús duerme en la tormenta."),
        },
        "topics": ["anxiety", "rest"],
        "short_goals": [
            _goal("Pause and breathe before answering.", "practice", 5, 7),
            _goal("Complete two lessons of the Anxiety study.", "study", 2, 7),
            _goal("Write one sentence each evening.", "reflection", 5, 7),
        ],
        "long_goals": [
            _goal("Keep a daily quiet minute.", "practice", 20, 30),
            _goal("Complete both peace studies.", "study", 4, 60),
            _goal("Look back once a week.", "reflection", 12, 90),
        ],
        "check_in_question": L(
            "Where did you find peace this week?", "¿Dónde hallaste paz esta semana?"
        ),
    },
    "love": {
        "key": "love",
        "title": L("Love", "Amor"),
        "definition": L(
            "Love is choosing another person's good at cost to yourself.",
            "El amor es elegir el bien del otro.",
        ),
        "refs": ["1 Corinthians 13:4-7", "1 John 4:7-11"],
        "jesus": {
            "ref": "John 13:3-5",
            "note": L("Jesus washes feet.", "Jesús lava los pies."),
        },
        "topics": ["marriage"],
        "short_goals": [_goal("One unrequested act of service.", "practice", 3, 7)] * 3,
        "long_goals": [_goal("Serve weekly without being asked.", "practice", 12, 90)]
        * 3,
        "check_in_question": L(
            "Whom did you love well this week?", "¿A quién amaste bien esta semana?"
        ),
    },
}


@pytest.fixture
def fake_library(monkeypatch):
    monkeypatch.setattr(library, "topics", lambda: FAKE_TOPICS)
    monkeypatch.setattr(library, "traits", lambda: FAKE_TRAITS)


@pytest.fixture
def client(authenticated_client, fake_library, web_bible):
    return authenticated_client


def set_stage(client, stage="adult", **extra):
    response = client.patch(
        "/api/v1/guides/profile/", {"life_stage": stage, **extra}, format="json"
    )
    assert response.status_code == 200, response.content
    return response.json()


def start(client, topic="anxiety"):
    response = client.post("/api/v1/guides/studies/", {"topic": topic}, format="json")
    assert response.status_code in (200, 201), response.content
    return response.json()


def answer(client, study_id, n=1, **overrides):
    body = {
        "answers": [
            {"question": "Q?", "answer": "I keep worrying about the deadline."}
        ],
        "stood_out": "The word guard.",
        "understanding": 4,
        "resonance": 5,
        **overrides,
    }
    return client.post(
        f"/api/v1/guides/studies/{study_id}/lessons/{n}/respond/", body, format="json"
    )


def journal_with_themes(user, themes, mood="", text="An ordinary day."):
    entry = JournalEntry(user=user, date=timezone.localdate(), mood_tag=mood)
    entry.set_content(text)
    entry.save()
    feedback = JournalFeedback(user=user, entry=entry, status="ok")
    feedback.set_payload({"themes": themes})
    feedback.save()
    return entry


# --------------------------------------------------------------------------
# The real library
# --------------------------------------------------------------------------


class TestRealLibrary:
    def test_library_is_complete_and_every_reference_exists(self):
        pytest.importorskip("pythonbible")  # verse counts, to prove references are real
        assert library.validate_library() == []

    def test_every_topic_and_trait_is_present(self):
        library.topics.cache_clear()
        library.traits.cache_clear()
        assert list(library.topics()) == ALL_TOPIC_KEYS
        assert list(library.traits()) == TRAIT_KEYS
        assert sum(len(t["lessons"]) for t in library.topics().values()) >= 4 * len(
            ALL_TOPIC_KEYS
        )

    def test_no_lesson_quotes_scripture_at_length(self):
        """Lessons paraphrase; the app shows the verse text itself."""
        for topic in library.topics().values():
            for lesson in topic["lessons"]:
                for field in ("truth", "simple"):
                    for text in lesson[field].values():
                        quoted = [
                            q for q in text.split('"')[1::2] if len(q.split()) > 12
                        ]
                        assert (
                            not quoted
                        ), f"{lesson['key']}.{field} quotes at length: {quoted}"

    def test_sensitive_topics_point_to_real_help(self):
        words = (
            "doctor",
            "counselor",
            "pastor",
            "someone you trust",
            "trusted",
            "tell someone",
        )
        for topic in library.topics().values():
            if topic["sensitive"]:
                practices = " ".join(
                    lesson["do"]["en"].lower() for lesson in topic["lessons"]
                )
                assert any(w in practices for w in words), topic["key"]

    def test_validator_catches_a_reference_that_does_not_exist(self):
        pytest.importorskip("pythonbible")
        errors = []
        library.check_reference("Philippians 4:99", "x", errors)
        library.check_reference("Hezekiah 1:1", "x", errors)
        library.check_reference("Psalm 151:1", "x", errors)
        library.check_reference("Psalm 119:1-40", "x", errors)
        library.check_reference("Psalm 23", "x", errors)
        assert len(errors) == 5
        ok = []
        library.check_reference("1 Corinthians 13:4-7", "x", ok)
        assert ok == []


# --------------------------------------------------------------------------
# Catalog, life stages, recommendations
# --------------------------------------------------------------------------


@pytest.mark.django_db
class TestCatalogAndRecommendations:
    def test_catalog_is_localised_and_carries_stage_notes(self, client):
        set_stage(client, "teen")
        body = client.get("/api/v1/guides/catalog/?lang=es").json()
        assert [s["key"] for s in body["life_stages"]] == ALL_STAGES
        peace = next(c for c in body["categories"] if c["key"] == "peace")
        assert peace["title"] == "Paz"
        anxiety = next(t for t in peace["topics"] if t["key"] == "anxiety")
        assert anxiety["stage_note"] == "anxiety para teen"
        assert anxiety["lesson_count"] == 2 and anxiety["enrollment"] is None
        assert len(body["assessment"]["items"]) == 14
        assert {t["key"] for t in body["traits"]} == {"peace", "love"}

    def test_new_person_gets_starters_with_a_reason(self, client):
        body = client.get("/api/v1/guides/recommendations/").json()
        assert body["based_on"] == {"entries_considered": 0, "has_profile": False}
        assert [r["topic"]["key"] for r in body["results"]][:2] == [
            "who_god_is",
            "prayer",
        ]
        assert all(r["reasons"] for r in body["results"])

    def test_journal_themes_drive_suggestions_and_the_reason_says_so(
        self, client, user
    ):
        set_stage(client)
        for _ in range(3):
            journal_with_themes(user, ["work pressure", "family"])
        top = client.get("/api/v1/guides/recommendations/").json()["results"][0]
        assert top["topic"]["key"] == "anxiety"
        assert any(
            "work pressure" in reason and "3" in reason for reason in top["reasons"]
        )

    def test_words_in_entries_without_feedback_also_count(self, client, user):
        set_stage(client)
        entry = JournalEntry(user=user, date=timezone.localdate())
        entry.set_content("I am exhausted and have nothing left.")
        entry.save()
        results = client.get("/api/v1/guides/recommendations/").json()["results"]
        assert results[0]["topic"]["key"] == "rest"
        assert results[0]["reasons"] == ["A recent entry uses words like “exhausted”."]
        assert len(results) >= 3  # padded with good first studies, each with a reason
        assert all(r["reasons"] for r in results)

        again = JournalEntry(user=user, date=timezone.localdate())
        again.set_content("Still so tired.")
        again.save()
        top = client.get("/api/v1/guides/recommendations/").json()["results"][0]
        assert top["reasons"] == ["2 of your recent entries use words like “tired”."]

    def test_needs_traits_situations_and_assessment_all_count(self, client):
        set_stage(
            client,
            "adult",
            needs=["marriage"],
            situations=["parent"],
            desired_traits=["peace"],
        )
        client.post(
            "/api/v1/guides/profile/assessment/",
            {"answers": {"prayer": 1}},
            format="json",
        )
        results = {
            r["topic"]["key"]: r
            for r in client.get("/api/v1/guides/recommendations/").json()["results"]
        }
        assert "looking for help" in results["marriage"]["reasons"][0]
        assert any("peace" in r for r in results["anxiety"]["reasons"])
        assert any("parent" in r for r in results["anxiety"]["reasons"])
        assert any("rated this low" in r for r in results["prayer"]["reasons"])
        scores = [r["score"] for r in results.values()]
        assert scores == sorted(scores, reverse=True)

    def test_life_stage_filters_what_is_offered(self, client):
        set_stage(client, "child", needs=["marriage", "anxiety"])
        keys = [
            r["topic"]["key"]
            for r in client.get("/api/v1/guides/recommendations/").json()["results"]
        ]
        assert "marriage" not in keys and "anxiety" in keys

    def test_studies_in_progress_or_done_are_not_suggested_again(self, client):
        set_stage(client, "adult", needs=["anxiety"])
        start(client, "anxiety")
        keys = [
            r["topic"]["key"]
            for r in client.get("/api/v1/guides/recommendations/").json()["results"]
        ]
        assert "anxiety" not in keys


# --------------------------------------------------------------------------
# Studies and lessons
# --------------------------------------------------------------------------


@pytest.mark.django_db
class TestStudies:
    def test_lesson_shows_real_scripture_and_adult_level(self, client):
        set_stage(client, "adult")
        study = start(client)
        assert study["life_stage"] == "adult" and study["lesson_count"] == 2
        lesson = client.get(f"/api/v1/guides/studies/{study['id']}/lessons/1/").json()
        assert lesson["passage"]["reference"] == "Philippians 4:6-7"
        assert lesson["passage"]["text"].startswith("In nothing be anxious")
        assert lesson["passage"]["verified"] is True
        assert lesson["explanation"] == "Adult truth anxiety 1."
        assert lesson["questions"][0] == "Adult question anxiety 1?"
        assert len(lesson["questions"]) == 3
        assert lesson["practice"] == "Adult practice anxiety 1."
        assert lesson["with_grown_up"] is False and lesson["support_note"] is None
        assert lesson["previous"] is None and lesson["next"] == {"number": 2}

    def test_each_stage_gets_its_own_question(self, client):
        seen = set()
        for stage in ("teen", "young_adult", "adult", "senior"):
            StudyEnrollment.objects.all().delete()
            set_stage(client, stage)
            study = start(client)
            seen.add(
                client.get(f"/api/v1/guides/studies/{study['id']}/lessons/1/").json()[
                    "questions"
                ][2]
            )
        assert len(seen) == 4

    def test_child_gets_the_simple_lesson_to_read_with_a_grown_up(self, client):
        set_stage(client, "child")
        study = start(client)
        lesson = client.get(f"/api/v1/guides/studies/{study['id']}/lessons/1/").json()
        assert lesson["with_grown_up"] is True
        assert lesson["explanation"] == "Simple truth anxiety 1."
        assert lesson["explanation_level"] == "simple"
        assert lesson["questions"][0] == "Kid question anxiety 1?"
        assert lesson["practice"] == "Kid practice anxiety 1."

    def test_spanish(self, client):
        set_stage(client, "adult")
        study = start(client)
        lesson = client.get(
            f"/api/v1/guides/studies/{study['id']}/lessons/1/?lang=es"
        ).json()
        assert lesson["explanation"] == "Verdad adulta anxiety 1."
        assert lesson["questions"][1].startswith("¿Qué te muestra")

    def test_sensitive_study_carries_a_support_note(self, client):
        set_stage(client, "adult")
        study = start(client, "despair")
        lesson = client.get(f"/api/v1/guides/studies/{study['id']}/lessons/1/").json()
        assert "988" in lesson["support_note"] and "counselor" in lesson["support_note"]

    def test_bible_source_down_still_shows_the_lesson(
        self, authenticated_client, fake_library
    ):
        set_stage(
            authenticated_client, "adult"
        )  # no web_bible fixture, network blocked
        study = start(authenticated_client)
        lesson = authenticated_client.get(
            f"/api/v1/guides/studies/{study['id']}/lessons/1/"
        ).json()
        assert lesson["passage"] is None
        assert lesson["passage_error"]["code"] == "SCRIPTURE_UNAVAILABLE"
        assert lesson["reference"] == "Philippians 4:6-7"
        assert lesson["explanation"]

    def test_simplify_is_remembered(self, client):
        set_stage(client, "adult")
        study = start(client)
        url = f"/api/v1/guides/studies/{study['id']}/lessons/1/"
        assert (
            client.post(url + "simplify/").json()["explanation"]
            == "Simple truth anxiety 1."
        )
        assert client.get(url).json()["explanation_level"] == "simple"

    def test_answering_gets_a_reply_and_advances(self, client, fake_llm, user):
        llm = fake_llm(
            reply={
                "reply": "You named the deadline plainly.",
                "follow_up": "What are you afraid will happen?",
            }
        )
        set_stage(client, "adult")
        study = start(client)
        result = answer(client, study["id"]).json()

        assert result["reply"] == {
            "text": "You named the deadline plainly.",
            "follow_up": "What are you afraid will happen?",
            "source": "ai",
            "fallback_reason": None,
        }
        assert "deadline" in llm.prompts[-1] and "Philippians 4:6-7" in llm.prompts[-1]
        assert result["next_step"] == {"kind": "next_lesson", "number": 2}
        assert (
            result["study"]["completed_lessons"] == [1]
            and result["study"]["progress_percent"] == 50
        )
        assert result["lesson"]["response"]["stood_out"] == "The word guard."

        record = LessonResponse.objects.get()
        assert b"deadline" not in bytes(record.encrypted_payload)
        assert (record.understanding, record.resonance) == (4, 5)

    def test_ai_down_gives_a_built_in_reply_that_says_why(self, client, fake_llm):
        fake_llm(error=LLMUnavailable("Could not reach Ollama."))
        set_stage(client, "adult")
        study = start(client)
        response = answer(client, study["id"], understanding=1)
        assert response.status_code == 200
        reply = response.json()["reply"]
        assert reply["source"] == "built_in"
        assert reply["fallback_reason"]["code"] == "AI_UNAVAILABLE"
        assert "Explain it more simply" in reply["text"]

    def test_a_childs_answers_are_never_sent_to_a_model(self, client, fake_llm):
        llm = fake_llm(reply={"reply": "x", "follow_up": None})
        set_stage(client, "child")
        study = start(client)
        reply = answer(client, study["id"]).json()["reply"]
        assert llm.prompts == []
        assert reply["source"] == "built_in" and reply["fallback_reason"] is None
        blocked = client.post(
            f"/api/v1/guides/studies/{study['id']}/lessons/1/personalize/"
        )
        assert blocked.status_code == 400 and llm.prompts == []

    def test_completing_every_lesson_completes_the_study(self, client, fake_llm):
        fake_llm(reply={"reply": "Good.", "follow_up": None})
        set_stage(client, "adult", needs=["rest"])
        study = start(client)
        answer(client, study["id"], 1)
        result = answer(client, study["id"], 2).json()
        assert (
            result["study"]["status"] == "completed"
            and result["study"]["progress_percent"] == 100
        )
        assert result["next_step"]["kind"] == "study_complete"
        assert result["next_step"]["suggestions"][0]["key"] == "rest"
        # Starting it again begins a fresh run rather than reopening the finished one.
        again = client.post(
            "/api/v1/guides/studies/", {"topic": "anxiety"}, format="json"
        )
        assert again.status_code == 201 and again.json()["id"] != study["id"]

    def test_validation(self, client, fake_llm):
        fake_llm(reply={"reply": "x"})
        set_stage(client, "adult")
        study = start(client)
        empty = answer(client, study["id"], answers=[], stood_out="")
        assert empty.status_code == 400 and empty.json()["suggestion"]
        assert answer(client, study["id"], understanding=9).status_code == 400
        assert (
            client.get(f"/api/v1/guides/studies/{study['id']}/lessons/7/").status_code
            == 404
        )
        assert (
            client.post(
                "/api/v1/guides/studies/", {"topic": "nope"}, format="json"
            ).status_code
            == 404
        )
        assert start(client)["id"] == study["id"]  # same active study, not a duplicate

    def test_personalize_uses_profile_and_themes_and_is_stored_encrypted(
        self, client, fake_llm, user
    ):
        llm = fake_llm(
            reply={
                "connection": "With small children and a heavy job, this may land close to home.",
                "explanation": "Paul is telling a tired parent what to do with worry.",
                "questions": ["Which worry is loudest at bedtime?", "Q2?", "Q3?"],
            }
        )
        set_stage(
            client, "adult", situations=["parent"], about_me="Two kids under five."
        )
        journal_with_themes(user, ["work pressure"])
        study = start(client)
        lesson = client.post(
            f"/api/v1/guides/studies/{study['id']}/lessons/1/personalize/"
        ).json()
        assert (
            lesson["personal"]["questions"][0] == "Which worry is loudest at bedtime?"
        )
        assert (
            lesson["personal"]["provider"] == "ollama"
            and lesson["personal"]["local"] is True
        )
        prompt = llm.prompts[-1]
        assert (
            "Parent" in prompt
            and "work pressure" in prompt
            and "Two kids under five." in prompt
        )
        assert (
            lesson["explanation"] == "Adult truth anxiety 1."
        )  # the standard lesson is untouched
        assert b"bedtime" not in bytes(LessonResponse.objects.get().encrypted_personal)

    def test_personalize_reports_ai_outage(self, client, fake_llm):
        fake_llm(error=LLMUnavailable("down"))
        set_stage(client, "adult")
        study = start(client)
        response = client.post(
            f"/api/v1/guides/studies/{study['id']}/lessons/1/personalize/"
        )
        assert (
            response.status_code == 503 and response.json()["code"] == "AI_UNAVAILABLE"
        )

    def test_other_peoples_studies_are_invisible(self, client, user_factory, fake_llm):
        fake_llm(reply={"reply": "x"})
        other = StudyEnrollment.objects.create(user=user_factory(), topic_key="anxiety")
        base = f"/api/v1/guides/studies/{other.id}/"
        assert client.get(base).status_code == 404
        assert client.get(base + "lessons/1/").status_code == 404
        assert answer(client, other.id).status_code == 404
        assert client.delete(base).status_code == 404
        assert client.get("/api/v1/guides/studies/").json() == []

    def test_endpoints_require_sign_in(self, api_client, fake_library):
        for path in ("catalog/", "recommendations/", "studies/", "profile/", "plans/"):
            assert api_client.get(f"/api/v1/guides/{path}").status_code in (
                401,
                403,
            ), path


# --------------------------------------------------------------------------
# Growth profile
# --------------------------------------------------------------------------

INSIGHTS = {
    "summary": "You are carrying a lot at work and still showing up to pray.",
    "items": [
        {
            "area": "spiritual",
            "title": "You keep praying",
            "text": "It seems prayer is steady for you.",
            "evidence": ["You rated 'I talk with God most days' 4 of 5"],
        },
        {
            "area": "inner",
            "title": "Hard to let go",
            "text": "You often mention work pressure.",
            "evidence": [
                "The theme 'work pressure' appears 3 times",
                "You rated letting go 2 of 5",
            ],
        },
        {
            "area": "inner",
            "title": "A label",
            "text": "This looks like an anxiety disorder.",
            "evidence": ["made up"],
        },
        {
            "area": "inner",
            "title": "No evidence",
            "text": "You seem fine.",
            "evidence": [],
        },
    ],
    "encouragement": "Tell one person how the week really went.",
    "suggested_topics": ["anxiety", "not_a_topic"],
    "suggested_traits": ["peace", "not_a_trait"],
}


@pytest.mark.django_db
class TestProfile:
    def test_empty_profile(self, client):
        body = client.get("/api/v1/guides/profile/").json()
        assert body["exists"] is False and body["life_stage"] is None
        assert body["insights"] is None and body["support"] is None
        assert "not a diagnosis" in body["disclaimer"]

    def test_setup_assessment_and_snapshot(self, client, user):
        set_stage(
            client,
            "adult",
            situations=["parent"],
            faith_background="growing",
            desired_traits=["love"],
            about_me="I travel a lot for work.",
        )
        body = client.post(
            "/api/v1/guides/profile/assessment/",
            {
                "answers": {"prayer": 4, "calm": 2, "release": 1},
                "trait_ratings": {"peace": 2, "love": 5},
            },
            format="json",
        ).json()
        assert body["exists"] is True and body["about_me"] == "I travel a lot for work."
        practices = {p["key"]: p["score"] for p in body["spiritual"]["practices"]}
        assert practices["prayer"] == 4 and practices["scripture"] is None
        assert body["spiritual"]["strengths"] == [
            {"trait": "love", "title": "Love", "score": 5}
        ]
        assert body["spiritual"]["growth_areas"][0] == {
            "trait": "peace",
            "title": "Peace",
            "score": 2,
        }
        inner = {p["key"]: p["score"] for p in body["inner_life"]["items"]}
        assert inner["calm"] == 2 and inner["release"] == 1
        assert body["assessment"]["history"][0]["practices_avg"] == 4.0
        assert body["assessment"]["history"][0]["inner_avg"] == 1.5

        record = ProfileAssessment.objects.get()
        assert b"calm" not in bytes(record.encrypted_payload)
        profile = GrowthProfile.objects.get()
        assert b"travel" not in bytes(profile.encrypted_about_me)

    def test_wizard_saves_merge_into_one_sitting_and_later_ones_make_history(
        self, client, user
    ):
        set_stage(client)
        client.post(
            "/api/v1/guides/profile/assessment/",
            {"answers": {"prayer": 2}},
            format="json",
        )
        client.post(
            "/api/v1/guides/profile/assessment/",
            {"answers": {"calm": 3}},
            format="json",
        )
        assert ProfileAssessment.objects.count() == 1
        ProfileAssessment.objects.update(taken_at=timezone.now() - timedelta(days=30))
        body = client.post(
            "/api/v1/guides/profile/assessment/",
            {"answers": {"prayer": 4}},
            format="json",
        ).json()
        assert [h["practices_avg"] for h in body["assessment"]["history"]] == [2.0, 4.0]
        assert body["assessment"]["answers"] == {
            "prayer": 4,
            "calm": 3,
        }  # unanswered items carry over

    def test_activity_feeds_the_snapshot(self, client, user, fake_llm):
        fake_llm(reply={"reply": "ok"})
        set_stage(client)
        journal_with_themes(user, ["work pressure"], mood="struggling")
        journal_with_themes(user, ["work pressure", "family"], mood="grateful")
        study = start(client)
        answer(client, study["id"], understanding=2, resonance=4)
        body = client.get("/api/v1/guides/profile/").json()
        assert body["inner_life"]["mood_counts"] == {"struggling": 1, "grateful": 1}
        assert body["inner_life"]["recurring_themes"] == [
            {"theme": "work pressure", "count": 2}
        ]
        assert body["inner_life"]["understanding_avg"] == 2.0
        assert body["spiritual"]["lessons_completed"] == 1
        assert body["spiritual"]["entries_with_feedback"] == 2

    def test_validation(self, client):
        assert (
            client.patch(
                "/api/v1/guides/profile/", {"life_stage": "elder"}, format="json"
            ).status_code
            == 400
        )
        assert (
            client.patch(
                "/api/v1/guides/profile/",
                {"desired_traits": ["peace", "love", "peace", "x"]},
                format="json",
            ).status_code
            == 400
        )
        set_stage(client)
        bad = client.post(
            "/api/v1/guides/profile/assessment/",
            {"answers": {"prayer": 6}},
            format="json",
        )
        assert bad.status_code == 400
        assert (
            client.post(
                "/api/v1/guides/profile/assessment/",
                {"answers": {"nope": 3}},
                format="json",
            ).status_code
            == 400
        )

    def test_insights_need_enough_to_go_on(self, client, fake_llm):
        llm = fake_llm(reply=INSIGHTS)
        set_stage(client)
        response = client.post("/api/v1/guides/profile/insights/")
        assert response.status_code == 400 and response.json()["suggestion"]
        assert llm.prompts == []

    def test_insights_must_cite_evidence_and_never_diagnose(
        self, client, fake_llm, user
    ):
        llm = fake_llm(reply=INSIGHTS)
        set_stage(
            client, "adult", about_me="I am not anxious, I am grieving my father."
        )
        client.post(
            "/api/v1/guides/profile/assessment/",
            {
                "answers": {
                    "prayer": 4,
                    "calm": 2,
                    "release": 2,
                    "hopeful": 3,
                    "rested": 2,
                }
            },
            format="json",
        )
        for _ in range(3):
            journal_with_themes(user, ["work pressure"])
        body = client.post("/api/v1/guides/profile/insights/").json()
        insights = body["insights"]
        assert [i["title"] for i in insights["items"]] == [
            "You keep praying",
            "Hard to let go",
        ]
        assert all(i["evidence"] and i["accurate"] is None for i in insights["items"])
        assert [t["key"] for t in insights["suggested_topics"]] == ["anxiety"]
        assert insights["suggested_traits"] == [{"key": "peace", "title": "Peace"}]
        assert insights["provider"] == "ollama" and insights["local"] is True
        prompt = llm.prompts[-1]
        assert "grieving my father" in prompt and "work pressure (3)" in prompt
        assert "I talk with God most days. → 4" in prompt
        assert b"praying" not in bytes(GrowthProfile.objects.get().encrypted_insights)

    def test_person_can_reject_an_insight_and_it_is_not_repeated(
        self, client, fake_llm, user
    ):
        llm = fake_llm(reply=INSIGHTS)
        set_stage(client)
        for _ in range(3):
            journal_with_themes(user, ["work pressure"])
        item = client.post("/api/v1/guides/profile/insights/").json()["insights"][
            "items"
        ][1]
        body = client.post(
            f"/api/v1/guides/profile/insights/{item['id']}/feedback/",
            {"accurate": False},
            format="json",
        ).json()
        assert body["insights"]["items"][1]["accurate"] is False
        client.post("/api/v1/guides/profile/insights/")
        assert (
            "Hard to let go" in llm.prompts[-1].split("ALREADY TOLD YOU WERE WRONG")[1]
        )
        assert (
            client.post(
                "/api/v1/guides/profile/insights/zzz/feedback/",
                {"accurate": True},
                format="json",
            ).status_code
            == 404
        )

    def test_insights_report_ai_outage(self, client, fake_llm, user):
        fake_llm(error=LLMUnavailable("down"))
        set_stage(client)
        for _ in range(3):
            journal_with_themes(user, ["x"])
        response = client.post("/api/v1/guides/profile/insights/")
        assert (
            response.status_code == 503 and response.json()["code"] == "AI_UNAVAILABLE"
        )

    def test_no_profile_is_built_for_a_child(self, client, fake_llm, user):
        llm = fake_llm(reply=INSIGHTS)
        set_stage(client, "adult")
        client.post(
            "/api/v1/guides/profile/assessment/",
            {"answers": {"calm": 1}},
            format="json",
        )
        body = set_stage(client, "child")
        assert body["profiling_enabled"] is False
        assert body["assessment"] is None and body["inner_life"]["items"] == []
        assert ProfileAssessment.objects.count() == 0  # what was inferred is dropped
        assert (
            client.post(
                "/api/v1/guides/profile/assessment/",
                {"answers": {"calm": 1}},
                format="json",
            ).status_code
            == 400
        )
        assert client.post("/api/v1/guides/profile/insights/").status_code == 400
        assert llm.prompts == []

    def test_support_message_when_someone_is_carrying_a_lot(self, client, user):
        set_stage(client)
        for _ in range(4):
            journal_with_themes(user, [], mood="struggling")
        journal_with_themes(user, [], mood="grateful")
        support = client.get("/api/v1/guides/profile/").json()["support"]
        assert (
            "someone you trust" in support["message"]
            and "988" not in support["message"]
        )

    def test_crisis_language_gets_the_urgent_message(self, client, user):
        set_stage(client)
        journal_with_themes(
            user, [], text="Some days I think they would be better off without me."
        )
        support = client.get("/api/v1/guides/profile/").json()["support"]
        assert "988" in support["message"] and "emergency" in support["message"]

    def test_erase_removes_profile_but_keeps_studies_and_plans(self, client, user):
        set_stage(client, about_me="private")
        client.post(
            "/api/v1/guides/profile/assessment/",
            {"answers": {"calm": 3}},
            format="json",
        )
        start(client)
        client.post("/api/v1/guides/plans/", {"trait": "peace"}, format="json")
        assert client.delete("/api/v1/guides/profile/").status_code == 204
        assert (
            GrowthProfile.objects.count() == 0
            and ProfileAssessment.objects.count() == 0
        )
        assert StudyEnrollment.objects.count() == 1 and GrowthPlan.objects.count() == 1
        assert client.get("/api/v1/guides/profile/").json()["exists"] is False


# --------------------------------------------------------------------------
# Growth plans
# --------------------------------------------------------------------------


@pytest.mark.django_db
class TestGrowthPlans:
    def make(self, client, **body):
        response = client.post(
            "/api/v1/guides/plans/", {"trait": "peace", **body}, format="json"
        )
        assert response.status_code == 201, response.content
        return response.json()

    def test_plan_has_short_and_long_goals_scripture_and_starting_status(self, client):
        set_stage(client)
        plan = self.make(
            client, why="I snap at my kids when work is heavy.", baseline_rating=2
        )
        assert plan["trait"]["title"] == "Peace" and plan["why"].startswith("I snap")
        assert [g["horizon"] for g in plan["goals"]] == ["long"] * 3 + ["short"] * 3
        short = [g for g in plan["goals"] if g["horizon"] == "short"]
        assert [g["auto"] for g in short] == [False, True, False]
        today = timezone.localdate()
        assert short[0]["due_date"] == str(today + timedelta(days=7))
        assert plan["target_date"] == str(today + timedelta(days=90))
        assert plan["scripture"] == [
            {"reference": "Philippians 4:6-7"},
            {"reference": "John 14:27"},
        ]
        assert plan["jesus"]["reference"] == "Mark 4:37-40"
        assert [t["key"] for t in plan["topics"]] == ["anxiety", "rest"]
        progress = plan["progress"]
        assert progress["percent"] == 0 and progress["stage"] == "starting"
        assert (
            progress["goals_total"] == 6
            and progress["days_in"] == 1
            and progress["days_total"] == 90
        )
        assert progress["check_in_due"] is False
        assert plan["goal_source"] == "catalog" and plan["current_rating"] == 2

        assert b"snap" not in bytes(GrowthPlan.objects.get().encrypted_why)
        assert b"breathe" not in bytes(GrowthGoal.objects.first().encrypted_title)

    def test_baseline_comes_from_the_assessment_when_not_given(self, client):
        set_stage(client)
        client.post(
            "/api/v1/guides/profile/assessment/",
            {"trait_ratings": {"peace": 3}},
            format="json",
        )
        assert self.make(client)["baseline_rating"] == 3

    def test_goal_progress_and_status(self, client):
        plan = self.make(client)
        goal = next(
            g for g in plan["goals"] if g["horizon"] == "short" and not g["auto"]
        )
        url = f"/api/v1/guides/plans/{plan['id']}/goals/{goal['id']}/"
        after = client.patch(url, {"add": 2}, format="json").json()
        updated = next(g for g in after["goals"] if g["id"] == goal["id"])
        assert (updated["progress_count"], updated["percent"], updated["status"]) == (
            2,
            40,
            "active",
        )
        after = client.patch(
            url, {"add": 10}, format="json"
        ).json()  # clamps at the target
        updated = next(g for g in after["goals"] if g["id"] == goal["id"])
        assert (updated["progress_count"], updated["status"]) == (5, "done")
        assert (
            after["progress"]["goals_done"] == 1
            and after["progress"]["short_percent"] == 33
        )
        assert after["progress"]["percent"] == 13  # 0.4 * 33 + 0.6 * 0

        skipped = client.patch(url, {"status": "skipped"}, format="json").json()
        assert skipped["progress"]["goals_total"] == 5

    def test_study_goals_count_lessons_automatically(self, client, fake_llm):
        fake_llm(reply={"reply": "ok"})
        set_stage(client)
        plan = self.make(client)
        auto = next(g for g in plan["goals"] if g["auto"] and g["horizon"] == "short")
        manual = client.patch(
            f"/api/v1/guides/plans/{plan['id']}/goals/{auto['id']}/",
            {"add": 1},
            format="json",
        )
        assert manual.status_code == 400 and manual.json()["suggestion"]
        ticked = client.patch(
            f"/api/v1/guides/plans/{plan['id']}/goals/{auto['id']}/",
            {"status": "done"},
            format="json",
        )
        assert ticked.status_code == 400

        study = start(client, "anxiety")
        answer(client, study["id"], 1)
        answer(client, study["id"], 2)
        after = client.get(f"/api/v1/guides/plans/{plan['id']}/").json()
        short_auto = next(g for g in after["goals"] if g["id"] == auto["id"])
        long_auto = next(
            g for g in after["goals"] if g["auto"] and g["horizon"] == "long"
        )
        assert (short_auto["progress_count"], short_auto["status"]) == (2, "done")
        assert (long_auto["progress_count"], long_auto["status"]) == (2, "active")
        assert after["progress"]["lessons_done"] == 2
        assert after["topics"][0]["enrollment"]["status"] == "completed"

    def test_lessons_before_the_plan_started_do_not_count(self, client, fake_llm):
        fake_llm(reply={"reply": "ok"})
        set_stage(client)
        study = start(client, "anxiety")
        answer(client, study["id"], 1)
        LessonResponse.objects.update(completed_at=timezone.now() - timedelta(days=2))
        assert self.make(client)["progress"]["lessons_done"] == 0

    def test_check_ins_track_rating_and_become_due_weekly(self, client):
        plan = self.make(client, baseline_rating=2)
        GrowthPlan.objects.update(started_at=timezone.now() - timedelta(days=8))
        due = client.get(f"/api/v1/guides/plans/{plan['id']}/").json()["progress"]
        assert due["check_in_due"] is True and "check-in is due" in due["summary"]

        after = client.post(
            f"/api/v1/guides/plans/{plan['id']}/checkins/",
            {"rating": 3, "note": "Stayed calm on Tuesday's call."},
            format="json",
        ).json()
        assert after["checkins"][0]["note"] == "Stayed calm on Tuesday's call."
        assert after["current_rating"] == 3 and after["progress"]["rating_change"] == 1
        assert after["progress"]["check_in_due"] is False
        assert (
            "from 2 to 3" in after["progress"]["summary"]
            and "Day 9 of" in after["progress"]["summary"]
        )
        assert (
            client.post(
                f"/api/v1/guides/plans/{plan['id']}/checkins/",
                {"rating": 0},
                format="json",
            ).status_code
            == 400
        )

    def test_custom_goals_and_editing(self, client):
        plan = self.make(client)
        url = f"/api/v1/guides/plans/{plan['id']}/goals/"
        after = client.post(
            url,
            {
                "title": "Walk without my phone",
                "horizon": "short",
                "target_count": 3,
                "days": 7,
            },
            format="json",
        ).json()
        mine = next(g for g in after["goals"] if g["title"] == "Walk without my phone")
        assert mine["auto"] is False and mine["target_count"] == 3
        renamed = client.patch(
            url + mine["id"] + "/", {"title": "Walk at lunch"}, format="json"
        ).json()
        assert any(g["title"] == "Walk at lunch" for g in renamed["goals"])
        removed = client.delete(url + mine["id"] + "/").json()
        assert len(removed["goals"]) == 6
        assert (
            client.post(
                url,
                {"title": "x", "horizon": "soon", "target_count": 1, "days": 1},
                format="json",
            ).status_code
            == 400
        )

    def test_status_changes_and_one_plan_per_trait(self, client):
        plan = self.make(client)
        duplicate = client.post(
            "/api/v1/guides/plans/", {"trait": "peace"}, format="json"
        )
        assert duplicate.status_code == 400 and duplicate.json()["suggestion"]
        url = f"/api/v1/guides/plans/{plan['id']}/"
        assert (
            client.patch(url, {"status": "paused"}, format="json").json()["progress"][
                "check_in_due"
            ]
            is False
        )
        done = client.patch(url, {"status": "completed"}, format="json").json()
        assert (
            done["progress"]["percent"] == 100
            and done["progress"]["stage"] == "established"
        )
        assert (
            client.post(
                "/api/v1/guides/plans/", {"trait": "peace"}, format="json"
            ).status_code
            == 201
        )
        assert (
            client.post(
                "/api/v1/guides/plans/", {"trait": "nope"}, format="json"
            ).status_code
            == 400
        )
        statuses = [p["status"] for p in client.get("/api/v1/guides/plans/").json()]
        assert statuses == ["active", "completed"]

    def test_ai_tailored_goals_keep_the_automatic_study_goals(self, client, fake_llm):
        llm = fake_llm(
            reply={
                "short_goals": [
                    {
                        "title": "Before each client call, pray one sentence.",
                        "kind": "prayer",
                        "target_count": 5,
                        "days": 7,
                    },
                    {"title": "Bad", "kind": "study", "target_count": 999, "days": 3},
                ],
                "long_goals": [
                    {
                        "title": "Leave work by six three days a week.",
                        "kind": "practice",
                        "target_count": 12,
                        "days": 30,
                    },
                ],
            }
        )
        set_stage(client, "adult", situations=["parent"])
        plan = self.make(
            client, why="Work calls leave me short with my kids.", personalize=True
        )
        assert plan["goal_source"] == "ai" and plan["personalize_error"] is None
        titles = [g["title"] for g in plan["goals"]]
        assert (
            "Before each client call, pray one sentence." in titles
            and "Bad" not in titles
        )
        assert sum(1 for g in plan["goals"] if g["auto"]) == 2
        assert (
            "Work calls leave me short" in llm.prompts[-1]
            and "Parent" in llm.prompts[-1]
        )

    def test_ai_down_still_creates_the_plan_from_the_catalog(self, client, fake_llm):
        fake_llm(error=LLMUnavailable("Could not reach Ollama."))
        plan = self.make(client, personalize=True)
        assert plan["goal_source"] == "catalog" and len(plan["goals"]) == 6
        assert plan["personalize_error"]["code"] == "AI_UNAVAILABLE"

    def test_other_peoples_plans_are_invisible(
        self, client, user_factory, fake_library
    ):
        other = GrowthPlan.objects.create(
            user=user_factory(), trait_key="peace", target_date=timezone.localdate()
        )
        base = f"/api/v1/guides/plans/{other.id}/"
        assert client.get(base).status_code == 404
        assert (
            client.patch(base, {"status": "paused"}, format="json").status_code == 404
        )
        assert (
            client.post(base + "checkins/", {"rating": 3}, format="json").status_code
            == 404
        )
        assert client.delete(base).status_code == 404
        assert client.get("/api/v1/guides/plans/").json() == []


# --------------------------------------------------------------------------
# Journal feedback knows about the profile
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_journal_feedback_uses_life_stage_and_growth_focus(client, fake_llm, user):
    from apps.journal.feedback import generate_feedback

    set_stage(client, "senior", desired_traits=["love"])
    client.post("/api/v1/guides/plans/", {"trait": "peace"}, format="json")
    llm = fake_llm(
        reply={
            "is_spiritual": False,
            "themes": ["family"],
            "reflection": "r",
            "passages": [
                {"reference": "Philippians 4:6-7", "why": "w", "meditation": "m"}
            ],
            "christlike_step": "s",
            "growth_note": "",
            "threads": [],
        }
    )
    entry = JournalEntry(user=user, date=timezone.localdate())
    entry.set_content("The grandchildren visited today.")
    entry.save()
    feedback = generate_feedback(entry)
    prompt = llm.prompts[-1]
    assert "write at this level): senior" in prompt
    assert "peace, love" in prompt
    assert {"life_stage", "growth_focus"} <= set(feedback.inputs_used)


@pytest.mark.django_db
def test_export_includes_study_and_growth_data(client, fake_llm, user):
    from apps.guides.export import export_guides

    fake_llm(reply={"reply": "ok"})
    set_stage(client, about_me="private note")
    client.post(
        "/api/v1/guides/profile/assessment/", {"answers": {"calm": 3}}, format="json"
    )
    study = start(client)
    answer(client, study["id"])
    plan = client.post(
        "/api/v1/guides/plans/", {"trait": "peace", "why": "because"}, format="json"
    ).json()
    client.post(
        f"/api/v1/guides/plans/{plan['id']}/checkins/",
        {"rating": 3, "note": "n"},
        format="json",
    )

    data = export_guides(user)
    assert data["profile"]["about_me"] == "private note"
    assert data["assessments"][0]["answers"] == {"calm": 3}
    assert data["studies"][0]["lessons"][0]["stood_out"] == "The word guard."
    assert data["growth_plans"][0]["why"] == "because"
    assert data["growth_plans"][0]["checkins"][0]["note"] == "n"
    assert len(data["growth_plans"][0]["goals"]) == 6

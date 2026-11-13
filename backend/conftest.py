"""
Pytest configuration and fixtures for Devotional Journal backend.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create and return a test user."""
    return User.objects.create_user(
        email="testuser@example.com",
        display_name="Test User",
        language_preference="en",
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Return an authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user_factory(db):
    """Factory for creating test users."""

    def create_user(email=None, **kwargs):
        if email is None:
            import uuid

            email = f"user-{uuid.uuid4().hex[:8]}@example.com"

        defaults = {
            "display_name": "Test User",
            "language_preference": "en",
        }
        defaults.update(kwargs)
        return User.objects.create_user(email=email, **defaults)

    return create_user


@pytest.fixture
def bible_translation(db):
    """Create a test Bible translation."""
    from apps.bible.models import BibleTranslation

    return BibleTranslation.objects.create(
        code="TEST",
        name="Test Translation",
        language="en",
        is_public_domain=True,
    )


@pytest.fixture
def bible_verses(db, bible_translation):
    """Create test Bible verses."""
    from apps.bible.models import BibleVerse

    verses = []
    for i in range(1, 7):
        verses.append(
            BibleVerse.objects.create(
                translation=bible_translation,
                book="PSA",
                book_name="Psalms",
                chapter=23,
                verse=i,
                text=f"Test verse {i} text.",
            )
        )
    return verses


@pytest.fixture
def reading_plan(db):
    """Create a test reading plan."""
    from apps.plans.models import ReadingPlan, ReadingPlanDay

    plan = ReadingPlan.objects.create(
        title_en="Test Plan",
        title_es="Plan de Prueba",
        description_en="A test reading plan.",
        description_es="Un plan de lectura de prueba.",
        duration_days=7,
        category="faith",
        is_premium=False,
        is_active=True,
        is_public=True,
    )

    for day in range(1, 8):
        ReadingPlanDay.objects.create(
            plan=plan,
            day_number=day,
            passages=[{"book": "PSA", "chapter": day}],
            theme_en=f"Day {day} Theme",
            theme_es=f"Tema del Día {day}",
        )

    return plan


# --------------------------------------------------------------------------
# Fixtures for AI + scripture features. Tests never touch the network.
# --------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Fail fast (as "source unavailable") if anything tries the Bible API."""
    from apps.bible import bolls_api

    def _blocked(*args, **kwargs):
        raise bolls_api.BollsAPIError("network disabled in tests")

    monkeypatch.setattr(bolls_api, "get_chapter", _blocked)


WEB_SAMPLE = {
    ("PHP", "Philippians", 4): {
        6: "In nothing be anxious, but in everything, by prayer and petition with thanksgiving, let your requests be made known to God.",
        7: "And the peace of God, which surpasses all understanding, will guard your hearts and your thoughts in Christ Jesus.",
    },
    ("MAT", "Matthew", 11): {
        28: "Come to me, all you who labor and are heavily burdened, and I will give you rest.",
        29: "Take my yoke upon you and learn from me, for I am gentle and humble in heart; and you will find rest for your souls.",
        30: "For my yoke is easy, and my burden is light.",
    },
    ("LAM", "Lamentations", 3): {
        22: "It is because of Yahweh's loving kindnesses that we are not consumed, because his mercies don't fail.",
        23: "They are new every morning. Great is your faithfulness.",
    },
    ("1CO", "1 Corinthians", 13): {
        4: "Love is patient and is kind. Love doesn't envy. Love doesn't brag, is not proud,",
        5: "doesn't behave itself inappropriately, doesn't seek its own way, is not provoked, takes no account of evil;",
    },
    ("JAS", "James", 1): {
        5: "But if any of you lacks wisdom, let him ask of God, who gives to all liberally and without reproach, and it will be given to him.",
    },
}


@pytest.fixture
def web_bible(db):
    """A handful of real World English Bible verses in the local database."""
    from apps.bible.models import BibleTranslation, BibleVerse

    translation = BibleTranslation.objects.create(
        code="WEB", name="World English Bible", language="en", is_public_domain=True
    )
    for (code, name, chapter), verses in WEB_SAMPLE.items():
        for verse, text in verses.items():
            BibleVerse.objects.create(
                translation=translation,
                book=code,
                book_name=name,
                chapter=chapter,
                verse=verse,
                text=text,
            )
    return translation


class FakeLLM:
    """Stands in for shared.llm.LLMClient."""

    def __init__(self, reply=None, error=None, text="A short encouraging reply."):
        from shared.llm import LLMConfig

        self.reply = reply
        self.error = error
        self.text = text
        self.prompts = []
        self.config = LLMConfig(
            "ollama", "test-model", "http://ollama.test", "", "server", True
        )

    def complete_json(self, prompt, system="", **kwargs):
        self.prompts.append(prompt)
        if self.error:
            raise self.error
        return self.reply(prompt) if callable(self.reply) else self.reply

    def complete(self, prompt, system="", **kwargs):
        self.prompts.append(prompt)
        if self.error:
            raise self.error
        return self.text


@pytest.fixture
def fake_llm(monkeypatch):
    """
    Install a FakeLLM everywhere the app obtains a model client.
    Usage: llm = fake_llm(reply={...})  or  fake_llm(error=LLMUnavailable("down"))
    """

    def install(**kwargs):
        llm = FakeLLM(**kwargs)
        for target in (
            "shared.llm.get_llm",
            "apps.journal.feedback.get_llm",
            "apps.reflections.crew.agents.get_llm",
            "apps.reflections.crew.crew.get_llm",
            "apps.reflections.services.get_llm",
            "apps.reflections.reviews.get_llm",
            "apps.guides.study.get_llm",
            "apps.guides.profile.get_llm",
            "apps.guides.plans.get_llm",
        ):
            monkeypatch.setattr(target, lambda user=None, _llm=llm: _llm)
        return llm

    return install

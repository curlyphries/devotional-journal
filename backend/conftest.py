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
        email='testuser@example.com',
        display_name='Test User',
        language_preference='en',
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
            email = f'user-{uuid.uuid4().hex[:8]}@example.com'
        
        defaults = {
            'display_name': 'Test User',
            'language_preference': 'en',
        }
        defaults.update(kwargs)
        return User.objects.create_user(email=email, **defaults)
    
    return create_user


@pytest.fixture
def bible_translation(db):
    """Create a test Bible translation."""
    from apps.bible.models import BibleTranslation
    
    return BibleTranslation.objects.create(
        code='TEST',
        name='Test Translation',
        language='en',
        is_public_domain=True,
    )


@pytest.fixture
def bible_verses(db, bible_translation):
    """Create test Bible verses."""
    from apps.bible.models import BibleVerse
    
    verses = []
    for i in range(1, 7):
        verses.append(BibleVerse.objects.create(
            translation=bible_translation,
            book='PSA',
            book_name='Psalms',
            chapter=23,
            verse=i,
            text=f'Test verse {i} text.',
        ))
    return verses


@pytest.fixture
def reading_plan(db):
    """Create a test reading plan."""
    from apps.plans.models import ReadingPlan, ReadingPlanDay
    
    plan = ReadingPlan.objects.create(
        title_en='Test Plan',
        title_es='Plan de Prueba',
        description_en='A test reading plan.',
        description_es='Un plan de lectura de prueba.',
        duration_days=7,
        category='faith',
        is_premium=False,
        is_active=True,
    )
    
    for day in range(1, 8):
        ReadingPlanDay.objects.create(
            plan=plan,
            day_number=day,
            passages=[{'book': 'PSA', 'chapter': day}],
            theme_en=f'Day {day} Theme',
            theme_es=f'Tema del Día {day}',
        )
    
    return plan

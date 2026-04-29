"""
Tests for users app.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            display_name='Test User',
        )
        assert user.email == 'test@example.com'
        assert user.display_name == 'Test User'
        assert user.language_preference == 'en'
        assert user.is_active
        assert not user.is_staff

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='admin@example.com',
            display_name='Admin',
        )
        assert user.is_staff
        assert user.is_superuser

    def test_user_str(self):
        user = User.objects.create_user(email='test@example.com')
        assert str(user) == 'test@example.com'

    def test_encryption_key_salt_generated(self):
        user = User.objects.create_user(email='test@example.com')
        assert user.encryption_key_salt is not None
        assert len(user.encryption_key_salt) == 32


@pytest.mark.django_db
class TestMagicLinkRequest:
    def test_request_magic_link_success(self, api_client):
        response = api_client.post('/api/v1/auth/magic-link/request/', {
            'email': 'newuser@example.com'
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data

    def test_request_magic_link_invalid_email(self, api_client):
        response = api_client.post('/api/v1/auth/magic-link/request/', {
            'email': 'invalid-email'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserProfile:
    def test_get_profile(self, authenticated_client, user):
        response = authenticated_client.get('/api/v1/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email

    def test_update_profile(self, authenticated_client, user):
        response = authenticated_client.patch('/api/v1/me/', {
            'display_name': 'Updated Name',
            'language_preference': 'es',
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['display_name'] == 'Updated Name'
        assert response.data['language_preference'] == 'es'

    def test_get_profile_unauthenticated(self, api_client):
        response = api_client.get('/api/v1/me/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

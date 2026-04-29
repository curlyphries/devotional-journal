"""
Tests for users app: model, authentication, JWT, magic link security, API key encryption.
"""

import hashlib
from datetime import timedelta
from unittest.mock import patch

import jwt
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.authentication import generate_tokens, refresh_access_token
from apps.users.models import MagicLinkToken

User = get_user_model()


# ---------------------------------------------------------------------------
# User Model
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            display_name="Test User",
        )
        assert user.email == "test@example.com"
        assert user.display_name == "Test User"
        assert user.language_preference == "en"
        assert user.is_active
        assert not user.is_staff

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.com",
            display_name="Admin",
        )
        assert user.is_staff
        assert user.is_superuser

    def test_user_str_does_not_contain_email(self):
        """__str__ must not expose email to prevent PII leakage in logs/Sentry."""
        user = User.objects.create_user(email="secret@example.com")
        assert "secret@example.com" not in str(user)

    def test_encryption_key_salt_generated(self):
        user = User.objects.create_user(email="test@example.com")
        assert user.encryption_key_salt is not None
        assert len(bytes(user.encryption_key_salt)) == 32

    def test_two_users_have_different_salts(self):
        u1 = User.objects.create_user(email="u1@example.com")
        u2 = User.objects.create_user(email="u2@example.com")
        assert bytes(u1.encryption_key_salt) != bytes(u2.encryption_key_salt)


# ---------------------------------------------------------------------------
# AI API Key Encryption
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestAIApiKeyEncryption:
    def test_set_and_get_api_key_roundtrip(self):
        """Key must survive an encrypt → save → reload → decrypt cycle."""
        user = User.objects.create_user(email="keytest@example.com")
        raw_key = "sk-test-supersecretapikey1234"
        user.set_ai_api_key(raw_key)
        user.save()

        reloaded = User.objects.get(pk=user.pk)
        assert reloaded.get_ai_api_key() == raw_key

    def test_stored_value_is_not_plaintext(self):
        """The raw key must never appear in the database column."""
        user = User.objects.create_user(email="keytest2@example.com")
        raw_key = "sk-plaintext-should-not-appear"
        user.set_ai_api_key(raw_key)
        user.save()

        reloaded = User.objects.get(pk=user.pk)
        assert raw_key not in reloaded.ai_api_key

    def test_set_empty_key_clears_field(self):
        user = User.objects.create_user(email="keytest3@example.com")
        user.set_ai_api_key("sk-some-key")
        user.save()
        user.set_ai_api_key("")
        user.save()

        reloaded = User.objects.get(pk=user.pk)
        assert reloaded.ai_api_key == ""
        assert reloaded.get_ai_api_key() == ""

    def test_api_key_set_bool_reflects_presence(self):
        """UserSerializer.ai_api_key_set must be True when key is stored."""
        user = User.objects.create_user(email="keytest4@example.com")
        assert not bool(user.ai_api_key)
        user.set_ai_api_key("sk-present")
        user.save()
        reloaded = User.objects.get(pk=user.pk)
        assert bool(reloaded.ai_api_key)

    def test_different_users_same_raw_key_produce_different_ciphertext(self):
        """Per-user salts must mean identical keys encrypt to different ciphertext."""
        u1 = User.objects.create_user(email="enc1@example.com")
        u2 = User.objects.create_user(email="enc2@example.com")
        raw = "sk-shared-key"
        u1.set_ai_api_key(raw)
        u2.set_ai_api_key(raw)
        assert u1.ai_api_key != u2.ai_api_key


# ---------------------------------------------------------------------------
# JWT Generation & Validation
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestJWTGeneration:
    def test_generate_tokens_returns_both_tokens(self, user):
        tokens = generate_tokens(user)
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["expires_in"] == 3600

    def test_access_token_payload(self, user):
        tokens = generate_tokens(user)
        payload = jwt.decode(
            tokens["access_token"], settings.SECRET_KEY, algorithms=["HS256"]
        )
        assert payload["user_id"] == str(user.id)
        assert payload["type"] == "access"

    def test_refresh_token_payload(self, user):
        tokens = generate_tokens(user)
        payload = jwt.decode(
            tokens["refresh_token"], settings.SECRET_KEY, algorithms=["HS256"]
        )
        assert payload["user_id"] == str(user.id)
        assert payload["type"] == "refresh"

    def test_refresh_produces_new_access_token(self, user):
        tokens = generate_tokens(user)
        new_tokens = refresh_access_token(tokens["refresh_token"])
        assert "access_token" in new_tokens
        # New token is valid for the same user
        payload = jwt.decode(
            new_tokens["access_token"], settings.SECRET_KEY, algorithms=["HS256"]
        )
        assert payload["user_id"] == str(user.id)

    def test_access_token_rejected_as_refresh(self, user):
        """Using an access token as a refresh token must be rejected."""
        from rest_framework.exceptions import AuthenticationFailed

        tokens = generate_tokens(user)
        with pytest.raises(AuthenticationFailed, match="Invalid token type"):
            refresh_access_token(tokens["access_token"])

    def test_tampered_token_rejected(self, user):
        """A token with a modified signature must raise AuthenticationFailed."""
        from rest_framework.exceptions import AuthenticationFailed

        tokens = generate_tokens(user)
        bad_token = tokens["access_token"] + "tampered"
        with pytest.raises(AuthenticationFailed):
            refresh_access_token(bad_token)


# ---------------------------------------------------------------------------
# JWT Authentication Middleware (HTTP layer)
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestJWTAuthentication:
    def test_authenticated_request_succeeds(self, user):
        tokens = generate_tokens(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access_token"]}')
        response = client.get("/api/v1/auth/profile/")
        assert response.status_code == status.HTTP_200_OK

    def test_missing_token_returns_401(self):
        client = APIClient()
        response = client.get("/api/v1/auth/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_malformed_token_returns_401(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer not.a.valid.jwt")
        response = client.get("/api/v1/auth/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_wrong_scheme_returns_401(self, user):
        tokens = generate_tokens(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {tokens["access_token"]}')
        response = client.get("/api/v1/auth/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ---------------------------------------------------------------------------
# Magic Link Token Model
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestMagicLinkToken:
    def test_raw_token_not_stored(self, user):
        """Only the SHA-256 hash of the raw token must persist in the database."""
        token_obj, raw = MagicLinkToken.create_for_user(user)
        assert raw not in token_obj.token_hash
        expected_hash = hashlib.sha256(raw.encode()).hexdigest()
        assert token_obj.token_hash == expected_hash

    def test_verify_valid_token(self, user):
        token_obj, raw = MagicLinkToken.create_for_user(user)
        found = MagicLinkToken.verify_token(raw)
        assert found is not None
        assert found.pk == token_obj.pk

    def test_verify_wrong_token_returns_none(self, user):
        MagicLinkToken.create_for_user(user)
        assert MagicLinkToken.verify_token("completely-wrong-token") is None

    def test_expired_token_returns_none(self, user):
        token_obj, raw = MagicLinkToken.create_for_user(user)
        token_obj.expires_at = timezone.now() - timedelta(minutes=1)
        token_obj.save()
        assert MagicLinkToken.verify_token(raw) is None

    def test_used_token_returns_none(self, user):
        token_obj, raw = MagicLinkToken.create_for_user(user)
        token_obj.mark_used()
        assert MagicLinkToken.verify_token(raw) is None


# ---------------------------------------------------------------------------
# Magic Link Request Endpoint
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestMagicLinkRequest:
    def test_existing_user_gets_200(self, api_client, user):
        with patch("apps.users.views.send_magic_link_email") as mock_task:
            mock_task.delay = lambda *a, **kw: None
            response = api_client.post(
                "/api/v1/auth/magic-link/request/", {"email": user.email}
            )
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.data

    def test_unknown_email_still_returns_200(self, api_client):
        """Must not reveal whether an email account exists (enumeration prevention)."""
        response = api_client.post(
            "/api/v1/auth/magic-link/request/", {"email": "nobody@example.com"}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_unknown_email_does_not_create_user(self, api_client):
        api_client.post(
            "/api/v1/auth/magic-link/request/", {"email": "ghost@example.com"}
        )
        assert not User.objects.filter(email="ghost@example.com").exists()

    def test_invalid_email_format_returns_400(self, api_client):
        response = api_client.post(
            "/api/v1/auth/magic-link/request/", {"email": "not-an-email"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ---------------------------------------------------------------------------
# Magic Link Verify Endpoint
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestMagicLinkVerify:
    def test_valid_token_returns_jwt_tokens(self, api_client, user):
        token_obj, raw = MagicLinkToken.create_for_user(user)
        response = api_client.post("/api/v1/auth/magic-link/verify/", {"token": raw})
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data
        assert "refresh_token" in response.data

    def test_invalid_token_returns_400(self, api_client):
        response = api_client.post(
            "/api/v1/auth/magic-link/verify/", {"token": "invalid-token-value"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_token_cannot_be_reused(self, api_client, user):
        """A magic link token must be single-use."""
        token_obj, raw = MagicLinkToken.create_for_user(user)
        api_client.post("/api/v1/auth/magic-link/verify/", {"token": raw})
        second = api_client.post("/api/v1/auth/magic-link/verify/", {"token": raw})
        assert second.status_code == status.HTTP_400_BAD_REQUEST


# ---------------------------------------------------------------------------
# User Profile Endpoints
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestUserProfile:
    def test_get_profile(self, authenticated_client, user):
        response = authenticated_client.get("/api/v1/auth/profile/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email

    def test_profile_does_not_expose_raw_api_key(self, authenticated_client, user):
        """The serializer must never return the raw ai_api_key value."""
        user.set_ai_api_key("sk-very-secret")
        user.save()
        response = authenticated_client.get("/api/v1/auth/profile/")
        assert response.status_code == status.HTTP_200_OK
        assert "sk-very-secret" not in str(response.data)
        assert "ai_api_key" not in response.data
        assert response.data.get("ai_api_key_set") is True

    def test_update_profile(self, authenticated_client, user):
        response = authenticated_client.patch(
            "/api/v1/auth/profile/",
            {
                "display_name": "Updated Name",
                "language_preference": "es",
            },
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_profile_unauthenticated(self, api_client):
        response = api_client.get("/api/v1/auth/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ---------------------------------------------------------------------------
# Dev Login — must not be reachable in production
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestDevLogin:
    def test_dev_login_available_in_debug(self, api_client):
        """Dev login endpoint must respond when DEBUG=True (test env)."""
        assert settings.DEBUG is True  # confirm we're in test/dev mode
        response = api_client.post(
            "/api/v1/auth/dev-login/", {"email": "devuser@example.com"}
        )
        # 200 or 404 depending on whether user exists; either way not a 500
        assert response.status_code in (
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
        )

"""Security regressions for auth and AI settings."""

import logging

import pytest

from apps.users.authentication import generate_tokens
from apps.users.tasks import send_magic_link_email


@pytest.mark.django_db
class TestTokens:
    def test_refresh_token_is_not_accepted_as_an_access_token(self, api_client, user):
        tokens = generate_tokens(user)

        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['refresh_token']}")
        assert api_client.get("/api/v1/me/").status_code in (401, 403)

        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access_token']}")
        assert api_client.get("/api/v1/me/").status_code == 200

    def test_inactive_user_cannot_refresh(self, api_client, user):
        tokens = generate_tokens(user)
        user.is_active = False
        user.save()
        response = api_client.post(
            "/api/v1/auth/refresh/",
            {"refresh_token": tokens["refresh_token"]},
            format="json",
        )
        assert response.status_code in (401, 403)


@pytest.mark.django_db
class TestMagicLinkLogging:
    def test_sign_in_link_is_not_logged_by_default(
        self, user, settings, caplog, capsys
    ):
        settings.MAGIC_LINK_LOG = False
        with caplog.at_level(logging.INFO):
            send_magic_link_email(str(user.id), "super-secret-token")
        printed = capsys.readouterr()
        # (the console email backend prints the email itself; mail is not a log)
        assert "super-secret-token" not in caplog.text
        assert "SIGN-IN LINK" not in printed.out
        assert user.email not in caplog.text

    def test_operator_can_opt_in_for_a_private_instance(self, user, settings, capsys):
        settings.MAGIC_LINK_LOG = True
        send_magic_link_email(str(user.id), "token-for-private-box")
        assert "token-for-private-box" in capsys.readouterr().out


@pytest.mark.django_db
class TestAiSettings:
    def test_metadata_address_is_rejected_on_save(self, authenticated_client, user):
        response = authenticated_client.patch(
            "/api/v1/me/",
            {"ai_provider": "ollama", "ai_base_url": "http://169.254.169.254/latest"},
            format="json",
        )
        assert response.status_code == 400
        assert "ai_base_url" in response.json()["details"]
        user.refresh_from_db()
        assert user.ai_base_url == ""

    def test_private_address_needs_operator_opt_in(
        self, authenticated_client, settings
    ):
        settings.AI_ALLOW_PRIVATE_URLS = False
        blocked = authenticated_client.patch(
            "/api/v1/me/", {"ai_base_url": "http://127.0.0.1:11434"}, format="json"
        )
        assert blocked.status_code == 400

        settings.AI_ALLOW_PRIVATE_URLS = True
        allowed = authenticated_client.patch(
            "/api/v1/me/", {"ai_base_url": "http://127.0.0.1:11434"}, format="json"
        )
        assert allowed.status_code == 200
        assert allowed.json()["ai_base_url"] == "http://127.0.0.1:11434"

    def test_consent_flag_round_trips_and_defaults_off(self, authenticated_client):
        assert (
            authenticated_client.get("/api/v1/me/").json()["allow_server_cloud_ai"]
            is False
        )
        response = authenticated_client.patch(
            "/api/v1/me/", {"allow_server_cloud_ai": True}, format="json"
        )
        assert response.json()["allow_server_cloud_ai"] is True

    def test_local_only_server_refuses_cloud_providers(
        self, authenticated_client, settings
    ):
        settings.AI_LOCAL_ONLY = True
        response = authenticated_client.patch(
            "/api/v1/me/",
            {"ai_provider": "openai", "ai_api_key": "sk-x"},
            format="json",
        )
        assert response.status_code == 400
        assert "ai_provider" in response.json()["details"]

    def test_api_key_is_never_returned(self, authenticated_client):
        response = authenticated_client.patch(
            "/api/v1/me/",
            {"ai_provider": "openai", "ai_api_key": "sk-very-secret"},
            format="json",
        )
        assert response.status_code == 200
        assert "sk-very-secret" not in response.content.decode()
        assert response.json()["ai_api_key_set"] is True

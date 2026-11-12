"""Tests for the API error envelope, request ids, health and the mesh guard."""

import pytest
from django.test import RequestFactory

from apps.users.middleware import MeshOnlyMiddleware

ENVELOPE_KEYS = {"error", "code", "suggestion", "request_id"}


@pytest.mark.django_db
class TestErrorEnvelope:
    def test_validation_error_names_the_field(self, authenticated_client):
        response = authenticated_client.post("/api/v1/journal/", {}, format="json")
        body = response.json()
        assert response.status_code == 400
        assert ENVELOPE_KEYS <= set(body)
        assert body["code"] == "VALIDATION_ERROR"
        assert "date" in body["details"] and "content" in body["details"]
        assert body["error"]  # a readable sentence, not a nested structure
        assert isinstance(body["error"], str)

    def test_unauthenticated(self, api_client):
        body = api_client.get("/api/v1/journal/").json()
        assert body["code"] in ("NOT_AUTHENTICATED", "PERMISSION_DENIED")
        assert body["suggestion"]

    def test_views_that_build_their_own_error_get_the_envelope_too(
        self, authenticated_client
    ):
        response = authenticated_client.get(
            "/api/v1/journal/00000000-0000-0000-0000-000000000000/"
        )
        body = response.json()
        assert response.status_code == 404
        assert body["error"] == "Entry not found"
        assert body["code"] == "NOT_FOUND"
        assert body["request_id"] == response["X-Request-ID"]

    def test_unexpected_exception_is_a_coded_500_without_internals(
        self, authenticated_client, monkeypatch
    ):
        from apps.journal import views

        def boom(user):
            raise RuntimeError("secret internal detail")

        monkeypatch.setattr(views, "theme_summary", boom)
        response = authenticated_client.get("/api/v1/journal/themes/")
        body = response.json()
        assert response.status_code == 500
        assert body["code"] == "SERVER_ERROR"
        assert "secret internal detail" not in response.content.decode()
        assert len(body["request_id"]) == 12

    def test_every_response_has_a_request_id(self, authenticated_client):
        first = authenticated_client.get("/api/v1/journal/")
        second = authenticated_client.get("/api/v1/journal/")
        assert first["X-Request-ID"] and first["X-Request-ID"] != second["X-Request-ID"]

    def test_bad_integer_params_are_400_not_500(self, authenticated_client):
        response = authenticated_client.post(
            "/api/v1/plans/generate/",
            {"topic": "x", "duration_days": "abc"},
            format="json",
        )
        assert response.status_code == 400
        assert response.json()["code"] == "VALIDATION_ERROR"


@pytest.mark.django_db
def test_health_reports_database_and_cache(api_client):
    response = api_client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "checks": {"database": True, "cache": True},
    }


class TestMeshOnly:
    def _call(self, settings, remote_addr, path="/api/v1/journal/", **headers):
        settings.MESH_ONLY = True
        middleware = MeshOnlyMiddleware(lambda request: "passed")
        request = RequestFactory().get(path, REMOTE_ADDR=remote_addr, **headers)
        return middleware(request)

    def test_mesh_and_loopback_clients_pass(self, settings):
        assert self._call(settings, "100.101.102.103") == "passed"
        assert self._call(settings, "127.0.0.1") == "passed"
        assert self._call(settings, "fd7a:115c:a1e0::1") == "passed"

    def test_outside_addresses_are_refused(self, settings):
        for address in ("8.8.8.8", "192.168.1.5", "100.63.255.255", "100.128.0.1", ""):
            response = self._call(settings, address)
            assert response.status_code == 403, address

    def test_real_ip_header_is_believed_only_from_our_proxy(self, settings):
        # From the nginx container: the header carries the real client.
        assert (
            self._call(settings, "172.18.0.5", HTTP_X_REAL_IP="100.101.102.103")
            == "passed"
        )
        assert (
            self._call(settings, "172.18.0.5", HTTP_X_REAL_IP="8.8.8.8").status_code
            == 403
        )
        # From anyone else: a forged header changes nothing.
        assert (
            self._call(
                settings, "8.8.8.8", HTTP_X_REAL_IP="100.101.102.103"
            ).status_code
            == 403
        )
        # Proxy with no header is not a mesh client.
        assert self._call(settings, "172.18.0.5").status_code == 403

    def test_health_probe_is_exempt_and_off_by_default(self, settings):
        assert self._call(settings, "172.18.0.1", path="/api/v1/health/") == "passed"
        settings.MESH_ONLY = False
        middleware = MeshOnlyMiddleware(lambda request: "passed")
        assert middleware(RequestFactory().get("/", REMOTE_ADDR="8.8.8.8")) == "passed"

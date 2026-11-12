"""Tests for shared.llm: provider resolution, consent, URL checks, error mapping."""

import httpx
import pytest

from shared import llm as llm_module
from shared.llm import (
    AIUrlNotAllowed,
    LLMBadResponse,
    LLMClient,
    LLMConfig,
    LLMConsentRequired,
    LLMLocalOnly,
    LLMNotConfigured,
    LLMTimeout,
    LLMUnavailable,
    ai_status,
    extract_json,
    resolve_llm_config,
    validate_ai_base_url,
)


@pytest.fixture
def fake_dns(monkeypatch):
    """Resolve test host names without touching DNS."""
    table = {
        "ollama.lan": "192.168.1.20",
        "mesh-box": "100.101.102.103",
        "public.example": "93.184.216.34",
        "rebind.example": "127.0.0.1",
        "metadata.example": "169.254.169.254",
    }

    def fake_getaddrinfo(host, *args, **kwargs):
        import ipaddress
        import socket

        try:
            ipaddress.ip_address(host)
            address = host
        except ValueError:
            if host not in table:
                raise socket.gaierror("unknown host")
            address = table[host]
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, 0))]

    monkeypatch.setattr(llm_module.socket, "getaddrinfo", fake_getaddrinfo)


@pytest.mark.django_db
class TestResolveConfig:
    def test_default_is_the_servers_local_ollama(self, user, settings):
        settings.LLM_BACKEND = "ollama"
        config = resolve_llm_config(user)
        assert (config.provider, config.source, config.local) == (
            "ollama",
            "server",
            True,
        )

    def test_server_cloud_default_needs_the_persons_consent(self, user, settings):
        settings.LLM_BACKEND = "anthropic"
        settings.ANTHROPIC_API_KEY = "sk-ant-server-key"
        with pytest.raises(LLMConsentRequired) as excinfo:
            resolve_llm_config(user)
        assert excinfo.value.code == "AI_CONSENT_REQUIRED"
        assert excinfo.value.suggestion

        user.allow_server_cloud_ai = True
        config = resolve_llm_config(user)
        assert (config.provider, config.source, config.local) == (
            "anthropic",
            "server",
            False,
        )

    def test_own_cloud_provider_is_used_without_extra_consent(self, user, settings):
        settings.LLM_BACKEND = "ollama"
        user.ai_provider = "openai"
        user.set_ai_api_key("sk-user-key")
        config = resolve_llm_config(user)
        assert (config.provider, config.source, config.local) == (
            "openai",
            "user",
            False,
        )
        assert config.api_key == "sk-user-key"
        assert "api_key" not in config.public()

    def test_chosen_provider_without_a_key_does_not_fall_back(self, user, settings):
        settings.LLM_BACKEND = "ollama"
        user.ai_provider = "anthropic"
        with pytest.raises(LLMNotConfigured):
            resolve_llm_config(user)

    def test_local_only_refuses_cloud_for_everyone(self, user, settings):
        settings.AI_LOCAL_ONLY = True
        user.ai_provider = "openai"
        user.set_ai_api_key("sk-user-key")
        with pytest.raises(LLMLocalOnly):
            resolve_llm_config(user)

        user.ai_provider = "none"
        settings.LLM_BACKEND = "ollama"
        assert resolve_llm_config(user).local is True

    def test_undecryptable_stored_key_is_never_sent_as_a_key(self, user):
        user.ai_provider = "openai"
        user.ai_api_key = "not-encrypted-legacy-value"
        assert user.get_ai_api_key() == ""
        with pytest.raises(LLMNotConfigured):
            resolve_llm_config(user)

    def test_ai_status_never_raises_and_explains(self, user, settings):
        settings.LLM_BACKEND = "anthropic"
        settings.ANTHROPIC_API_KEY = "sk-ant-server-key"
        status = ai_status(user)
        assert status["reachable"] is False
        assert status["consent_required"] is True
        assert status["code"] == "AI_CONSENT_REQUIRED"
        assert status["suggestion"]


class TestBaseUrlValidation:
    def test_rejects_bad_schemes_and_credentials(self, fake_dns):
        for url in (
            "ftp://public.example",
            "file:///etc/passwd",
            "public.example",
            "http://user:pw@public.example",
        ):
            with pytest.raises(AIUrlNotAllowed):
                validate_ai_base_url(url)

    def test_metadata_and_link_local_are_always_blocked(self, fake_dns, settings):
        settings.AI_ALLOW_PRIVATE_URLS = True
        for url in ("http://169.254.169.254/latest", "http://metadata.example/"):
            with pytest.raises(AIUrlNotAllowed):
                validate_ai_base_url(url)

    def test_private_addresses_blocked_unless_operator_allows(self, fake_dns, settings):
        settings.AI_ALLOW_PRIVATE_URLS = False
        for url in (
            "http://127.0.0.1:11434",
            "http://192.168.1.20:11434",
            "http://ollama.lan:11434",
            "http://rebind.example/",  # public-looking name that resolves to loopback
            "http://2130706433/",  # 127.0.0.1 as a decimal integer
        ):
            with pytest.raises(AIUrlNotAllowed):
                validate_ai_base_url(url)

        settings.AI_ALLOW_PRIVATE_URLS = True
        assert (
            validate_ai_base_url("http://ollama.lan:11434/")
            == "http://ollama.lan:11434"
        )

    def test_public_address_allowed_and_unknown_host_rejected(self, fake_dns, settings):
        settings.AI_ALLOW_PRIVATE_URLS = False
        assert (
            validate_ai_base_url("https://public.example/v1")
            == "https://public.example/v1"
        )
        with pytest.raises(AIUrlNotAllowed):
            validate_ai_base_url("https://does-not-exist.example")
        assert validate_ai_base_url("") == ""


class TestExtractJson:
    def test_plain_fenced_and_embedded(self):
        assert extract_json('{"a": 1}') == {"a": 1}
        assert extract_json('```json\n{"a": 1}\n```') == {"a": 1}
        assert extract_json('Sure! Here it is: {"a": [1, 2]} Hope that helps.') == {
            "a": [1, 2]
        }
        assert extract_json("[1, 2]") == [1, 2]

    def test_garbage_raises(self):
        for text in ("", "no json here", '{"a": '):
            with pytest.raises(ValueError):
                extract_json(text)


def _client(provider="ollama"):
    return LLMClient(
        LLMConfig(provider, "m", "http://ollama.test", "key", "server", True)
    )


class TestClientErrors:
    def _post(self, monkeypatch, handler):
        monkeypatch.setattr(llm_module.httpx, "post", handler)

    def test_success(self, monkeypatch):
        captured = {}

        def handler(url, **kwargs):
            captured["url"], captured["json"] = url, kwargs["json"]
            return httpx.Response(
                200,
                json={"response": ' {"ok": true} '},
                request=httpx.Request("POST", url),
            )

        self._post(monkeypatch, handler)
        assert _client().complete_json("hi", "sys") == {"ok": True}
        assert captured["url"] == "http://ollama.test/api/generate"
        assert (
            captured["json"]["format"] == "json" and captured["json"]["system"] == "sys"
        )

    def test_unreachable_timeout_and_statuses_are_typed(self, monkeypatch):
        def refuse(url, **kwargs):
            raise httpx.ConnectError("refused")

        self._post(monkeypatch, refuse)
        with pytest.raises(LLMUnavailable) as excinfo:
            _client().complete("hi")
        assert "ollama.test" in excinfo.value.suggestion

        def slow(url, **kwargs):
            raise httpx.ReadTimeout("slow")

        self._post(monkeypatch, slow)
        with pytest.raises(LLMTimeout):
            _client().complete("hi")

        def status(code):
            def handler(url, **kwargs):
                return httpx.Response(code, json={}, request=httpx.Request("POST", url))

            return handler

        self._post(monkeypatch, status(404))
        with pytest.raises(LLMNotConfigured) as excinfo:
            _client().complete("hi")
        assert "ollama pull m" in excinfo.value.suggestion

        self._post(monkeypatch, status(401))
        with pytest.raises(LLMNotConfigured):
            _client("openai").complete("hi")

        self._post(monkeypatch, status(500))
        with pytest.raises(LLMUnavailable):
            _client().complete("hi")

    def test_empty_or_non_json_reply_is_a_bad_response(self, monkeypatch):
        def reply(text):
            def handler(url, **kwargs):
                return httpx.Response(
                    200, json={"response": text}, request=httpx.Request("POST", url)
                )

            return handler

        self._post(monkeypatch, reply(""))
        with pytest.raises(LLMBadResponse):
            _client().complete("hi")

        self._post(monkeypatch, reply("I cannot do that."))
        with pytest.raises(LLMBadResponse):
            _client().complete_json("hi")

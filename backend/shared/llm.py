"""
The one place the app talks to a language model.

Every AI feature goes through `get_llm(user)`. That single path decides:

  * which provider handles a request (the user's own choice first, then the
    server default),
  * whether the request is *allowed* to leave the network (a user's text is
    never sent to a server-configured cloud provider unless they opted in;
    with AI_LOCAL_ONLY nothing leaves the network at all), and
  * how failures surface (typed errors with a code and a suggestion — never a
    silent canned answer).
"""

import ipaddress
import json
import logging
import re
import socket
import time
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import urlparse

import httpx
from django.conf import settings

from .errors import AppError

logger = logging.getLogger(__name__)

CLOUD_PROVIDERS = {"anthropic", "openai", "openrouter"}
PROVIDER_URLS = {
    "openai": "https://api.openai.com/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "anthropic": "https://api.anthropic.com/v1",
}
PROVIDER_LABELS = {
    "ollama": "Ollama",
    "anthropic": "Anthropic",
    "openai": "OpenAI",
    "openrouter": "OpenRouter",
    "custom": "your custom AI server",
}


class LLMError(AppError):
    status_code = 503
    code = "AI_UNAVAILABLE"


class LLMUnavailable(LLMError):
    code = "AI_UNAVAILABLE"


class LLMTimeout(LLMError):
    code = "AI_TIMEOUT"


class LLMNotConfigured(LLMError):
    code = "AI_NOT_CONFIGURED"


class LLMConsentRequired(LLMError):
    status_code = 403
    code = "AI_CONSENT_REQUIRED"


class LLMLocalOnly(LLMError):
    status_code = 403
    code = "AI_LOCAL_ONLY"


class LLMBadResponse(LLMError):
    status_code = 502
    code = "AI_BAD_RESPONSE"


class AIUrlNotAllowed(AppError):
    status_code = 400
    code = "AI_URL_NOT_ALLOWED"


# --------------------------------------------------------------------------
# Base-URL validation (SSRF guard)
# --------------------------------------------------------------------------


def _is_private(addr: ipaddress._BaseAddress) -> bool:
    return addr.is_private or addr.is_loopback


def _never_allowed(addr: ipaddress._BaseAddress) -> bool:
    # Link-local covers cloud metadata endpoints (169.254.169.254, fe80::/10).
    return (
        addr.is_link_local
        or addr.is_multicast
        or addr.is_unspecified
        or (addr.is_reserved and not addr.is_loopback)
    )


def _resolve(host: str) -> list:
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except (socket.gaierror, UnicodeError) as exc:
        raise AIUrlNotAllowed(
            f"The AI server address '{host}' could not be found."
        ) from exc
    return [ipaddress.ip_address(info[4][0].split("%")[0]) for info in infos]


def validate_ai_base_url(url: str) -> str:
    """
    Check a user-supplied AI server URL and return it normalised.

    The host name is resolved and every address it points at is checked, so a
    DNS name (or an odd spelling like http://2130706433/) cannot be used to
    reach something it should not. Addresses on a private network are allowed
    only when the operator set AI_ALLOW_PRIVATE_URLS (self-hosted / mesh
    installs, where the model server legitimately lives on the LAN).
    """
    url = (url or "").strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise AIUrlNotAllowed(
            "The AI server address must start with http:// or https://."
        )
    if parsed.username or parsed.password:
        raise AIUrlNotAllowed(
            "The AI server address must not contain a username or password."
        )

    allow_private = getattr(settings, "AI_ALLOW_PRIVATE_URLS", False)
    for addr in _resolve(parsed.hostname):
        if _never_allowed(addr):
            raise AIUrlNotAllowed("That AI server address is not allowed.")
        if _is_private(addr) and not allow_private:
            raise AIUrlNotAllowed(
                "That address is on a private network, which this server does not allow.",
                suggestion=(
                    "Use a public https address, or ask the administrator to set "
                    "AI_ALLOW_PRIVATE_URLS=true for a self-hosted install."
                ),
            )
    return url.rstrip("/")


def is_local_url(url: str) -> bool:
    """True when the URL points at this machine or a private/mesh network."""
    host = urlparse(url or "").hostname
    if not host:
        return False
    try:
        addrs = _resolve(host)
    except AppError:
        return False
    cgnat = ipaddress.ip_network("100.64.0.0/10")  # Tailscale / mesh range
    return bool(addrs) and all(_is_private(a) or a in cgnat for a in addrs)


# --------------------------------------------------------------------------
# Provider resolution
# --------------------------------------------------------------------------


@dataclass
class LLMConfig:
    provider: str
    model: str
    base_url: str
    api_key: str = ""
    source: str = "server"  # "user" (their own settings) | "server" (operator default)
    local: bool = True  # request stays on this machine / private network

    @property
    def label(self) -> str:
        return PROVIDER_LABELS.get(self.provider, self.provider)

    def public(self) -> dict:
        """Safe to store and show: never includes the key."""
        return {
            "provider": self.provider,
            "model": self.model,
            "local": self.local,
            "source": self.source,
        }


def _local_only() -> bool:
    return bool(getattr(settings, "AI_LOCAL_ONLY", False))


def _user_config(user) -> Optional[LLMConfig]:
    provider = (getattr(user, "ai_provider", "") or "none").lower()
    if provider in ("", "none"):
        return None

    model = getattr(user, "ai_model", "") or ""
    base_url = getattr(user, "ai_base_url", "") or ""

    if provider == "ollama":
        url = validate_ai_base_url(base_url) if base_url else settings.OLLAMA_BASE_URL
        return LLMConfig(
            provider="ollama",
            model=model or settings.OLLAMA_MODEL,
            base_url=url.rstrip("/"),
            source="user",
            local=True if not base_url else is_local_url(url),
        )

    api_key = user.get_ai_api_key() if hasattr(user, "get_ai_api_key") else ""
    if not api_key:
        raise LLMNotConfigured(
            f"{PROVIDER_LABELS.get(provider, provider)} is selected but no API key is saved."
        )

    if provider == "custom":
        if not base_url:
            raise LLMNotConfigured("A custom AI provider needs a server address.")
        url = validate_ai_base_url(base_url)
        if not model:
            raise LLMNotConfigured("A custom AI provider needs a model name.")
        return LLMConfig("custom", model, url, api_key, "user", is_local_url(url))

    if provider in CLOUD_PROVIDERS:
        default_model = (
            settings.ANTHROPIC_MODEL if provider == "anthropic" else "gpt-4o-mini"
        )
        return LLMConfig(
            provider,
            model or default_model,
            PROVIDER_URLS[provider],
            api_key,
            "user",
            False,
        )

    raise LLMNotConfigured(f"Unknown AI provider '{provider}'.")


def _server_config(user) -> LLMConfig:
    backend = (getattr(settings, "LLM_BACKEND", "ollama") or "ollama").lower()

    if backend == "anthropic":
        api_key = getattr(settings, "ANTHROPIC_API_KEY", "") or ""
        if not api_key:
            raise LLMNotConfigured(
                "The server's AI provider is not set up.",
                suggestion=(
                    "Configure your own provider in Settings → AI Provider, or ask the "
                    "administrator to set ANTHROPIC_API_KEY."
                ),
            )
        if not getattr(user, "allow_server_cloud_ai", False):
            raise LLMConsentRequired(
                "This server's default AI runs in the cloud (Anthropic), and you have "
                "not allowed your text to be sent there."
            )
        return LLMConfig(
            "anthropic",
            settings.ANTHROPIC_MODEL,
            PROVIDER_URLS["anthropic"],
            api_key,
            "server",
            False,
        )

    url = settings.OLLAMA_BASE_URL.rstrip("/")
    return LLMConfig("ollama", settings.OLLAMA_MODEL, url, "", "server", True)


def resolve_llm_config(user=None) -> LLMConfig:
    """
    Decide which provider serves this user. Raises an LLMError subclass (with a
    code and a suggestion) rather than quietly falling back to another provider.
    """
    config = _user_config(user) if user is not None else None
    if config is None:
        config = _server_config(user)
    if _local_only() and not config.local:
        raise LLMLocalOnly(
            f"{config.label} is a cloud service, and this server only allows AI on its own network."
        )
    return config


# --------------------------------------------------------------------------
# Client
# --------------------------------------------------------------------------


def extract_json(text: str) -> Any:
    """Parse the first JSON object/array in a model reply (tolerates code fences)."""
    if not text:
        raise ValueError("empty response")
    cleaned = re.sub(
        r"^```[a-zA-Z]*\s*|\s*```\s*$", "", text.strip(), flags=re.MULTILINE
    )
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    starts = [i for i in (cleaned.find("{"), cleaned.find("[")) if i >= 0]
    if not starts:
        raise ValueError("no JSON found")
    start = min(starts)
    closer = "}" if cleaned[start] == "{" else "]"
    end = cleaned.rfind(closer)
    if end <= start:
        raise ValueError("unterminated JSON")
    fragment = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", cleaned[start : end + 1])
    return json.loads(fragment)


class LLMClient:
    """Minimal provider-agnostic text completion."""

    def __init__(self, config: LLMConfig):
        self.config = config

    # -- public ------------------------------------------------------------

    def complete(
        self,
        prompt: str,
        system: str = "",
        max_tokens: int = 800,
        temperature: float = 0.7,
        json_mode: bool = False,
        timeout: float = 90.0,
    ) -> str:
        started = time.monotonic()
        try:
            if self.config.provider == "ollama":
                text = self._ollama(
                    prompt, system, max_tokens, temperature, json_mode, timeout
                )
            elif self.config.provider == "anthropic":
                text = self._anthropic(prompt, system, max_tokens, temperature, timeout)
            else:
                text = self._openai(prompt, system, max_tokens, temperature, timeout)
        except httpx.TimeoutException as exc:
            raise LLMTimeout(
                f"{self.config.label} did not answer within {int(timeout)} seconds."
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise self._status_error(exc) from exc
        except httpx.HTTPError as exc:
            raise LLMUnavailable(
                f"Could not reach {self.config.label}.",
                suggestion=self._unreachable_hint(),
            ) from exc
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMBadResponse(
                f"{self.config.label} returned a reply in an unexpected format."
            ) from exc

        text = (text or "").strip()
        if not text:
            raise LLMBadResponse(f"{self.config.label} returned an empty reply.")
        logger.info(
            "llm call provider=%s model=%s source=%s ms=%d",
            self.config.provider,
            self.config.model,
            self.config.source,
            int((time.monotonic() - started) * 1000),
        )
        return text

    def complete_json(self, prompt: str, system: str = "", **kwargs) -> Any:
        kwargs.setdefault("temperature", 0.4)
        text = self.complete(prompt, system, json_mode=True, **kwargs)
        try:
            return extract_json(text)
        except ValueError as exc:
            raise LLMBadResponse(
                f"{self.config.label} did not return the structured answer that was asked for."
            ) from exc

    def health(self) -> dict:
        """Cheap reachability check. Never raises."""
        info = {**self.config.public(), "reachable": False, "detail": ""}
        if self.config.provider != "ollama":
            info["reachable"] = bool(self.config.api_key)
            return info
        try:
            response = httpx.get(f"{self.config.base_url}/api/tags", timeout=4.0)
            response.raise_for_status()
            models = [m.get("name", "") for m in response.json().get("models", [])]
        except Exception as exc:  # noqa: BLE001 - any failure means "not reachable"
            info["detail"] = f"Could not reach Ollama at {self.config.base_url}."
            logger.info("ollama health check failed: %s", exc.__class__.__name__)
            return info
        if not any(self.config.model in name for name in models):
            info["detail"] = (
                f"Ollama is running but the model '{self.config.model}' is not installed. "
                f"Run: ollama pull {self.config.model}"
            )
            return info
        info["reachable"] = True
        return info

    # -- providers ---------------------------------------------------------

    def _ollama(self, prompt, system, max_tokens, temperature, json_mode, timeout):
        body = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        if system:
            body["system"] = system
        if json_mode:
            body["format"] = "json"
        response = httpx.post(
            f"{self.config.base_url}/api/generate", json=body, timeout=timeout
        )
        response.raise_for_status()
        return response.json().get("response", "")

    def _anthropic(self, prompt, system, max_tokens, temperature, timeout):
        body = {
            "model": self.config.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            body["system"] = system
        response = httpx.post(
            f"{self.config.base_url}/messages",
            headers={
                "x-api-key": self.config.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=body,
            timeout=timeout,
        )
        response.raise_for_status()
        return "".join(
            block.get("text", "")
            for block in response.json()["content"]
            if block.get("type") == "text"
        )

    def _openai(self, prompt, system, max_tokens, temperature, timeout):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = httpx.post(
            f"{self.config.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.config.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages,
            },
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    # -- error mapping -----------------------------------------------------

    def _unreachable_hint(self) -> str:
        if self.config.provider == "ollama":
            return (
                f"Check that Ollama is running at {self.config.base_url} and reachable "
                "from the server (Settings → AI Provider → Test connection)."
            )
        return "Check the server's internet connection, then try again."

    def _status_error(self, exc: httpx.HTTPStatusError) -> LLMError:
        code = exc.response.status_code
        label = self.config.label
        if code in (401, 403):
            return LLMNotConfigured(
                f"{label} rejected the API key.",
                suggestion="Re-enter your API key in Settings → AI Provider.",
            )
        if code == 404:
            hint = (
                f"Run: ollama pull {self.config.model}"
                if self.config.provider == "ollama"
                else "Check the model name in Settings → AI Provider."
            )
            return LLMNotConfigured(
                f"{label} does not have the model '{self.config.model}'.",
                suggestion=hint,
            )
        if code == 429:
            return LLMUnavailable(
                f"{label} is rate-limiting requests or the account is out of credit.",
                suggestion="Wait a minute and try again, or check your plan with the provider.",
            )
        return LLMUnavailable(f"{label} returned an error ({code}).")


def get_llm(user=None) -> LLMClient:
    """The LLM client for this user. Raises LLMError if none may be used."""
    return LLMClient(resolve_llm_config(user))


def ai_status(user=None) -> dict:
    """Describe which AI would serve this user and whether it can, without raising."""
    try:
        client = get_llm(user)
    except AppError as exc:
        return {
            "backend": (getattr(user, "ai_provider", "") or "none"),
            "model": None,
            "reachable": False,
            "configured": False,
            "source": "user",
            "local": False,
            "consent_required": exc.code == "AI_CONSENT_REQUIRED",
            "code": exc.code,
            "message": exc.message,
            "suggestion": exc.suggestion,
        }
    health = client.health()
    reachable = health["reachable"]
    return {
        "backend": client.config.provider,
        "model": client.config.model,
        "reachable": reachable,
        "configured": reachable,
        "source": client.config.source,
        "local": client.config.local,
        "consent_required": False,
        "code": None if reachable else "AI_UNAVAILABLE",
        "message": health["detail"] or None,
        "suggestion": (
            None if reachable else (health["detail"] or client._unreachable_hint())
        ),
    }

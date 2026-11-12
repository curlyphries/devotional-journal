"""
One error shape for the whole API, plus request ids.

Every 4xx/5xx JSON response looks like:

    {
      "error": "Human-readable description of what went wrong",
      "code": "AI_UNAVAILABLE",
      "suggestion": "What the person can do about it",
      "request_id": "3f9c2a1b7d4e",
      "details": {"field": ["..."]}          # validation errors only
    }

`request_id` is also sent as the X-Request-ID response header and stamped on
every log line for that request, so a reference quoted by a user leads
straight to the server log. Codes are documented in docs/TROUBLESHOOTING.md.
"""

import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions as drf_exceptions
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .request_id import get_request_id

logger = logging.getLogger(__name__)

SUGGESTIONS = {
    "VALIDATION_ERROR": "Check the highlighted fields and try again.",
    "NOT_AUTHENTICATED": "Sign in again.",
    "PERMISSION_DENIED": "You do not have access to this item.",
    "NOT_FOUND": "It may have been deleted. Go back and refresh the list.",
    "RATE_LIMITED": "Wait a few minutes before trying again.",
    "SERVER_ERROR": (
        "Try again. If it keeps happening, report it with the reference shown — "
        "the server log has the details under that reference."
    ),
    "AI_UNAVAILABLE": (
        "Make sure your AI provider is running and reachable "
        "(Settings → AI Provider → Test connection)."
    ),
    "AI_TIMEOUT": (
        "The model took too long. Try again, or choose a smaller/faster model "
        "in Settings → AI Provider."
    ),
    "AI_NOT_CONFIGURED": "Finish setting up your provider in Settings → AI Provider.",
    "AI_CONSENT_REQUIRED": (
        "This server's default AI runs in the cloud. Allow it in Settings → AI "
        "Provider, or configure your own (local) provider there."
    ),
    "AI_BAD_RESPONSE": (
        "The model returned something unusable. Try again; if it repeats, use a "
        "larger model in Settings → AI Provider."
    ),
    "AI_URL_NOT_ALLOWED": "Use the address of your own AI server (http or https).",
    "AI_LOCAL_ONLY": (
        "This server only allows AI that runs on its own network. Choose Ollama "
        "in Settings → AI Provider."
    ),
    "SCRIPTURE_UNAVAILABLE": (
        "The Bible text source could not be reached. Try again shortly; an "
        "administrator can load a translation locally (see docs/TROUBLESHOOTING.md)."
    ),
}

_STATUS_CODES = {
    400: "VALIDATION_ERROR",
    401: "NOT_AUTHENTICATED",
    403: "PERMISSION_DENIED",
    404: "NOT_FOUND",
    405: "VALIDATION_ERROR",
    422: "VALIDATION_ERROR",
    429: "RATE_LIMITED",
}


class AppError(drf_exceptions.APIException):
    """Raise anywhere in a request to return a coded error with a suggestion."""

    status_code = status.HTTP_400_BAD_REQUEST
    code = "VALIDATION_ERROR"

    def __init__(self, message=None, code=None, suggestion=None, status_code=None):
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        self.message = message or "The request could not be completed."
        self.suggestion = suggestion or SUGGESTIONS.get(self.code)
        super().__init__(detail=self.message)

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "suggestion": self.suggestion,
        }


def _first_message(detail) -> str:
    """Pull one readable sentence out of DRF's nested validation structure."""
    if isinstance(detail, dict):
        for key, value in detail.items():
            message = _first_message(value)
            if message:
                if key in ("non_field_errors", "detail", "error"):
                    return message
                return f"{str(key).replace('_', ' ').capitalize()}: {message}"
        return ""
    if isinstance(detail, (list, tuple)):
        for item in detail:
            message = _first_message(item)
            if message:
                return message
        return ""
    return str(detail) if detail is not None else ""


def envelope(code: str, message: str, suggestion=None, details=None) -> dict:
    body = {
        "error": message,
        "code": code,
        "suggestion": suggestion or SUGGESTIONS.get(code),
        "request_id": get_request_id(),
    }
    if details:
        body["details"] = details
    return body


def error_response(code, message, http_status, suggestion=None, details=None):
    return Response(envelope(code, message, suggestion, details), status=http_status)


def exception_handler(exc, context):
    """DRF EXCEPTION_HANDLER: every raised error leaves in the envelope shape."""
    if isinstance(exc, AppError):
        response = Response(
            envelope(exc.code, exc.message, exc.suggestion), status=exc.status_code
        )
        if exc.status_code >= 500:
            logger.warning("%s: %s", exc.code, exc.message)
        return response

    if isinstance(exc, Http404):
        exc = drf_exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = drf_exceptions.PermissionDenied()

    # Imported here: rest_framework.views reads the renderer setting, which
    # points back at this module.
    from rest_framework.views import exception_handler as drf_exception_handler

    response = drf_exception_handler(exc, context)

    if response is None:
        # Anything unexpected: log it with the request id, never leak internals.
        view = context.get("view")
        logger.exception(
            "Unhandled error in %s", view.__class__.__name__ if view else "request"
        )
        return Response(
            envelope(
                "SERVER_ERROR", "Something went wrong on the server. Nothing was lost."
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    code = _STATUS_CODES.get(response.status_code, "SERVER_ERROR")
    details = None
    if isinstance(exc, drf_exceptions.ValidationError):
        code = "VALIDATION_ERROR"
        if isinstance(response.data, dict):
            details = response.data
        message = _first_message(response.data) or "Some of the input is not valid."
    elif isinstance(exc, drf_exceptions.Throttled):
        wait = int(exc.wait) if exc.wait else None
        message = "Too many requests."
        suggestion = (
            f"Try again in about {max(1, round(wait / 60))} minute(s)."
            if wait
            else None
        )
        response.data = envelope(code, message, suggestion)
        return response
    else:
        message = _first_message(response.data) or "The request could not be completed."

    response.data = envelope(code, message, details=details)
    return response


class EnvelopeJSONRenderer(JSONRenderer):
    """
    Views that build their own `Response({"error": ...}, status=4xx)` get the
    same envelope: a code, a suggestion and the request id are filled in.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = (renderer_context or {}).get("response")
        if (
            response is not None
            and response.status_code >= 400
            and isinstance(data, dict)
            and "request_id" not in data
        ):
            code = data.get("code")
            if not isinstance(code, str):
                code = _STATUS_CODES.get(response.status_code, "SERVER_ERROR")
            message = ""
            for key in ("error", "detail", "message"):
                if isinstance(data.get(key), str) and data[key]:
                    message = data[key]
                    break
            if not message:
                message = _first_message(data) or "The request could not be completed."
            suggestion = data.get("suggestion")
            data = {
                **data,
                **envelope(code, message, suggestion),
            }
        return super().render(data, accepted_media_type, renderer_context)

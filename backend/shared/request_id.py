"""
Request ids: one short id per request, on the response (X-Request-ID) and on
every log line, so a reference a person quotes leads straight to the log.

Kept free of Django/DRF imports so the logging config can load it at startup.
"""

import contextvars
import logging
import uuid

_request_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)


def get_request_id() -> str:
    return _request_id.get()


class RequestIDMiddleware:
    """Assign each request an id; expose it on the response and to logging."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = uuid.uuid4().hex[:12]
        request.request_id = request_id
        token = _request_id.set(request_id)
        try:
            response = self.get_response(request)
        finally:
            _request_id.reset(token)
        response["X-Request-ID"] = request_id
        return response


class RequestIDLogFilter(logging.Filter):
    """Adds `request_id` to every log record (use {request_id} in formats)."""

    def filter(self, record):
        record.request_id = get_request_id()
        return True

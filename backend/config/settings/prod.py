"""
Production settings for Devotional Journal.
"""

import dj_database_url

from .base import *

try:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    _sentry_available = True
except ImportError:
    _sentry_available = False

DEBUG = False

ALLOWED_HOSTS = [h for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()]

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "true").lower() == "true"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS - restrict to known origins
_cors_origins = os.environ.get("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [o for o in _cors_origins.split(",") if o.strip()]

# Cache (Redis — shared across all gunicorn workers)
_redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/1")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": _redis_url,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Sub-path deployment support (e.g. curlyphries.net/devotional-journal/)
_script_name = os.environ.get("FORCE_SCRIPT_NAME", "")
if _script_name:
    FORCE_SCRIPT_NAME = _script_name

# Static files
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    },
}

# Security headers
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Sentry
if _sentry_available and os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        # Stack-frame locals and request bodies can hold decrypted journal
        # text and API keys. Never ship them off the server.
        include_local_variables=False,
        max_request_body_size="never",
    )

# Secrets are required in production: a missing SECRET_KEY would otherwise fall
# back to a publicly known value and make every session token forgeable.
if not os.environ.get("SECRET_KEY"):
    raise ValueError("SECRET_KEY must be set in production")

# Encryption key is required in production
if not ENCRYPTION_ROOT_KEY:
    raise ValueError("ENCRYPTION_ROOT_KEY must be set in production")

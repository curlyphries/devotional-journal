"""
Django base settings for Devotional Journal project.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "")
if not SECRET_KEY:
    import warnings

    warnings.warn(
        "SECRET_KEY is not set. Using an empty key — set SECRET_KEY in your environment.",
        stacklevel=2,
    )
    SECRET_KEY = "dev-only-insecure-key-do-not-use-in-production-replace-me"

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "corsheaders",
    "django_filters",
    "django_celery_beat",
    # Local apps
    "apps.users",
    "apps.bible",
    "apps.plans",
    "apps.journal",
    "apps.prompts",
    "apps.streaks",
    "apps.groups",
    "apps.reflections",
]

MIDDLEWARE = [
    "shared.request_id.RequestIDMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "apps.users.middleware.MeshOnlyMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.users.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "30/hour",
        "user": "1000/hour",
        "auth": "10/hour",
        "magic_link": "5/hour",
        "plan_generate": "10/hour",
    },
    "EXCEPTION_HANDLER": "shared.errors.exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "shared.errors.EnvelopeJSONRenderer",
    ],
    # Number of reverse proxies in front of Django. Set it (NUM_PROXIES=2 for
    # host nginx + the frontend container) so throttles key on the real client
    # address and cannot be dodged with a forged X-Forwarded-For header.
    "NUM_PROXIES": (
        int(os.environ["NUM_PROXIES"]) if os.environ.get("NUM_PROXIES") else None
    ),
    "DEFAULT_PAGINATION_CLASS": "shared.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

# Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# Encryption
ENCRYPTION_ROOT_KEY = os.environ.get("ENCRYPTION_ROOT_KEY")

# LLM Configuration
LLM_BACKEND = os.environ.get("LLM_BACKEND", "ollama")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def env_bool(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


# Only allow AI that runs on this machine / private network. With this on, cloud
# providers are refused for everyone, whatever a user selects in Settings.
AI_LOCAL_ONLY = env_bool("AI_LOCAL_ONLY", False)
# Let users point at an AI server on a private address (LAN / mesh). Needed for
# self-hosted Ollama; leave off on a public multi-user instance (SSRF guard).
AI_ALLOW_PRIVATE_URLS = env_bool("AI_ALLOW_PRIVATE_URLS", False)

# Bible translations used for scripture shown with feedback, in order of
# preference. Both defaults are public domain. Text comes from the local
# database when loaded (manage.py load_translation WEB), else the Bolls API.
SCRIPTURE_TRANSLATIONS = [
    t.strip().upper()
    for t in os.environ.get("SCRIPTURE_TRANSLATIONS", "WEB,KJV").split(",")
    if t.strip()
]

# Mesh-only access (e.g. a Tailscale tailnet). When on, requests from outside
# MESH_ALLOWED_CIDRS are refused. Bind the published ports to the mesh
# interface as well — see docs/MESH_DEPLOYMENT.md.
MESH_ONLY = env_bool("MESH_ONLY", False)
MESH_ALLOWED_CIDRS = [
    c.strip()
    for c in os.environ.get(
        "MESH_ALLOWED_CIDRS", "100.64.0.0/10,fd7a:115c:a1e0::/48,127.0.0.0/8,::1/128"
    ).split(",")
    if c.strip()
]
# Proxies whose X-Real-IP header is believed (the nginx containers).
MESH_TRUSTED_PROXY_CIDRS = [
    c.strip()
    for c in os.environ.get(
        "MESH_TRUSTED_PROXY_CIDRS", "172.16.0.0/12,127.0.0.0/8,::1/128"
    ).split(",")
    if c.strip()
]

# Print sign-in links to the server log. A sign-in link is a credential, so
# this is off wherever a real mail server is configured. With no mail server
# (EMAIL_HOST unset or a placeholder) the log is the only way to sign in, so it
# defaults on there. Set MAGIC_LINK_LOG explicitly to override either way.
_NO_MAIL_SERVER = os.environ.get("EMAIL_HOST", "localhost") in (
    "",
    "localhost",
    "smtp.example.com",
)
MAGIC_LINK_LOG = env_bool("MAGIC_LINK_LOG", _NO_MAIL_SERVER)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"request_id": {"()": "shared.request_id.RequestIDLogFilter"}},
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} [{request_id}] {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["request_id"],
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        # httpx logs full request URLs at INFO; keep them out of the log.
        "httpx": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "true").lower() == "true"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "noreply@devotionaljournal.com"
)

# Magic Link
MAGIC_LINK_EXPIRY_MINUTES = 15

# Google OAuth
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.environ.get(
    "GOOGLE_REDIRECT_URI", "https://devotionaljournal.net/api/auth/google/callback/"
)
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://devotionaljournal.net")

"""
Development settings for Devotional Journal.
"""

from .base import *

DEBUG = True

# Allow hosts from environment variable or defaults
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0").split(
    ","
)

import dj_database_url

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "devotional"),
            "USER": os.environ.get("POSTGRES_USER", "devotional"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "devotional_dev"),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }

# CORS - restrict to known local origins even in development
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001",
).split(",")

# Disable throttling in local dev to avoid friction during development
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []

# Debug toolbar (optional - only if installed)
try:
    import debug_toolbar

    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]
except ImportError:
    pass

# Email - console backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Use a default encryption key for development
if not ENCRYPTION_ROOT_KEY:
    import warnings

    warnings.warn(
        "ENCRYPTION_ROOT_KEY is not set. Using insecure dev key — NEVER use this in production.",
        stacklevel=2,
    )
    ENCRYPTION_ROOT_KEY = "dev-encryption-key-32-bytes-long!"

# Tailscale-only access - disabled for public OAuth access
TAILSCALE_ONLY = False

# Add Tailscale middleware (disabled for public access)
# MIDDLEWARE.append('apps.users.middleware.TailscaleOnlyMiddleware')

# Frontend URL for magic links
FRONTEND_URL = "http://localhost:3001"

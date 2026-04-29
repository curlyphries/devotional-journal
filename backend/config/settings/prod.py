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

ALLOWED_HOSTS = [h for h in os.environ.get('ALLOWED_HOSTS', '').split(',') if h.strip()]

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'true').lower() == 'true'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS - restrict to known origins
_cors_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '')
CORS_ALLOWED_ORIGINS = [o for o in _cors_origins.split(',') if o.strip()]

# Sub-path deployment support (e.g. curlyphries.net/devotional-journal/)
_script_name = os.environ.get('FORCE_SCRIPT_NAME', '')
if _script_name:
    FORCE_SCRIPT_NAME = _script_name

# Static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Security headers
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Sentry
if _sentry_available and os.environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )

# Encryption key is required in production
if not ENCRYPTION_ROOT_KEY:
    raise ValueError('ENCRYPTION_ROOT_KEY must be set in production')

"""
URL configuration for Devotional Journal project.
"""

from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    """
    Liveness/readiness probe: is the database reachable, is the cache
    reachable. Unauthenticated, so it reports booleans only - no versions,
    hosts or error text. (AI reachability is per person: /prompts/ai-status/.)
    """
    import logging

    from django.core.cache import cache
    from django.db import connection

    logger = logging.getLogger("config.health")
    checks = {"database": False, "cache": False}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = True
    except Exception:
        logger.exception("Health check: database unreachable")
    try:
        cache.set("health:ping", "1", 10)
        checks["cache"] = cache.get("health:ping") == "1"
    except Exception:
        logger.exception("Health check: cache unreachable")

    healthy = all(checks.values())
    return JsonResponse(
        {"status": "ok" if healthy else "degraded", "checks": checks},
        status=200 if healthy else 503,
    )


urlpatterns = [
    path("api/v1/health/", health_check),
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.users.urls")),
    path("api/v1/me/", include("apps.users.profile_urls")),
    path("api/v1/bible/", include("apps.bible.urls")),
    path("api/v1/plans/", include("apps.plans.urls")),
    path("api/v1/journal/", include("apps.journal.urls")),
    path("api/v1/prompts/", include("apps.prompts.urls")),
    path("api/v1/groups/", include("apps.groups.urls")),
    path("api/v1/guides/", include("apps.guides.urls")),
    path("api/v1/", include("apps.reflections.urls")),
]

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

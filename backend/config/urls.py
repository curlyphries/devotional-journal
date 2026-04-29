"""
URL configuration for Devotional Journal project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('api/v1/health/', health_check),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/me/', include('apps.users.profile_urls')),
    path('api/v1/bible/', include('apps.bible.urls')),
    path('api/v1/plans/', include('apps.plans.urls')),
    path('api/v1/journal/', include('apps.journal.urls')),
    path('api/v1/prompts/', include('apps.prompts.urls')),
    path('api/v1/groups/', include('apps.groups.urls')),
    path('api/v1/', include('apps.reflections.urls')),
]

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

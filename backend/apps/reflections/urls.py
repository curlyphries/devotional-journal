"""
URL configuration for the Life Reflection system.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .admin_views import (
    DevotionalAuditViewSet,
    DevotionalQualityReportView,
)
from .views import (
    AlignmentTrendViewSet,
    CrewView,
    DailyReflectionViewSet,
    DashboardStatsView,
    DevotionalPassageViewSet,
    FocusIntentionViewSet,
    GrowthDataView,
    LifeAreaViewSet,
    MilestonesView,
    OpenThreadViewSet,
    ScriptureInsightView,
    StudyGuideSessionViewSet,
    ThreadPromptPendingView,
    ThreadPromptRespondView,
    ThreadPromptViewSet,
    UserJourneyViewSet,
)

router = DefaultRouter()
router.register(r"life-areas", LifeAreaViewSet, basename="life-area")
router.register(r"journeys", UserJourneyViewSet, basename="journey")
router.register(r"reflections", DailyReflectionViewSet, basename="reflection")
router.register(r"trends", AlignmentTrendViewSet, basename="trend")
router.register(r"threads", OpenThreadViewSet, basename="thread")
router.register(r"thread-prompts", ThreadPromptViewSet, basename="thread-prompt")
router.register(r"focus", FocusIntentionViewSet, basename="focus")
router.register(r"passages", DevotionalPassageViewSet, basename="passage")
router.register(r"study-sessions", StudyGuideSessionViewSet, basename="study-session")
router.register(r"admin/audits", DevotionalAuditViewSet, basename="devotional-audit")

urlpatterns = [
    path("", include(router.urls)),
    # Dashboard
    path("dashboard/stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    # Thread prompts
    path(
        "thread-prompts/pending/",
        ThreadPromptPendingView.as_view(),
        name="thread-prompts-pending",
    ),
    path(
        "thread-prompts/<uuid:thread_id>/respond/",
        ThreadPromptRespondView.as_view(),
        name="thread-prompt-respond",
    ),
    # Milestones & Growth
    path("milestones/", MilestonesView.as_view(), name="milestones"),
    path("trends/growth/", GrowthDataView.as_view(), name="growth-data"),
    # Crew API endpoints
    path("crew/health/", CrewView.as_view(), {"action": "health"}, name="crew-health"),
    path(
        "crew/weekly-review/",
        CrewView.as_view(),
        {"action": "weekly-review"},
        name="crew-weekly-review",
    ),
    path(
        "crew/monthly-recap/",
        CrewView.as_view(),
        {"action": "monthly-recap"},
        name="crew-monthly-recap",
    ),
    path(
        "crew/ask-agent/",
        CrewView.as_view(),
        {"action": "ask-agent"},
        name="crew-ask-agent",
    ),
    path(
        "insights/scripture/", ScriptureInsightView.as_view(), name="scripture-insights"
    ),
    # Admin endpoints
    path(
        "admin/quality-report/",
        DevotionalQualityReportView.as_view(),
        name="quality-report",
    ),
]

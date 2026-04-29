"""
URL routes for reading plans.
"""

from django.urls import path

from .views import (
    AdvanceDayView,
    EnrolledPlansView,
    EnrollView,
    PlanDetailView,
    PlanListView,
    TodayReadingView,
)

urlpatterns = [
    path("", PlanListView.as_view(), name="plan-list"),
    path("<uuid:plan_id>/", PlanDetailView.as_view(), name="plan-detail"),
    path("<uuid:plan_id>/enroll/", EnrollView.as_view(), name="plan-enroll"),
    path("enrolled/", EnrolledPlansView.as_view(), name="enrolled-plans"),
    path(
        "enrolled/<uuid:enrollment_id>/today/",
        TodayReadingView.as_view(),
        name="today-reading",
    ),
    path(
        "enrolled/<uuid:enrollment_id>/advance/",
        AdvanceDayView.as_view(),
        name="advance-day",
    ),
]

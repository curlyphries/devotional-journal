"""
URL routes for groups (Phase 2).
"""

from django.urls import path

from .views import (
    GroupDetailView,
    GroupEngagementView,
    GroupListCreateView,
    JoinGroupView,
    LeaveGroupView,
    SetGroupPlanView,
)

urlpatterns = [
    path("", GroupListCreateView.as_view(), name="group-list"),
    path("<uuid:group_id>/", GroupDetailView.as_view(), name="group-detail"),
    path("<uuid:group_id>/join/", JoinGroupView.as_view(), name="group-join"),
    path("<uuid:group_id>/leave/", LeaveGroupView.as_view(), name="group-leave"),
    path(
        "<uuid:group_id>/engagement/",
        GroupEngagementView.as_view(),
        name="group-engagement",
    ),
    path(
        "<uuid:group_id>/set-plan/", SetGroupPlanView.as_view(), name="group-set-plan"
    ),
]

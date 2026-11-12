"""
URL routes for journal entries.
"""

from django.urls import path

from .views import (
    JournalDetailView,
    JournalEntryDeepDiveView,
    JournalExportView,
    JournalFeedbackListView,
    JournalFeedbackRateView,
    JournalFeedbackView,
    JournalListCreateView,
    JournalThemesView,
)

urlpatterns = [
    path("", JournalListCreateView.as_view(), name="journal-list"),
    path("export/", JournalExportView.as_view(), name="journal-export"),
    path("themes/", JournalThemesView.as_view(), name="journal-themes"),
    path("feedback/", JournalFeedbackListView.as_view(), name="journal-feedback-list"),
    path(
        "feedback/<uuid:feedback_id>/rate/",
        JournalFeedbackRateView.as_view(),
        name="journal-feedback-rate",
    ),
    path("<uuid:entry_id>/", JournalDetailView.as_view(), name="journal-detail"),
    path(
        "<uuid:entry_id>/feedback/",
        JournalFeedbackView.as_view(),
        name="journal-feedback",
    ),
    path(
        "<uuid:entry_id>/deep-dive/",
        JournalEntryDeepDiveView.as_view(),
        name="journal-deep-dive",
    ),
]

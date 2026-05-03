"""
URL routes for user profile endpoints.
"""

from django.urls import path

from .export_views import (
    FullDataExportView,
    GrowthReportExportView,
    HighlightsMarkdownExportView,
    JournalMarkdownExportView,
)
from .views import ProfileView

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("export/", FullDataExportView.as_view(), name="full-export"),
    path("export/journal/", JournalMarkdownExportView.as_view(), name="export-journal"),
    path("export/highlights/", HighlightsMarkdownExportView.as_view(), name="export-highlights"),
    path("export/growth/", GrowthReportExportView.as_view(), name="export-growth"),
]

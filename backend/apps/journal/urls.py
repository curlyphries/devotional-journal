"""
URL routes for journal entries.
"""
from django.urls import path

from .views import (
    JournalListCreateView,
    JournalDetailView,
    JournalExportView,
    JournalEntryDeepDiveView,
)

urlpatterns = [
    path('', JournalListCreateView.as_view(), name='journal-list'),
    path('<uuid:entry_id>/', JournalDetailView.as_view(), name='journal-detail'),
    path('<uuid:entry_id>/deep-dive/', JournalEntryDeepDiveView.as_view(), name='journal-deep-dive'),
    path('export/', JournalExportView.as_view(), name='journal-export'),
]

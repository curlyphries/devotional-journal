"""
URL routes for prompt generation.
"""
from django.urls import path

from .views import (
    GeneratePromptsView,
    HeartPromptGuidanceView,
    ExplorationHistoryListView,
    ExplorationHistoryDetailView,
    ExplorationBookmarkView,
)

urlpatterns = [
    path('generate/', GeneratePromptsView.as_view(), name='generate-prompts'),
    path('explore/', HeartPromptGuidanceView.as_view(), name='explore-heart-prompt'),
    path('explorations/', ExplorationHistoryListView.as_view(), name='exploration-list'),
    path('explorations/<uuid:exploration_id>/', ExplorationHistoryDetailView.as_view(), name='exploration-detail'),
    path('explorations/<uuid:exploration_id>/bookmark/', ExplorationBookmarkView.as_view(), name='exploration-bookmark'),
]

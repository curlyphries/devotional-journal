"""
URL routes for Bible endpoints.
"""

from django.urls import path

from .views import (
    BollsPassageView,
    BollsSearchView,
    BollsTranslationsView,
    BollsVerifyView,
    HighlightDetailView,
    HighlightListCreateView,
    PassageReadView,
    SearchView,
    TranslationListView,
)

urlpatterns = [
    # Local database translations (KJV loaded)
    path("translations/", TranslationListView.as_view(), name="bible-translations"),
    path("read/", PassageReadView.as_view(), name="bible-read"),
    path("search/", SearchView.as_view(), name="bible-search"),
    # Bolls Bible API (external - KJV, ASV, YLT, WEB, RV1960)
    path(
        "bolls/translations/",
        BollsTranslationsView.as_view(),
        name="bolls-translations",
    ),
    path("bolls/read/", BollsPassageView.as_view(), name="bolls-read"),
    path("bolls/search/", BollsSearchView.as_view(), name="bolls-search"),
    path("bolls/verify/", BollsVerifyView.as_view(), name="bolls-verify"),
    # User highlights and notes
    path("highlights/", HighlightListCreateView.as_view(), name="highlight-list"),
    path(
        "highlights/<uuid:pk>/", HighlightDetailView.as_view(), name="highlight-detail"
    ),
]

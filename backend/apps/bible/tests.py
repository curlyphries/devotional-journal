"""
Tests for bible app.
"""

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestBibleModels:
    def test_translation_str(self, bible_translation):
        assert str(bible_translation) == "TEST - Test Translation"

    def test_verse_str(self, bible_verses):
        verse = bible_verses[0]
        assert "Psalms 23:1" in str(verse)


@pytest.mark.django_db
class TestBibleAPI:
    def test_list_translations(self, authenticated_client, bible_translation):
        response = authenticated_client.get("/api/v1/bible/translations/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert response.data[0]["code"] == "TEST"

    def test_read_passage(self, authenticated_client, bible_translation, bible_verses):
        response = authenticated_client.get(
            "/api/v1/bible/read/",
            {
                "translation": "TEST",
                "book": "PSA",
                "chapter": 23,
                "verse_start": 1,
                "verse_end": 3,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["verses"]) == 3

    def test_read_passage_invalid_translation(self, authenticated_client):
        response = authenticated_client.get(
            "/api/v1/bible/read/",
            {
                "translation": "INVALID",
                "book": "PSA",
                "chapter": 23,
            },
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_search_verses(self, authenticated_client, bible_translation, bible_verses):
        response = authenticated_client.get(
            "/api/v1/bible/search/",
            {
                "translation": "TEST",
                "q": "verse",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 1

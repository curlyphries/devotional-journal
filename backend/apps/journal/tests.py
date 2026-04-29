"""
Tests for journal app.
"""

import pytest
from django.utils import timezone
from rest_framework import status

from apps.journal.models import JournalEntry


@pytest.mark.django_db
class TestJournalEntry:
    def test_create_entry(self, user):
        entry = JournalEntry.objects.create(
            user=user,
            date=timezone.now().date(),
            mood_tag="grateful",
        )
        entry.set_content("This is my journal entry.")
        entry.save()

        assert entry.user == user
        assert entry.mood_tag == "grateful"

    def test_content_encryption(self, user):
        entry = JournalEntry.objects.create(
            user=user,
            date=timezone.now().date(),
        )
        original_content = "Secret journal content"
        entry.set_content(original_content)
        entry.save()

        # Encrypted content should not equal original
        assert entry.encrypted_content != original_content.encode()

        # Decrypted content should match original
        assert entry.get_content() == original_content

    def test_entry_str(self, user):
        entry = JournalEntry.objects.create(
            user=user,
            date=timezone.now().date(),
        )
        assert user.email in str(entry)


@pytest.mark.django_db
class TestJournalAPI:
    def test_list_entries(self, authenticated_client, user):
        # Create some entries
        for i in range(3):
            entry = JournalEntry.objects.create(
                user=user,
                date=timezone.now().date(),
            )
            entry.set_content(f"Entry {i}")
            entry.save()

        response = authenticated_client.get("/api/v1/journal/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_create_entry(self, authenticated_client):
        response = authenticated_client.post(
            "/api/v1/journal/",
            {
                "date": timezone.now().date().isoformat(),
                "content": "My new journal entry",
                "mood_tag": "peaceful",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["mood_tag"] == "peaceful"

    def test_get_entry(self, authenticated_client, user):
        entry = JournalEntry.objects.create(
            user=user,
            date=timezone.now().date(),
        )
        entry.set_content("Test content")
        entry.save()

        response = authenticated_client.get(f"/api/v1/journal/{entry.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["content"] == "Test content"

    def test_update_entry(self, authenticated_client, user):
        entry = JournalEntry.objects.create(
            user=user,
            date=timezone.now().date(),
        )
        entry.set_content("Original content")
        entry.save()

        response = authenticated_client.patch(
            f"/api/v1/journal/{entry.id}/",
            {
                "content": "Updated content",
            },
        )
        assert response.status_code == status.HTTP_200_OK

        entry.refresh_from_db()
        assert entry.get_content() == "Updated content"

    def test_delete_entry(self, authenticated_client, user):
        entry = JournalEntry.objects.create(
            user=user,
            date=timezone.now().date(),
        )

        response = authenticated_client.delete(f"/api/v1/journal/{entry.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not JournalEntry.objects.filter(id=entry.id).exists()

    def test_cannot_access_other_user_entry(self, authenticated_client, user_factory):
        other_user = user_factory()
        entry = JournalEntry.objects.create(
            user=other_user,
            date=timezone.now().date(),
        )

        response = authenticated_client.get(f"/api/v1/journal/{entry.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

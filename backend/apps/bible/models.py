"""
Bible models for translations, verses, and user highlights.
"""

import uuid

from django.conf import settings
from django.db import models


class BibleTranslation(models.Model):
    """
    Bible translation metadata.
    """

    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("es", "Spanish"),
    ]

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    is_public_domain = models.BooleanField(default=True)
    provider_class = models.CharField(
        max_length=200,
        blank=True,
        help_text="Dotted path to Python class for API-based translations",
    )

    class Meta:
        db_table = "bible_translations"

    def __str__(self):
        return f"{self.code} - {self.name}"


class BibleVerse(models.Model):
    """
    Individual Bible verse.
    """

    translation = models.ForeignKey(
        BibleTranslation, on_delete=models.CASCADE, related_name="verses"
    )
    book = models.CharField(max_length=10)
    book_name = models.CharField(max_length=50)
    chapter = models.PositiveIntegerField()
    verse = models.PositiveIntegerField()
    text = models.TextField()

    class Meta:
        db_table = "bible_verses"
        unique_together = ["translation", "book", "chapter", "verse"]
        indexes = [
            models.Index(fields=["translation", "book", "chapter"]),
            models.Index(fields=["book", "chapter", "verse"]),
        ]

    def __str__(self):
        return f"{self.book_name} {self.chapter}:{self.verse}"

    @property
    def reference(self):
        return f"{self.book_name} {self.chapter}:{self.verse}"


class VerseHighlight(models.Model):
    """
    User's highlighted verses with optional notes.
    """

    HIGHLIGHT_COLORS = [
        ("yellow", "Yellow"),
        ("green", "Green"),
        ("blue", "Blue"),
        ("pink", "Pink"),
        ("orange", "Orange"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verse_highlights",
    )
    book = models.CharField(max_length=50)
    chapter = models.IntegerField()
    verse_start = models.IntegerField()
    verse_end = models.IntegerField(null=True, blank=True)
    translation = models.CharField(max_length=20, default="KJV")
    color = models.CharField(max_length=20, choices=HIGHLIGHT_COLORS, default="yellow")
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "verse_highlights"
        ordering = ["book", "chapter", "verse_start"]
        unique_together = ["user", "book", "chapter", "verse_start", "translation"]

    def __str__(self):
        verse_ref = f"{self.book} {self.chapter}:{self.verse_start}"
        if self.verse_end and self.verse_end != self.verse_start:
            verse_ref += f"-{self.verse_end}"
        return f"VerseHighlight({self.id}) - {verse_ref}"

    @property
    def reference(self):
        ref = f"{self.book} {self.chapter}:{self.verse_start}"
        if self.verse_end and self.verse_end != self.verse_start:
            ref += f"-{self.verse_end}"
        return ref

"""Tests for reference parsing and passage lookup."""

import pytest

from apps.bible import bolls_api
from apps.bible.books import find_book, parse_reference
from apps.bible.lookup import clean_verse_text, fetch_passage, fetch_reference

_REAL_GET_CHAPTER = bolls_api.get_chapter


class TestBooks:
    @pytest.mark.parametrize(
        "text,code",
        [
            ("Genesis", "GEN"),
            ("1 Corinthians", "1CO"),
            ("1Cor", "1CO"),
            ("I Corinthians", "1CO"),
            ("First John", "1JN"),
            ("Psalm", "PSA"),
            ("Psalms", "PSA"),
            ("Song of Songs", "SNG"),
            ("Phil", "PHP"),
            ("Jn", "JHN"),
            ("rev.", "REV"),
            ("PHP", "PHP"),
            (50, "PHP"),
            ("Salmos", "PSA"),
            ("2 Tim", "2TI"),
        ],
    )
    def test_find_book(self, text, code):
        assert find_book(text).code == code

    def test_unknown_books(self):
        for text in ("Hezekiah", "", None, "4 John", "67"):
            assert find_book(text) is None

    @pytest.mark.parametrize(
        "text,expected",
        [
            ("Philippians 4:6-7", ("PHP", 4, 6, 7)),
            ("1 Corinthians 13:4", ("1CO", 13, 4, 4)),
            ("Song of Solomon 2:1-3", ("SNG", 2, 1, 3)),
            ("Psalm 23", ("PSA", 23, None, None)),
            ("Jn 3:16", ("JHN", 3, 16, 16)),
            ("2 Tim. 1:7", ("2TI", 1, 7, 7)),
            ("Romans 8:28–30", ("ROM", 8, 28, 30)),
        ],
    )
    def test_parse_reference(self, text, expected):
        parsed = parse_reference(text)
        assert (
            parsed.book.code,
            parsed.chapter,
            parsed.verse_start,
            parsed.verse_end,
        ) == expected

    def test_parse_reference_rejects_nonsense(self):
        for text in ("", "Hezekiah 3:16", "love one another", "John", None):
            assert parse_reference(text) is None


def test_clean_verse_text_strips_markup():
    raw = "In the beginning<S>7225</S> God<sup>a</sup> created<br/> the <i>heavens</i> &amp; earth."
    assert clean_verse_text(raw) == "In the beginning God created the heavens & earth."


@pytest.mark.django_db
class TestLookup:
    def test_local_database_is_used_first(self, web_bible):
        passage = fetch_reference("Phil 4:6-7")
        assert passage.reference == "Philippians 4:6-7"
        assert passage.translation == "WEB" and passage.source == "local"
        assert passage.text.startswith("In nothing be anxious")
        assert passage.text.endswith("in Christ Jesus.")
        assert passage.to_dict()["translation_name"] == "World English Bible"

    def test_missing_passages_return_none(self, web_bible):
        assert fetch_reference("Philippians 4:99") is None  # verse out of range
        assert fetch_reference("Philippians 77:1") is None  # chapter out of range
        assert fetch_reference("Hezekiah 1:1") is None
        assert fetch_passage("John", "three", 16) is None

    def test_range_past_the_end_of_the_chapter_is_trimmed(self, web_bible):
        passage = fetch_reference("Matthew 11:28-40")
        assert passage.reference == "Matthew 11:28-30"

    def test_falls_back_to_the_api_then_the_next_translation(self, db, monkeypatch):
        calls = []

        def fake_get_chapter(translation, book, chapter):
            calls.append((translation, book, chapter))
            if translation == "WEB":
                raise bolls_api.BollsAPIError("down")
            return [
                {
                    "verse": 16,
                    "text": "For God so loved the world,<br/> that he gave...",
                },
                {"verse": 17, "text": "For God sent not his Son..."},
            ]

        monkeypatch.setattr(bolls_api, "get_chapter", fake_get_chapter)
        passage = fetch_reference("John 3:16")
        assert calls == [("WEB", "JHN", 3), ("KJV", "JHN", 3)]
        assert (passage.translation, passage.source) == ("KJV", "bolls")
        assert passage.text == "For God so loved the world, that he gave..."


def test_bolls_requests_use_book_numbers(monkeypatch):
    """Bolls addresses books by number; codes and names must be translated."""
    seen = []

    class Reply:
        def raise_for_status(self):
            pass

        def json(self):
            return [{"verse": 1, "text": "x"}]

    def fake_get(url, timeout=None):
        seen.append(url)
        return Reply()

    monkeypatch.setattr(bolls_api.requests, "get", fake_get)
    monkeypatch.setattr(bolls_api.cache, "get", lambda key: None)
    monkeypatch.setattr(bolls_api.cache, "set", lambda *args, **kwargs: None)

    # _REAL_GET_CHAPTER was captured at import, before the autouse network block.
    _REAL_GET_CHAPTER("WEB", "PHP", 4)
    _REAL_GET_CHAPTER("WEB", "1 Corinthians", 13)
    assert seen == [
        "https://bolls.life/get-text/WEB/50/4/",
        "https://bolls.life/get-text/WEB/46/13/",
    ]

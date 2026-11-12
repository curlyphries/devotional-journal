"""
Retrieve the actual text of a passage from a Bible source.

This is the only place scripture text shown to a user may come from. Models
suggest *references*; the words are always fetched here, so a model can never
put a misquoted or invented verse in front of someone.

Lookup order for each translation in settings.SCRIPTURE_TRANSLATIONS
(default WEB, then KJV):
  1. the local database (works with no outbound network), then
  2. the Bolls API.
"""

import html
import logging
import re
from dataclasses import asdict, dataclass
from typing import Optional

from django.conf import settings

from . import bolls_api
from .books import Book, find_book, format_reference, parse_reference
from .models import BibleVerse

logger = logging.getLogger(__name__)

MAX_VERSES = 12  # keep a passage short enough to meditate on

TRANSLATION_NAMES = {
    "WEB": "World English Bible",
    "KJV": "King James Version",
    "ASV": "American Standard Version (1901)",
    "YLT": "Young's Literal Translation (1898)",
    "RV1960": "Reina-Valera 1960",
}


@dataclass
class Passage:
    reference: str
    book: str
    book_code: str
    chapter: int
    verse_start: int
    verse_end: int
    text: str
    translation: str
    translation_name: str
    source: str  # "local" | "bolls"
    verified: bool = True

    def to_dict(self) -> dict:
        data = asdict(self)
        data.pop("book_code")
        return data


def clean_verse_text(text: str) -> str:
    """Strip markup the sources embed (Strong's numbers, footnotes, <br>, <i>)."""
    if not text:
        return ""
    text = re.sub(r"<S>.*?</S>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<sup>.*?</sup>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def preferred_translations(language: str = "en") -> list[str]:
    configured = list(getattr(settings, "SCRIPTURE_TRANSLATIONS", ["WEB", "KJV"]))
    if language == "es":
        return ["RV1960", *[t for t in configured if t != "RV1960"]]
    return configured


def _from_local(translation: str, book: Book, chapter: int, start: int, end: int):
    rows = list(
        BibleVerse.objects.filter(
            translation__code=translation,
            book=book.code,
            chapter=chapter,
            verse__gte=start,
            verse__lte=end,
        )
        .order_by("verse")
        .values_list("verse", "text")
    )
    return rows or None


def _from_bolls(translation: str, book: Book, chapter: int, start: int, end: int):
    if translation not in bolls_api.ALLOWED_TRANSLATIONS:
        return None
    try:
        verses = bolls_api.get_chapter(translation, book.code, chapter)
    except bolls_api.BollsAPIError as exc:
        logger.warning(
            "Bible source unavailable for %s %s: %s", book.code, chapter, exc
        )
        return None
    if not isinstance(verses, list):
        return None
    rows = [
        (v.get("verse"), v.get("text", ""))
        for v in verses
        if isinstance(v, dict)
        and isinstance(v.get("verse"), int)
        and start <= v["verse"] <= end
    ]
    return sorted(rows) or None


def fetch_passage(
    book,
    chapter,
    verse_start=None,
    verse_end=None,
    translations: Optional[list[str]] = None,
) -> Optional[Passage]:
    """
    Return the passage text, or None if the reference does not exist in any
    available source (unknown book, chapter or verse out of range, sources down).
    """
    resolved = book if isinstance(book, Book) else find_book(book)
    if not resolved:
        return None
    try:
        chapter = int(chapter)
        start = int(verse_start) if verse_start not in (None, "") else 1
        end = int(verse_end) if verse_end not in (None, "") else None
    except (TypeError, ValueError):
        return None
    if chapter < 1 or start < 1:
        return None
    if end is None:
        # No verse given at all -> the opening of the chapter; one verse -> itself.
        end = start + MAX_VERSES - 1 if verse_start in (None, "") else start
    if end < start:
        end = start
    end = min(end, start + MAX_VERSES - 1)

    for translation in translations or preferred_translations():
        for source, fetch in (("local", _from_local), ("bolls", _from_bolls)):
            rows = fetch(translation, resolved, chapter, start, end)
            if not rows:
                continue
            # The first requested verse must exist; a tail that runs past the
            # end of the chapter is simply trimmed.
            if rows[0][0] != start:
                continue
            text = " ".join(clean_verse_text(t) for _, t in rows).strip()
            if not text:
                continue
            last = rows[-1][0]
            return Passage(
                reference=format_reference(resolved, chapter, start, last),
                book=resolved.name,
                book_code=resolved.code,
                chapter=chapter,
                verse_start=start,
                verse_end=last,
                text=text,
                translation=translation,
                translation_name=TRANSLATION_NAMES.get(translation, translation),
                source=source,
            )
    return None


def fetch_reference(
    reference: str, translations: Optional[list[str]] = None
) -> Optional[Passage]:
    """fetch_passage for a free-text reference such as "1 Corinthians 13:4-7"."""
    parsed = parse_reference(reference)
    if not parsed:
        return None
    return fetch_passage(
        parsed.book,
        parsed.chapter,
        parsed.verse_start,
        parsed.verse_end,
        translations=translations,
    )

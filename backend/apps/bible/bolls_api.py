"""
Bolls Bible API integration for fetching verses from multiple translations.
Personal use only - some translations have copyright restrictions for commercial use.
"""

import logging
from typing import Optional

import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Translations available for personal use
# Public domain: KJV, ASV, YLT, WEB
# Fair use (non-commercial): RVR1960
ALLOWED_TRANSLATIONS = {
    "KJV": {
        "name": "King James Version",
        "language": "en",
        "public_domain": True,
    },
    "ASV": {
        "name": "American Standard Version (1901)",
        "language": "en",
        "public_domain": True,
    },
    "YLT": {
        "name": "Young's Literal Translation (1898)",
        "language": "en",
        "public_domain": True,
    },
    "WEB": {
        "name": "World English Bible",
        "language": "en",
        "public_domain": True,
    },
    "RV1960": {
        "name": "Reina-Valera 1960",
        "language": "es",
        "public_domain": False,
        "attribution": "El texto bíblico ha sido tomado de la versión Reina-Valera © 1960 Sociedades Bíblicas en América Latina; © renovado 1988 Sociedades Bíblicas Unidas. Utilizado con permiso.",
    },
}

BOLLS_API_BASE = "https://bolls.life/get-text"
CACHE_TIMEOUT = 60 * 60 * 24 * 7  # 7 days


class BollsAPIError(Exception):
    """Error fetching from Bolls API"""

    pass


def get_available_translations():
    """Return list of available translations with metadata."""
    return [
        {
            "code": code,
            "name": info["name"],
            "language": info["language"],
            "public_domain": info["public_domain"],
            "attribution": info.get("attribution"),
        }
        for code, info in ALLOWED_TRANSLATIONS.items()
    ]


def get_chapter(translation: str, book: str, chapter: int) -> Optional[list]:
    """
    Fetch a chapter from Bolls API.

    Args:
        translation: Translation code (e.g., 'KJV', 'RVR1960')
        book: Book abbreviation (e.g., 'GEN', 'PSA', 'JHN')
        chapter: Chapter number

    Returns:
        List of verse dicts with 'verse' and 'text' keys
    """
    if translation not in ALLOWED_TRANSLATIONS:
        raise BollsAPIError(
            f"Translation '{translation}' not allowed. Use one of: {list(ALLOWED_TRANSLATIONS.keys())}"
        )

    cache_key = f"bolls:{translation}:{book}:{chapter}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    url = f"{BOLLS_API_BASE}/{translation}/{book}/{chapter}/"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        verses = response.json()

        # Cache the result
        cache.set(cache_key, verses, CACHE_TIMEOUT)

        return verses
    except requests.RequestException as e:
        logger.error(f"Bolls API error: {e}")
        raise BollsAPIError(f"Failed to fetch {book} {chapter} from Bolls API: {e}")


def get_verse(translation: str, book: str, chapter: int, verse: int) -> Optional[dict]:
    """
    Fetch a single verse.

    Returns:
        Dict with 'verse', 'text', 'translation', 'book', 'chapter' keys
    """
    verses = get_chapter(translation, book, chapter)

    for v in verses:
        if v.get("verse") == verse:
            return {
                "verse": verse,
                "text": v.get("text", ""),
                "translation": translation,
                "book": book,
                "chapter": chapter,
            }

    return None


def get_verse_range(
    translation: str, book: str, chapter: int, start_verse: int, end_verse: int
) -> list:
    """
    Fetch a range of verses from a chapter.

    Returns:
        List of verse dicts
    """
    verses = get_chapter(translation, book, chapter)

    result = []
    for v in verses:
        verse_num = v.get("verse", 0)
        if start_verse <= verse_num <= end_verse:
            result.append(
                {
                    "verse": verse_num,
                    "text": v.get("text", ""),
                    "translation": translation,
                    "book": book,
                    "chapter": chapter,
                }
            )

    return result


def search_text(translation: str, query: str, limit: int = 20) -> list:
    """
    Search for text in a translation using Bolls API.
    Note: Bolls search endpoint may have different behavior.

    Returns:
        List of matching verse dicts
    """
    if translation not in ALLOWED_TRANSLATIONS:
        raise BollsAPIError(f"Translation '{translation}' not allowed")

    cache_key = f"bolls:search:{translation}:{query}:{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    url = f"https://bolls.life/search/{translation}/"

    try:
        response = requests.get(url, params={"search": query}, timeout=15)
        response.raise_for_status()
        results = response.json()

        # Limit results
        results = results[:limit] if len(results) > limit else results

        # Cache for shorter time since searches vary
        cache.set(cache_key, results, 60 * 60)  # 1 hour

        return results
    except requests.RequestException as e:
        logger.error(f"Bolls search error: {e}")
        raise BollsAPIError(f"Search failed: {e}")


# Book name mappings (Bolls uses specific abbreviations)
BOOK_MAPPINGS = {
    # Old Testament
    "genesis": "GEN",
    "gen": "GEN",
    "exodus": "EXO",
    "exo": "EXO",
    "ex": "EXO",
    "leviticus": "LEV",
    "lev": "LEV",
    "numbers": "NUM",
    "num": "NUM",
    "deuteronomy": "DEU",
    "deu": "DEU",
    "deut": "DEU",
    "joshua": "JOS",
    "jos": "JOS",
    "josh": "JOS",
    "judges": "JDG",
    "jdg": "JDG",
    "judg": "JDG",
    "ruth": "RUT",
    "rut": "RUT",
    "1samuel": "1SA",
    "1sam": "1SA",
    "1sa": "1SA",
    "2samuel": "2SA",
    "2sam": "2SA",
    "2sa": "2SA",
    "1kings": "1KI",
    "1ki": "1KI",
    "2kings": "2KI",
    "2ki": "2KI",
    "1chronicles": "1CH",
    "1chr": "1CH",
    "1ch": "1CH",
    "2chronicles": "2CH",
    "2chr": "2CH",
    "2ch": "2CH",
    "ezra": "EZR",
    "ezr": "EZR",
    "nehemiah": "NEH",
    "neh": "NEH",
    "esther": "EST",
    "est": "EST",
    "job": "JOB",
    "psalms": "PSA",
    "psalm": "PSA",
    "psa": "PSA",
    "ps": "PSA",
    "proverbs": "PRO",
    "prov": "PRO",
    "pro": "PRO",
    "ecclesiastes": "ECC",
    "ecc": "ECC",
    "eccl": "ECC",
    "songofsolomon": "SNG",
    "song": "SNG",
    "sos": "SNG",
    "sng": "SNG",
    "isaiah": "ISA",
    "isa": "ISA",
    "jeremiah": "JER",
    "jer": "JER",
    "lamentations": "LAM",
    "lam": "LAM",
    "ezekiel": "EZK",
    "ezek": "EZK",
    "ezk": "EZK",
    "daniel": "DAN",
    "dan": "DAN",
    "hosea": "HOS",
    "hos": "HOS",
    "joel": "JOL",
    "jol": "JOL",
    "amos": "AMO",
    "amo": "AMO",
    "obadiah": "OBA",
    "oba": "OBA",
    "obad": "OBA",
    "jonah": "JON",
    "jon": "JON",
    "micah": "MIC",
    "mic": "MIC",
    "nahum": "NAH",
    "nah": "NAH",
    "habakkuk": "HAB",
    "hab": "HAB",
    "zephaniah": "ZEP",
    "zep": "ZEP",
    "zeph": "ZEP",
    "haggai": "HAG",
    "hag": "HAG",
    "zechariah": "ZEC",
    "zec": "ZEC",
    "zech": "ZEC",
    "malachi": "MAL",
    "mal": "MAL",
    # New Testament
    "matthew": "MAT",
    "matt": "MAT",
    "mat": "MAT",
    "mark": "MRK",
    "mrk": "MRK",
    "luke": "LUK",
    "luk": "LUK",
    "john": "JHN",
    "jhn": "JHN",
    "acts": "ACT",
    "act": "ACT",
    "romans": "ROM",
    "rom": "ROM",
    "1corinthians": "1CO",
    "1cor": "1CO",
    "1co": "1CO",
    "2corinthians": "2CO",
    "2cor": "2CO",
    "2co": "2CO",
    "galatians": "GAL",
    "gal": "GAL",
    "ephesians": "EPH",
    "eph": "EPH",
    "philippians": "PHP",
    "phil": "PHP",
    "php": "PHP",
    "colossians": "COL",
    "col": "COL",
    "1thessalonians": "1TH",
    "1thess": "1TH",
    "1th": "1TH",
    "2thessalonians": "2TH",
    "2thess": "2TH",
    "2th": "2TH",
    "1timothy": "1TI",
    "1tim": "1TI",
    "1ti": "1TI",
    "2timothy": "2TI",
    "2tim": "2TI",
    "2ti": "2TI",
    "titus": "TIT",
    "tit": "TIT",
    "philemon": "PHM",
    "phlm": "PHM",
    "phm": "PHM",
    "hebrews": "HEB",
    "heb": "HEB",
    "james": "JAS",
    "jas": "JAS",
    "1peter": "1PE",
    "1pet": "1PE",
    "1pe": "1PE",
    "2peter": "2PE",
    "2pet": "2PE",
    "2pe": "2PE",
    "1john": "1JN",
    "1jn": "1JN",
    "2john": "2JN",
    "2jn": "2JN",
    "3john": "3JN",
    "3jn": "3JN",
    "jude": "JUD",
    "jud": "JUD",
    "revelation": "REV",
    "rev": "REV",
}


def normalize_book(book: str) -> str:
    """Convert various book name formats to Bolls API format."""
    normalized = book.lower().replace(" ", "").replace(".", "")
    return BOOK_MAPPINGS.get(normalized, book.upper())

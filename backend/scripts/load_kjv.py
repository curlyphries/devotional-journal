#!/usr/bin/env python
"""
Load KJV Bible text into the database.

This script downloads the KJV Bible from a public domain source and loads it
into the BibleVerse model.

Usage:
    python manage.py shell < scripts/load_kjv.py
    # OR
    python scripts/load_kjv.py  (if DJANGO_SETTINGS_MODULE is set)
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

# Setup Django if running standalone
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    import django

    django.setup()

from apps.bible.models import BibleTranslation, BibleVerse

# Book abbreviations mapping
BOOK_ABBREVS = {
    "Genesis": "GEN",
    "Exodus": "EXO",
    "Leviticus": "LEV",
    "Numbers": "NUM",
    "Deuteronomy": "DEU",
    "Joshua": "JOS",
    "Judges": "JDG",
    "Ruth": "RUT",
    "1 Samuel": "1SA",
    "2 Samuel": "2SA",
    "1 Kings": "1KI",
    "2 Kings": "2KI",
    "1 Chronicles": "1CH",
    "2 Chronicles": "2CH",
    "Ezra": "EZR",
    "Nehemiah": "NEH",
    "Esther": "EST",
    "Job": "JOB",
    "Psalms": "PSA",
    "Proverbs": "PRO",
    "Ecclesiastes": "ECC",
    "Song of Solomon": "SNG",
    "Isaiah": "ISA",
    "Jeremiah": "JER",
    "Lamentations": "LAM",
    "Ezekiel": "EZK",
    "Daniel": "DAN",
    "Hosea": "HOS",
    "Joel": "JOL",
    "Amos": "AMO",
    "Obadiah": "OBA",
    "Jonah": "JON",
    "Micah": "MIC",
    "Nahum": "NAH",
    "Habakkuk": "HAB",
    "Zephaniah": "ZEP",
    "Haggai": "HAG",
    "Zechariah": "ZEC",
    "Malachi": "MAL",
    "Matthew": "MAT",
    "Mark": "MRK",
    "Luke": "LUK",
    "John": "JHN",
    "Acts": "ACT",
    "Romans": "ROM",
    "1 Corinthians": "1CO",
    "2 Corinthians": "2CO",
    "Galatians": "GAL",
    "Ephesians": "EPH",
    "Philippians": "PHP",
    "Colossians": "COL",
    "1 Thessalonians": "1TH",
    "2 Thessalonians": "2TH",
    "1 Timothy": "1TI",
    "2 Timothy": "2TI",
    "Titus": "TIT",
    "Philemon": "PHM",
    "Hebrews": "HEB",
    "James": "JAS",
    "1 Peter": "1PE",
    "2 Peter": "2PE",
    "1 John": "1JN",
    "2 John": "2JN",
    "3 John": "3JN",
    "Jude": "JUD",
    "Revelation": "REV",
}

# KJV JSON source (public domain)
KJV_URL = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json"


def download_kjv():
    """Download KJV JSON from GitHub."""
    print("Downloading KJV Bible data...")
    cache_path = Path(__file__).parent / "kjv_cache.json"

    if cache_path.exists():
        print("Using cached KJV data...")
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    with urllib.request.urlopen(KJV_URL) as response:
        data = json.loads(response.read().decode("utf-8-sig"))

    # Cache for future runs
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    return data


def load_kjv():
    """Load KJV Bible into database."""
    # Create or get KJV translation
    translation, created = BibleTranslation.objects.get_or_create(
        code="KJV",
        defaults={
            "name": "King James Version",
            "language": "en",
            "is_public_domain": True,
            "provider_class": "apps.bible.providers.DatabaseProvider",
        },
    )

    if not created:
        print(
            f"KJV translation already exists with {BibleVerse.objects.filter(translation=translation).count()} verses"
        )
        response = input("Delete existing verses and reload? (y/N): ")
        if response.lower() != "y":
            print("Aborted.")
            return
        BibleVerse.objects.filter(translation=translation).delete()

    print("Loading KJV Bible...")
    kjv_data = download_kjv()

    verses_to_create = []

    for book_data in kjv_data:
        book_name = book_data.get("name", "")
        book_abbrev = book_data.get("abbrev", "").upper()

        # Try to get standard abbreviation
        if book_name in BOOK_ABBREVS:
            book_code = BOOK_ABBREVS[book_name]
        else:
            book_code = book_abbrev[:3].upper()

        chapters = book_data.get("chapters", [])

        for chapter_idx, chapter_verses in enumerate(chapters, start=1):
            for verse_idx, verse_text in enumerate(chapter_verses, start=1):
                verses_to_create.append(
                    BibleVerse(
                        translation=translation,
                        book=book_code,
                        book_name=book_name,
                        chapter=chapter_idx,
                        verse=verse_idx,
                        text=verse_text,
                    )
                )

        print(f"  Processed {book_name}: {len(chapters)} chapters")

    # Bulk create for performance
    print(f"Saving {len(verses_to_create)} verses to database...")
    BibleVerse.objects.bulk_create(verses_to_create, batch_size=1000)

    print(f"Done! Loaded {len(verses_to_create)} verses.")


if __name__ == "__main__":
    load_kjv()

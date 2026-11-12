"""
Load a whole Bible translation into the local database so scripture lookups
work with no outbound network (a mesh-only / offline install).

    python manage.py load_translation WEB
    python manage.py load_translation KJV --file /path/to/KJV.json

Without --file the translation is downloaded once from the Bolls API's bulk
export. The file is a JSON list of
    {"book": 1-66, "chapter": n, "verse": n, "text": "..."}
"""

import json

import requests
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.bible.bolls_api import ALLOWED_TRANSLATIONS
from apps.bible.books import BOOKS
from apps.bible.lookup import clean_verse_text
from apps.bible.models import BibleTranslation, BibleVerse

BULK_URL = "https://bolls.life/static/translations/{code}.json"


class Command(BaseCommand):
    help = "Load a public-domain Bible translation into the local database."

    def add_arguments(self, parser):
        parser.add_argument("code", help="Translation code, e.g. WEB or KJV")
        parser.add_argument(
            "--file", help="Read from a local JSON file instead of downloading"
        )
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Replace verses that are already loaded",
        )

    def handle(self, *args, **options):
        code = options["code"].upper()
        info = ALLOWED_TRANSLATIONS.get(code)
        if not info:
            raise CommandError(
                f"Unknown translation '{code}'. Choose one of: {', '.join(ALLOWED_TRANSLATIONS)}"
            )

        translation, _ = BibleTranslation.objects.get_or_create(
            code=code,
            defaults={
                "name": info["name"],
                "language": info["language"],
                "is_public_domain": info["public_domain"],
            },
        )
        existing = BibleVerse.objects.filter(translation=translation).count()
        if existing and not options["replace"]:
            self.stdout.write(
                f"{code} already has {existing} verses loaded. Use --replace to reload."
            )
            return

        if options["file"]:
            try:
                with open(options["file"], encoding="utf-8-sig") as handle:
                    rows = json.load(handle)
            except (OSError, ValueError) as exc:
                raise CommandError(f"Could not read {options['file']}: {exc}")
        else:
            url = BULK_URL.format(code=code)
            self.stdout.write(f"Downloading {url} ...")
            try:
                response = requests.get(url, timeout=120)
                response.raise_for_status()
                rows = response.json()
            except (requests.RequestException, ValueError) as exc:
                raise CommandError(
                    f"Download failed: {exc}. Download the file on another machine "
                    "and pass it with --file."
                )

        if not isinstance(rows, list) or not rows:
            raise CommandError("The translation file is empty or not a JSON list.")

        books = {book.number: book for book in BOOKS}
        verses = []
        skipped = 0
        for row in rows:
            try:
                book = books[int(row["book"])]
                chapter, verse = int(row["chapter"]), int(row["verse"])
            except (KeyError, TypeError, ValueError):
                skipped += 1  # e.g. deuterocanonical books (number > 66)
                continue
            text = clean_verse_text(str(row.get("text", "")))
            if not text:
                skipped += 1
                continue
            verses.append(
                BibleVerse(
                    translation=translation,
                    book=book.code,
                    book_name=book.name,
                    chapter=chapter,
                    verse=verse,
                    text=text,
                )
            )

        if not verses:
            raise CommandError("No usable verses were found in the file.")

        with transaction.atomic():
            BibleVerse.objects.filter(translation=translation).delete()
            BibleVerse.objects.bulk_create(verses, batch_size=2000)

        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded {len(verses)} verses of {info['name']} ({skipped} rows skipped)."
            )
        )

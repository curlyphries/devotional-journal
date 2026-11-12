"""
Canonical table of the 66 books: number (as used by the Bolls API), the
three-letter code stored in BibleVerse.book, and the display name.

Single source of truth for turning whatever a person or a model wrote
("1 Cor", "Psalm", "Song of Songs") into a book we can actually look up.
"""

import re
from typing import NamedTuple, Optional


class Book(NamedTuple):
    number: int
    code: str
    name: str


_BOOKS = [
    ("GEN", "Genesis"),
    ("EXO", "Exodus"),
    ("LEV", "Leviticus"),
    ("NUM", "Numbers"),
    ("DEU", "Deuteronomy"),
    ("JOS", "Joshua"),
    ("JDG", "Judges"),
    ("RUT", "Ruth"),
    ("1SA", "1 Samuel"),
    ("2SA", "2 Samuel"),
    ("1KI", "1 Kings"),
    ("2KI", "2 Kings"),
    ("1CH", "1 Chronicles"),
    ("2CH", "2 Chronicles"),
    ("EZR", "Ezra"),
    ("NEH", "Nehemiah"),
    ("EST", "Esther"),
    ("JOB", "Job"),
    ("PSA", "Psalms"),
    ("PRO", "Proverbs"),
    ("ECC", "Ecclesiastes"),
    ("SNG", "Song of Solomon"),
    ("ISA", "Isaiah"),
    ("JER", "Jeremiah"),
    ("LAM", "Lamentations"),
    ("EZK", "Ezekiel"),
    ("DAN", "Daniel"),
    ("HOS", "Hosea"),
    ("JOL", "Joel"),
    ("AMO", "Amos"),
    ("OBA", "Obadiah"),
    ("JON", "Jonah"),
    ("MIC", "Micah"),
    ("NAH", "Nahum"),
    ("HAB", "Habakkuk"),
    ("ZEP", "Zephaniah"),
    ("HAG", "Haggai"),
    ("ZEC", "Zechariah"),
    ("MAL", "Malachi"),
    ("MAT", "Matthew"),
    ("MRK", "Mark"),
    ("LUK", "Luke"),
    ("JHN", "John"),
    ("ACT", "Acts"),
    ("ROM", "Romans"),
    ("1CO", "1 Corinthians"),
    ("2CO", "2 Corinthians"),
    ("GAL", "Galatians"),
    ("EPH", "Ephesians"),
    ("PHP", "Philippians"),
    ("COL", "Colossians"),
    ("1TH", "1 Thessalonians"),
    ("2TH", "2 Thessalonians"),
    ("1TI", "1 Timothy"),
    ("2TI", "2 Timothy"),
    ("TIT", "Titus"),
    ("PHM", "Philemon"),
    ("HEB", "Hebrews"),
    ("JAS", "James"),
    ("1PE", "1 Peter"),
    ("2PE", "2 Peter"),
    ("1JN", "1 John"),
    ("2JN", "2 John"),
    ("3JN", "3 John"),
    ("JUD", "Jude"),
    ("REV", "Revelation"),
]

BOOKS = [Book(i, code, name) for i, (code, name) in enumerate(_BOOKS, start=1)]

# Extra spellings people and models actually use.
_ALIASES = {
    "GEN": ["gn"],
    "EXO": ["ex", "exod"],
    "DEU": ["deut", "dt"],
    "JOS": ["josh"],
    "JDG": ["judg"],
    "1SA": ["1sam"],
    "2SA": ["2sam"],
    "1KI": ["1kgs"],
    "2KI": ["2kgs"],
    "1CH": ["1chr", "1chron"],
    "2CH": ["2chr", "2chron"],
    "PSA": ["psalm", "ps", "pss", "salmos", "salmo"],
    "PRO": ["prov", "prv", "proverbios"],
    "ECC": ["eccl", "eccles", "qoheleth"],
    "SNG": ["songofsongs", "song", "canticles", "sos"],
    "EZK": ["ezek", "eze"],
    "JOL": ["joe"],
    "OBA": ["obad"],
    "JON": ["jnh"],
    "NAH": ["nam"],
    "ZEP": ["zeph"],
    "ZEC": ["zech"],
    "MAT": ["matt", "mt", "mateo"],
    "MRK": ["mk", "mar", "marcos"],
    "LUK": ["lk", "lucas"],
    "JHN": ["jn", "joh", "juan"],
    "ACT": ["hechos"],
    "ROM": ["rm", "romanos"],
    "1CO": ["1cor"],
    "2CO": ["2cor"],
    "EPH": ["efesios"],
    "PHP": ["phil", "filipenses"],
    "1TH": ["1thess", "1thes"],
    "2TH": ["2thess", "2thes"],
    "1TI": ["1tim"],
    "2TI": ["2tim"],
    "PHM": ["phlm", "philem"],
    "JAS": ["jm", "santiago"],
    "1PE": ["1pet", "1pt"],
    "2PE": ["2pet", "2pt"],
    "1JN": ["1jo", "1joh"],
    "2JN": ["2jo", "2joh"],
    "3JN": ["3jo", "3joh"],
    "REV": ["revelations", "apocalypse", "apocalipsis", "rv"],
}

_ROMAN = {"i": "1", "ii": "2", "iii": "3", "first": "1", "second": "2", "third": "3"}


def _key(text: str) -> str:
    text = text.strip().lower()
    # "II Timothy" / "First John" -> "2 timothy" / "1 john"
    match = re.match(r"^(i{1,3}|first|second|third)\s+(.*)$", text)
    if match:
        text = _ROMAN[match.group(1)] + match.group(2)
    return re.sub(r"[^a-z0-9]", "", text)


_LOOKUP: dict[str, Book] = {}
for _book in BOOKS:
    for _spelling in [_book.code, _book.name, *_ALIASES.get(_book.code, [])]:
        _LOOKUP[_key(_spelling)] = _book
    _LOOKUP[str(_book.number)] = _book


def find_book(value) -> Optional[Book]:
    """Resolve a name, abbreviation, code or 1-66 number to a Book, else None."""
    if value is None:
        return None
    return _LOOKUP.get(_key(str(value)))


_REFERENCE_RE = re.compile(
    r"^\s*(?P<book>(?:[1-3]|i{1,3}|first|second|third)?\s*[A-Za-zñÑáéíóú. ]+?)\.?\s*"
    r"(?P<chapter>\d+)(?:\s*[:.]\s*(?P<start>\d+)(?:\s*[-–—]\s*(?P<end>\d+))?)?\s*$",
    re.IGNORECASE,
)


class ParsedReference(NamedTuple):
    book: Book
    chapter: int
    verse_start: Optional[int]
    verse_end: Optional[int]

    @property
    def label(self) -> str:
        return format_reference(
            self.book, self.chapter, self.verse_start, self.verse_end
        )


def parse_reference(text: str) -> Optional[ParsedReference]:
    """Parse "1 Corinthians 13:4-7", "Psalm 23", "Jn 3:16". None if unrecognised."""
    if not text:
        return None
    match = _REFERENCE_RE.match(str(text))
    if not match:
        return None
    book = find_book(match.group("book"))
    if not book:
        return None
    start = int(match.group("start")) if match.group("start") else None
    end = int(match.group("end")) if match.group("end") else start
    if start is not None and end is not None and end < start:
        end = start
    return ParsedReference(book, int(match.group("chapter")), start, end)


def format_reference(
    book: Book, chapter: int, verse_start: Optional[int], verse_end: Optional[int]
) -> str:
    if verse_start is None:
        return f"{book.name} {chapter}"
    if verse_end is None or verse_end == verse_start:
        return f"{book.name} {chapter}:{verse_start}"
    return f"{book.name} {chapter}:{verse_start}-{verse_end}"

"""
Bible Text Verification System

Verifies text from Bolls API against trusted sources to detect modifications.
Uses multiple verification methods:
1. Cross-reference with bible-api.com (canonical public domain texts)
2. Cross-reference with locally stored KJV (already verified)
3. Text similarity analysis with tolerance for minor formatting differences
"""

import hashlib
import logging
import re
from difflib import SequenceMatcher
from typing import Optional

import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Trusted source: bible-api.com (serves WEB translation - public domain)
BIBLE_API_BASE = "https://bible-api.com"

# Verification thresholds
SIMILARITY_THRESHOLD = 0.95  # 95% match required
EXACT_MATCH_THRESHOLD = 1.0


class VerificationResult:
    """Result of a text verification check."""

    def __init__(
        self,
        verified: bool,
        confidence: float,
        source_text: str,
        reference_text: str,
        reference_source: str,
        differences: list = None,
        warnings: list = None,
    ):
        self.verified = verified
        self.confidence = confidence  # 0.0 to 1.0
        self.source_text = source_text
        self.reference_text = reference_text
        self.reference_source = reference_source
        self.differences = differences or []
        self.warnings = warnings or []

    def to_dict(self):
        return {
            "verified": self.verified,
            "confidence": round(self.confidence, 4),
            "confidence_percent": f"{self.confidence * 100:.1f}%",
            "reference_source": self.reference_source,
            "differences": self.differences,
            "warnings": self.warnings,
            "source_text_preview": (
                self.source_text[:200] + "..."
                if len(self.source_text) > 200
                else self.source_text
            ),
            "reference_text_preview": (
                self.reference_text[:200] + "..."
                if len(self.reference_text) > 200
                else self.reference_text
            ),
        }


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison.
    Removes formatting artifacts while preserving meaning.
    """
    if not text:
        return ""

    # Remove Strong's numbers (e.g., <S>1234</S>)
    text = re.sub(r"<S>\d+</S>", "", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    # Normalize quotes and apostrophes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(""", "'").replace(""", "'")

    # Normalize dashes
    text = text.replace("—", "-").replace("–", "-")

    # Lowercase for comparison (preserves meaning)
    text = text.lower()

    return text


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity ratio between two texts."""
    if not text1 or not text2:
        return 0.0

    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)

    return SequenceMatcher(None, norm1, norm2).ratio()


def find_differences(text1: str, text2: str) -> list:
    """Find specific differences between two texts."""
    differences = []

    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)

    words1 = norm1.split()
    words2 = norm2.split()

    matcher = SequenceMatcher(None, words1, words2)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "replace":
            differences.append(
                {
                    "type": "changed",
                    "source": " ".join(words1[i1:i2]),
                    "reference": " ".join(words2[j1:j2]),
                }
            )
        elif tag == "delete":
            differences.append(
                {
                    "type": "removed_from_source",
                    "source": " ".join(words1[i1:i2]),
                    "reference": None,
                }
            )
        elif tag == "insert":
            differences.append(
                {
                    "type": "added_in_source",
                    "source": None,
                    "reference": " ".join(words2[j1:j2]),
                }
            )

    return differences


def fetch_from_bible_api(reference: str) -> Optional[str]:
    """
    Fetch verse from bible-api.com (trusted source).
    Reference format: "John 3:16" or "John 3:16-17"
    Returns WEB translation text.
    """
    cache_key = f"bible_api_verify:{reference}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        url = f"{BIBLE_API_BASE}/{reference}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "text" in data:
            text = data["text"]
            cache.set(cache_key, text, 60 * 60 * 24 * 30)  # Cache 30 days
            return text

        return None
    except Exception as e:
        logger.warning(f"bible-api.com fetch failed for {reference}: {e}")
        return None


def verify_against_local_kjv(
    book: str, chapter: int, verse: int, text: str
) -> Optional[VerificationResult]:
    """
    Verify text against locally stored KJV.
    Only works for KJV translation.
    """
    from .models import BibleTranslation, BibleVerse

    try:
        translation = BibleTranslation.objects.get(code="KJV")
        local_verse = BibleVerse.objects.filter(
            translation=translation, book__iexact=book, chapter=chapter, verse=verse
        ).first()

        if not local_verse:
            return None

        similarity = calculate_similarity(text, local_verse.text)
        differences = (
            find_differences(text, local_verse.text)
            if similarity < EXACT_MATCH_THRESHOLD
            else []
        )

        warnings = []
        if similarity < SIMILARITY_THRESHOLD:
            warnings.append(
                f"Text differs significantly from local KJV ({similarity*100:.1f}% match)"
            )

        return VerificationResult(
            verified=similarity >= SIMILARITY_THRESHOLD,
            confidence=similarity,
            source_text=text,
            reference_text=local_verse.text,
            reference_source="Local KJV Database (31,100 verified verses)",
            differences=differences,
            warnings=warnings,
        )
    except Exception as e:
        logger.warning(f"Local KJV verification failed: {e}")
        return None


def verify_against_bible_api(reference: str, text: str) -> Optional[VerificationResult]:
    """
    Verify text against bible-api.com (WEB translation).
    Good for cross-checking modern English translations.
    """
    reference_text = fetch_from_bible_api(reference)

    if not reference_text:
        return None

    similarity = calculate_similarity(text, reference_text)
    differences = (
        find_differences(text, reference_text)
        if similarity < EXACT_MATCH_THRESHOLD
        else []
    )

    warnings = []
    # WEB vs other translations will have natural differences
    # We're checking for meaning preservation, not exact match
    if similarity < 0.7:  # Lower threshold for cross-translation
        warnings.append(
            f"Significant differences from WEB translation ({similarity*100:.1f}% match)"
        )

    return VerificationResult(
        verified=similarity >= 0.7,  # Cross-translation threshold
        confidence=similarity,
        source_text=text,
        reference_text=reference_text,
        reference_source="bible-api.com (World English Bible - Public Domain)",
        differences=differences,
        warnings=warnings,
    )


def verify_verse(
    translation: str, book: str, chapter: int, verse: int, text: str
) -> dict:
    """
    Main verification function.
    Attempts multiple verification methods and returns combined result.
    """
    results = {
        "translation": translation,
        "reference": f"{book} {chapter}:{verse}",
        "text_hash": hashlib.sha256(normalize_text(text).encode()).hexdigest()[:16],
        "verifications": [],
        "overall_verified": False,
        "overall_confidence": 0.0,
        "warnings": [],
    }

    # Method 1: Local KJV verification (if KJV translation)
    if translation.upper() == "KJV":
        local_result = verify_against_local_kjv(book, chapter, verse, text)
        if local_result:
            results["verifications"].append(
                {"method": "local_kjv", **local_result.to_dict()}
            )

    # Method 2: Cross-reference with bible-api.com
    reference = f"{book} {chapter}:{verse}"
    api_result = verify_against_bible_api(reference, text)
    if api_result:
        results["verifications"].append(
            {"method": "bible_api_com", **api_result.to_dict()}
        )

    # Calculate overall verification status
    if results["verifications"]:
        confidences = [v["confidence"] for v in results["verifications"]]
        results["overall_confidence"] = max(confidences)
        results["overall_verified"] = any(
            v["verified"] for v in results["verifications"]
        )

        # Collect all warnings
        for v in results["verifications"]:
            results["warnings"].extend(v.get("warnings", []))
    else:
        results["warnings"].append("No verification sources available for this verse")

    return results


def verify_chapter(translation: str, book: str, chapter: int, verses: list) -> dict:
    """
    Verify an entire chapter of verses.
    Returns summary statistics and any problematic verses.
    """
    results = {
        "translation": translation,
        "reference": f"{book} {chapter}",
        "total_verses": len(verses),
        "verified_count": 0,
        "failed_count": 0,
        "unverifiable_count": 0,
        "average_confidence": 0.0,
        "problematic_verses": [],
        "summary": "",
    }

    confidences = []

    for v in verses:
        verse_num = v.get("verse")
        text = v.get("text", "")

        if not text:
            results["unverifiable_count"] += 1
            continue

        verification = verify_verse(translation, book, chapter, verse_num, text)

        if verification["overall_verified"]:
            results["verified_count"] += 1
        elif verification["verifications"]:
            results["failed_count"] += 1
            results["problematic_verses"].append(
                {
                    "verse": verse_num,
                    "confidence": verification["overall_confidence"],
                    "warnings": verification["warnings"],
                }
            )
        else:
            results["unverifiable_count"] += 1

        if verification["overall_confidence"] > 0:
            confidences.append(verification["overall_confidence"])

    if confidences:
        results["average_confidence"] = sum(confidences) / len(confidences)

    # Generate summary
    if results["failed_count"] == 0 and results["verified_count"] > 0:
        results["summary"] = (
            f"✅ All {results['verified_count']} verifiable verses passed integrity check"
        )
    elif results["failed_count"] > 0:
        results["summary"] = (
            f"⚠️ {results['failed_count']} verses have potential integrity issues"
        )
    else:
        results["summary"] = "❓ Unable to verify - no reference sources available"

    return results

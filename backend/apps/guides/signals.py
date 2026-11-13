"""
What the app can see about a person, gathered in one place.

Recommendations, the profile and AI prompts all read from here, so there is
exactly one answer to "what did the app look at?". Nothing here is stored;
it is recomputed from the person's own (encrypted) records each time.
"""

import logging
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import timedelta

from django.utils import timezone

from .catalog import ASSESSMENT_ITEMS
from .models import (
    GrowthPlan,
    GrowthProfile,
    LessonResponse,
    ProfileAssessment,
    StudyEnrollment,
)

logger = logging.getLogger(__name__)

CRISIS_PATTERNS = [
    r"kill myself",
    r"end my life",
    r"suicid",
    r"don'?t want to (live|be alive|be here)",
    r"better off without me",
    r"hurt myself",
    r"harm myself",
    r"no reason to live",
    r"quitarme la vida",
    r"no quiero (seguir )?vivir",
    r"matarme",
    r"hacerme daño",
    r"estar[ií]an mejor sin m[ií]",
    r"acabar con (mi vida|todo)",
]
CRISIS_RE = re.compile("|".join(CRISIS_PATTERNS), re.IGNORECASE)


@dataclass
class Signals:
    profile: GrowthProfile = None
    assessment: dict = None  # latest {"answers", "trait_ratings"} or None
    assessment_taken_at: object = None
    themes: Counter = field(default_factory=Counter)  # from journal feedback
    moods: Counter = field(default_factory=Counter)  # mood tags, last 30 entries
    recent_moods: list = field(default_factory=list)  # last 14 days, newest first
    entry_texts: list = field(default_factory=list)  # recent entries without feedback
    entries_considered: int = 0
    entries_with_feedback: int = 0
    responses: list = field(
        default_factory=list
    )  # completed LessonResponse, newest first
    enrollments: list = field(default_factory=list)
    plans: list = field(default_factory=list)  # active GrowthPlan
    open_threads: int = 0
    crisis_language: bool = False

    @property
    def life_stage(self) -> str:
        return self.profile.life_stage if self.profile else ""

    @property
    def completed_topics(self) -> set:
        return {e.topic_key for e in self.enrollments if e.status == "completed"}

    @property
    def active_topics(self) -> set:
        return {e.topic_key for e in self.enrollments if e.status == "active"}

    def averages(self) -> dict:
        """Average of answered assessment items per area (None if none answered)."""
        answers = (self.assessment or {}).get("answers", {})
        out = {}
        for area in ("practices", "inner"):
            scores = [
                answers[item["key"]]
                for item in ASSESSMENT_ITEMS
                if item["area"] == area and isinstance(answers.get(item["key"]), int)
            ]
            out[area] = round(sum(scores) / len(scores), 2) if scores else None
        return out


def gather(user) -> Signals:
    from apps.journal.feedback import strip_metadata
    from apps.journal.models import JournalEntry, JournalFeedback
    from apps.reflections.models import OpenThread

    signals = Signals()
    signals.profile = (
        GrowthProfile.objects.filter(user=user).select_related("user").first()
    )

    latest = ProfileAssessment.objects.filter(user=user).select_related("user").first()
    if latest:
        signals.assessment = latest.get_payload()
        signals.assessment_taken_at = latest.taken_at

    entries = list(JournalEntry.objects.filter(user=user).select_related("user")[:30])
    signals.entries_considered = len(entries)
    signals.moods = Counter(e.mood_tag for e in entries if e.mood_tag)
    cutoff = timezone.localdate() - timedelta(days=14)
    signals.recent_moods = [
        e.mood_tag for e in entries if e.mood_tag and e.date >= cutoff
    ]

    feedback = list(
        JournalFeedback.objects.filter(user=user, is_current=True)
        .select_related("user")
        .order_by("-created_at")[:30]
    )
    signals.entries_with_feedback = len(feedback)
    with_feedback = set()
    for record in feedback:
        with_feedback.add(record.entry_id)
        try:
            signals.themes.update(record.get_payload().get("themes", []))
        except Exception:  # noqa: BLE001 - one unreadable record must not hide the rest
            logger.warning("could not read feedback payload %s", record.id)

    scanned = []
    for entry in entries[:10]:
        try:
            text = strip_metadata(entry.get_content())
        except Exception:  # noqa: BLE001
            continue
        scanned.append(text)
        if entry.id not in with_feedback and text:
            signals.entry_texts.append(text[:1500])

    signals.enrollments = list(StudyEnrollment.objects.filter(user=user))
    signals.responses = list(
        LessonResponse.objects.filter(enrollment__user=user, completed_at__isnull=False)
        .select_related("enrollment", "enrollment__user")
        .order_by("-completed_at")[:40]
    )
    signals.plans = list(
        GrowthPlan.objects.filter(user=user, status="active").select_related("user")
    )
    signals.open_threads = OpenThread.objects.filter(
        user=user, status__in=["open", "following_up", "progressing"]
    ).count()

    for response in signals.responses[:5]:
        try:
            payload = response.get_payload()
        except Exception:  # noqa: BLE001
            continue
        scanned.append(payload.get("stood_out", ""))
        scanned.extend(a.get("answer", "") for a in payload.get("answers", []))
    if signals.profile:
        try:
            scanned.append(signals.profile.get_about_me())
        except Exception:  # noqa: BLE001
            pass
    signals.crisis_language = any(CRISIS_RE.search(text or "") for text in scanned[:25])
    return signals

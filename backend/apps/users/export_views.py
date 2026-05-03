"""
Data export views — full JSON export and formatted Markdown exports.
"""

import io
import json
import zipfile
from datetime import datetime, timezone

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.bible.models import VerseHighlight
from apps.journal.models import JournalEntry
from apps.plans.models import ReadingPlan, ReadingPlanDay, UserPlanEnrollment
from apps.reflections.models import (
    DailyReflection,
    FocusIntention,
    OpenThread,
    UserJourney,
)


def _iso(dt):
    """Safe ISO format for datetimes."""
    return dt.isoformat() if dt else None


class FullDataExportView(APIView):
    """
    GET /api/v1/me/export/
    Returns a ZIP containing all user data as JSON files.
    Covers GDPR data portability.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        buf = io.BytesIO()

        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            # Profile
            zf.writestr(
                "profile.json",
                json.dumps(
                    {
                        "id": str(user.id),
                        "email": user.email,
                        "display_name": user.display_name,
                        "language_preference": user.language_preference,
                        "timezone": user.timezone,
                        "created_at": _iso(user.created_at),
                        "last_active_at": _iso(user.last_active_at),
                    },
                    indent=2,
                ),
            )

            # Journal entries (decrypted)
            entries = JournalEntry.objects.filter(user=user).order_by("date")
            zf.writestr(
                "journal-entries.json",
                json.dumps(
                    [
                        {
                            "id": str(e.id),
                            "date": e.date.isoformat(),
                            "mood": e.mood_tag,
                            "content": e.get_content(),
                            "focus_themes": e.focus_themes,
                            "created_at": _iso(e.created_at),
                        }
                        for e in entries
                    ],
                    indent=2,
                ),
            )

            # Highlights
            highlights = VerseHighlight.objects.filter(user=user).order_by("created_at")
            zf.writestr(
                "highlights.json",
                json.dumps(
                    [
                        {
                            "id": str(h.id),
                            "book": h.book,
                            "chapter": h.chapter,
                            "verse_start": h.verse_start,
                            "verse_end": h.verse_end,
                            "translation": h.translation,
                            "color": h.color,
                            "note": h.note,
                            "created_at": _iso(h.created_at),
                        }
                        for h in highlights
                    ],
                    indent=2,
                ),
            )

            # Reflections (decrypted)
            reflections = DailyReflection.objects.filter(user=user).order_by("date")
            zf.writestr(
                "reflections.json",
                json.dumps(
                    [
                        {
                            "id": str(r.id),
                            "date": r.date.isoformat(),
                            "scripture_reference": r.scripture_reference,
                            "scripture_themes": r.scripture_themes,
                            "reflection": r.get_reflection(),
                            "gratitude": r.get_gratitude_note(),
                            "struggle": r.get_struggle_note(),
                            "tomorrow_intention": r.get_tomorrow_intention(),
                            "area_scores": r.area_scores,
                            "ai_insight": r.ai_insight,
                            "created_at": _iso(r.created_at),
                        }
                        for r in reflections
                    ],
                    indent=2,
                ),
            )

            # Open threads (decrypted)
            threads = OpenThread.objects.filter(user=user).order_by("created_at")
            thread_data = []
            for t in threads:
                summary = ""
                try:
                    from shared.encryption import decrypt_content

                    if t.encrypted_summary:
                        summary = decrypt_content(
                            bytes(t.encrypted_summary), user.encryption_key_salt
                        )
                except Exception:
                    summary = "(unable to decrypt)"
                thread_data.append(
                    {
                        "id": str(t.id),
                        "thread_type": t.thread_type,
                        "summary": summary,
                        "status": t.status,
                        "related_life_area": t.related_life_area,
                        "created_at": _iso(t.created_at),
                        "resolved_at": _iso(t.resolved_at),
                    }
                )
            zf.writestr("threads.json", json.dumps(thread_data, indent=2))

            # Reading plans (owned by user)
            plans = ReadingPlan.objects.filter(created_by=user)
            plan_list = []
            for p in plans:
                days = ReadingPlanDay.objects.filter(plan=p).order_by("day_number")
                plan_list.append(
                    {
                        "id": str(p.id),
                        "title": p.title_en,
                        "title_es": p.title_es,
                        "description": p.description_en,
                        "category": p.category,
                        "duration_days": p.duration_days,
                        "is_public": p.is_public,
                        "days": [
                            {
                                "day_number": d.day_number,
                                "passages": d.passages,
                                "theme_en": d.theme_en,
                                "theme_es": d.theme_es,
                            }
                            for d in days
                        ],
                    }
                )
            zf.writestr("plans.json", json.dumps(plan_list, indent=2))

            # Enrollments
            enrollments = UserPlanEnrollment.objects.filter(user=user).select_related(
                "plan"
            )
            zf.writestr(
                "enrollments.json",
                json.dumps(
                    [
                        {
                            "plan_title": e.plan.title_en,
                            "current_day": e.current_day,
                            "total_days": e.plan.duration_days,
                            "started_at": _iso(e.started_at),
                            "completed_at": _iso(e.completed_at),
                            "is_active": e.is_active,
                        }
                        for e in enrollments
                    ],
                    indent=2,
                ),
            )

            # Focus intentions
            intentions = FocusIntention.objects.filter(user=user).order_by(
                "-created_at"
            )
            zf.writestr(
                "focus-intentions.json",
                json.dumps(
                    [
                        {
                            "id": str(fi.id),
                            "intention_text": fi.intention_text,
                            "themes": fi.themes,
                            "period_type": fi.period_type,
                            "is_active": fi.is_active,
                            "created_at": _iso(fi.created_at),
                        }
                        for fi in intentions
                    ],
                    indent=2,
                ),
            )

            # Journeys
            journeys = UserJourney.objects.filter(user=user).order_by("-created_at")
            zf.writestr(
                "journeys.json",
                json.dumps(
                    [
                        {
                            "id": str(j.id),
                            "title": j.title,
                            "goal_statement": j.goal_statement,
                            "success_definition": j.success_definition,
                            "duration_days": j.duration_days,
                            "current_day": j.current_day,
                            "status": j.status,
                            "focus_areas": j.focus_areas,
                            "created_at": _iso(j.created_at),
                        }
                        for j in journeys
                    ],
                    indent=2,
                ),
            )

        buf.seek(0)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        response = HttpResponse(buf.read(), content_type="application/zip")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="devotional-journal-export-{timestamp}.zip"'
        return response


class JournalMarkdownExportView(APIView):
    """
    GET /api/v1/me/export/journal/
    Returns journal entries as a formatted Markdown file.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        entries = JournalEntry.objects.filter(user=user).order_by("date")

        lines = [
            f"# Journal — {user.display_name or user.email}",
            f"*Exported {datetime.now(timezone.utc).strftime('%B %d, %Y')}*",
            "",
        ]

        current_month = None
        for e in entries:
            month_label = e.date.strftime("%B %Y")
            if month_label != current_month:
                current_month = month_label
                lines.append(f"\n---\n\n## {month_label}\n")

            mood = f" — _{e.mood_tag}_" if e.mood_tag else ""
            lines.append(f"### {e.date.strftime('%A, %B %d')}{mood}\n")

            content = e.get_content()
            # Strip metadata blocks from display
            if "<!-- DJ_META_START -->" in content:
                idx = content.find("<!-- DJ_META_END -->")
                if idx != -1:
                    content = content[idx + len("<!-- DJ_META_END -->") :].strip()

            lines.append(content)
            lines.append("")

        md = "\n".join(lines)
        response = HttpResponse(md, content_type="text/markdown; charset=utf-8")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="journal-entries.md"'
        return response


class HighlightsMarkdownExportView(APIView):
    """
    GET /api/v1/me/export/highlights/
    Returns highlights grouped by book as Markdown.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        highlights = VerseHighlight.objects.filter(user=user).order_by(
            "book", "chapter", "verse_start"
        )

        lines = [
            f"# Highlights — {user.display_name or user.email}",
            f"*Exported {datetime.now(timezone.utc).strftime('%B %d, %Y')}*",
            "",
        ]

        current_book = None
        for h in highlights:
            if h.book != current_book:
                current_book = h.book
                lines.append(f"\n## {h.book}\n")

            verse_ref = f"{h.chapter}:{h.verse_start}"
            if h.verse_end and h.verse_end != h.verse_start:
                verse_ref += f"-{h.verse_end}"

            color_emoji = {
                "yellow": "🟡",
                "green": "🟢",
                "blue": "🔵",
                "pink": "🩷",
                "orange": "🟠",
            }.get(h.color, "")

            lines.append(f"- **{h.book} {verse_ref}** {color_emoji}")
            if h.note:
                lines.append(f"  > {h.note}")
            lines.append("")

        md = "\n".join(lines)
        response = HttpResponse(md, content_type="text/markdown; charset=utf-8")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="highlights.md"'
        return response


class GrowthReportExportView(APIView):
    """
    GET /api/v1/me/export/growth/
    Returns a Markdown growth report: reflections summary, area scores, threads resolved.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        reflections = DailyReflection.objects.filter(user=user).order_by("date")
        threads = OpenThread.objects.filter(user=user)
        entries = JournalEntry.objects.filter(user=user)
        highlights = VerseHighlight.objects.filter(user=user)
        enrollments = UserPlanEnrollment.objects.filter(user=user)

        total_reflections = reflections.count()
        total_entries = entries.count()
        total_highlights = highlights.count()
        resolved_threads = threads.filter(status="resolved").count()
        open_threads = threads.filter(status__in=["open", "following_up", "progressing"]).count()
        completed_plans = enrollments.filter(completed_at__isnull=False).count()

        # Aggregate life area scores
        area_totals = {}
        area_counts = {}
        for r in reflections:
            if r.area_scores:
                for area, score in r.area_scores.items():
                    area_totals[area] = area_totals.get(area, 0) + score
                    area_counts[area] = area_counts.get(area, 0) + 1

        area_averages = {
            area: round(area_totals[area] / area_counts[area], 1)
            for area in sorted(area_totals.keys())
        }

        # Mood distribution
        mood_counts = {}
        for e in entries:
            if e.mood_tag:
                mood_counts[e.mood_tag] = mood_counts.get(e.mood_tag, 0) + 1

        # Date range
        first_date = None
        last_date = None
        if reflections.exists():
            first_date = reflections.first().date
            last_date = reflections.last().date
        elif entries.exists():
            first_entry = entries.order_by("date").first()
            last_entry = entries.order_by("-date").first()
            first_date = first_entry.date if first_entry else None
            last_date = last_entry.date if last_entry else None

        lines = [
            f"# Growth Report — {user.display_name or user.email}",
            f"*Exported {datetime.now(timezone.utc).strftime('%B %d, %Y')}*",
            "",
        ]

        if first_date and last_date:
            days = (last_date - first_date).days + 1
            lines.append(
                f"**Period:** {first_date.strftime('%B %d, %Y')} – {last_date.strftime('%B %d, %Y')} ({days} days)"
            )
            lines.append("")

        lines.append("## Summary\n")
        lines.append(f"| Metric | Count |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Journal entries | {total_entries} |")
        lines.append(f"| Daily reflections | {total_reflections} |")
        lines.append(f"| Verse highlights | {total_highlights} |")
        lines.append(f"| Reading plans completed | {completed_plans} |")
        lines.append(f"| Threads resolved | {resolved_threads} |")
        lines.append(f"| Threads still open | {open_threads} |")
        lines.append("")

        if area_averages:
            lines.append("## Life Area Averages\n")
            lines.append("| Area | Average Score (1-10) |")
            lines.append("|------|---------------------|")
            for area, avg in area_averages.items():
                bar = "█" * int(avg) + "░" * (10 - int(avg))
                lines.append(f"| {area.replace('_', ' ').title()} | {avg} {bar} |")
            lines.append("")

        if mood_counts:
            lines.append("## Mood Distribution\n")
            total_moods = sum(mood_counts.values())
            mood_emojis = {
                "grateful": "🙏",
                "struggling": "😔",
                "convicted": "💭",
                "peaceful": "😌",
                "fired_up": "🔥",
            }
            for mood, count in sorted(
                mood_counts.items(), key=lambda x: x[1], reverse=True
            ):
                pct = round(count / total_moods * 100)
                emoji = mood_emojis.get(mood, "")
                lines.append(f"- {emoji} **{mood.replace('_', ' ').title()}**: {count} ({pct}%)")
            lines.append("")

        # Recent resolved threads
        resolved = threads.filter(status="resolved").order_by("-resolved_at")[:5]
        if resolved:
            lines.append("## Recently Resolved Threads\n")
            from shared.encryption import decrypt_content

            for t in resolved:
                summary = ""
                try:
                    if t.encrypted_summary:
                        summary = decrypt_content(
                            bytes(t.encrypted_summary), user.encryption_key_salt
                        )
                except Exception:
                    summary = "(encrypted)"
                resolved_date = (
                    t.resolved_at.strftime("%B %d") if t.resolved_at else "Unknown"
                )
                lines.append(
                    f"- ✅ **{t.thread_type.replace('_', ' ').title()}** — {summary} *(resolved {resolved_date})*"
                )
            lines.append("")

        md = "\n".join(lines)
        response = HttpResponse(md, content_type="text/markdown; charset=utf-8")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="growth-report.md"'
        return response

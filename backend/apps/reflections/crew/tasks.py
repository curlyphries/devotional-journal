"""
Crew tasks for different guidance scenarios.
"""

import logging
from datetime import date, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


class BaseTask:
    """Base class for crew tasks."""

    def __init__(self, crew):
        self.crew = crew

    def execute(self, user, **kwargs) -> Optional[str]:
        """Execute the task and return result."""
        raise NotImplementedError


class DailyInsightTask(BaseTask):
    """Generate daily insight for a reflection."""

    def execute(self, user, reflection=None, **kwargs) -> Optional[str]:
        """Generate insight for today's reflection."""
        if not reflection:
            return None

        context = self._build_context(user, reflection)

        # For daily insights, we use a simplified flow
        # Just the mentor and coordinator
        mentor_output = self.crew.mentor.generate(
            f"The user reflected: {reflection.get_reflection()[:500]}\n"
            f"They're grateful for: {reflection.get_gratitude_note()}\n"
            f"They struggled with: {reflection.get_struggle_note()}\n"
            f"Offer brief, practical encouragement.",
            context,
        )

        if not mentor_output:
            return None

        # Coordinator synthesizes (simplified for daily)
        return self.crew.coordinator.generate(
            f"Based on this mentor insight:\n{mentor_output}\n\n"
            f"Create a brief (2-3 sentences) encouraging response for the user. "
            f"End with a thought for tomorrow.",
            context,
        )

    def _build_context(self, user, reflection) -> dict:
        from ..models import OpenThread, UserJourney

        journey = UserJourney.objects.filter(user=user, status="active").first()
        open_threads = OpenThread.objects.filter(
            user=user, status__in=["open", "following_up"]
        ).count()

        return {
            "scripture": reflection.scripture_reference,
            "themes": reflection.scripture_themes,
            "goal": journey.goal_statement if journey else "Not specified",
            "day_in_journey": journey.current_day if journey else 0,
            "open_threads": open_threads,
        }


class WeeklyReviewTask(BaseTask):
    """Generate weekly review with full crew analysis."""

    def execute(self, user, **kwargs) -> Optional[str]:
        """Generate comprehensive weekly review."""
        context = self._build_context(user)

        if not context.get("reflections"):
            return "No reflections this week to review."

        # Run all agents
        agent_outputs = {}

        # Scripture Scholar
        agent_outputs["scripture"] = self.crew.scripture_scholar.generate(
            f"The user read these passages this week: {context['scriptures']}\n"
            f"Their main struggles were: {context['struggles']}\n"
            f"What biblical wisdom connects to their situation?",
            context,
        )

        # Mentor
        agent_outputs["mentor"] = self.crew.mentor.generate(
            f"This week the user:\n"
            f"- Reflected {context['reflection_count']} times\n"
            f"- Struggled with: {context['struggles']}\n"
            f"- Was grateful for: {context['gratitudes']}\n"
            f"What practical wisdom would you offer?",
            context,
        )

        # Pattern Analyst
        agent_outputs["patterns"] = self.crew.pattern_analyst.generate(
            f"Analyze these patterns from the week:\n"
            f"- Area scores: {context['area_averages']}\n"
            f"- Reflection days: {context['reflection_days']}\n"
            f"- Struggles mentioned: {context['struggles']}\n"
            f"What patterns do you notice?",
            context,
        )

        # Journey Guide
        agent_outputs["journey"] = self.crew.journey_guide.generate(
            f"User's journey status:\n"
            f"- Goal: {context['goal']}\n"
            f"- Day {context['current_day']} of {context['total_days']}\n"
            f"- Open threads: {context['open_threads']}\n"
            f"- Threads resolved this week: {context['resolved_threads']}\n"
            f"How is their progress?",
            context,
        )

        # Coordinator synthesizes
        return self.crew.coordinator.synthesize(agent_outputs, context)

    def _build_context(self, user) -> dict:
        from ..models import DailyReflection, OpenThread, UserJourney

        week_ago = date.today() - timedelta(days=7)

        reflections = DailyReflection.objects.filter(
            user=user, date__gte=week_ago
        ).order_by("date")

        journey = UserJourney.objects.filter(user=user, status="active").first()

        open_threads = OpenThread.objects.filter(
            user=user, status__in=["open", "following_up", "progressing"]
        )

        resolved_threads = OpenThread.objects.filter(
            user=user, status="resolved", resolved_at__gte=week_ago
        ).count()

        # Aggregate data
        scriptures = [
            r.scripture_reference for r in reflections if r.scripture_reference
        ]
        struggles = [r.get_struggle_note() for r in reflections if r.encrypted_struggle]
        gratitudes = [
            r.get_gratitude_note() for r in reflections if r.encrypted_gratitude
        ]
        reflection_days = [r.date.strftime("%A") for r in reflections]

        # Calculate area averages
        area_averages = {}
        for reflection in reflections:
            for area, score in reflection.area_scores.items():
                if area not in area_averages:
                    area_averages[area] = []
                area_averages[area].append(score)

        for area in area_averages:
            scores = area_averages[area]
            area_averages[area] = round(sum(scores) / len(scores), 1) if scores else 0

        return {
            "reflections": list(reflections),
            "reflection_count": reflections.count(),
            "scriptures": ", ".join(scriptures[:5]) if scriptures else "None",
            "struggles": "; ".join(struggles[:3]) if struggles else "None noted",
            "gratitudes": "; ".join(gratitudes[:3]) if gratitudes else "None noted",
            "reflection_days": (
                ", ".join(reflection_days) if reflection_days else "None"
            ),
            "area_averages": area_averages,
            "goal": journey.goal_statement if journey else "Not specified",
            "current_day": journey.current_day if journey else 0,
            "total_days": journey.duration_days if journey else 0,
            "open_threads": [t.get_summary() for t in open_threads[:5]],
            "resolved_threads": resolved_threads,
        }


class MonthlyRecapTask(BaseTask):
    """Generate monthly recap with trend analysis."""

    def execute(self, user, **kwargs) -> Optional[str]:
        """Generate comprehensive monthly recap."""
        context = self._build_context(user)

        if not context.get("reflections"):
            return "No reflections this month to review."

        # Run all agents with monthly focus
        agent_outputs = {}

        # Scripture Scholar - monthly themes
        agent_outputs["scripture"] = self.crew.scripture_scholar.generate(
            f"Over the past month, the user engaged with these themes: {context['themes']}\n"
            f"Their journey focus areas are: {context['focus_areas']}\n"
            f"What overarching biblical narrative connects their month?",
            context,
        )

        # Mentor - monthly wisdom
        agent_outputs["mentor"] = self.crew.mentor.generate(
            f"This month the user:\n"
            f"- Reflected {context['reflection_count']} times\n"
            f"- Consistency: {context['consistency_rate']}%\n"
            f"- Main struggles: {context['top_struggles']}\n"
            f"- Growth areas: {context['growth_areas']}\n"
            f"What wisdom would you offer for the month ahead?",
            context,
        )

        # Pattern Analyst - monthly trends
        agent_outputs["patterns"] = self.crew.pattern_analyst.generate(
            f"Monthly analysis:\n"
            f"- Week-over-week area trends: {context['weekly_trends']}\n"
            f"- Best days: {context['best_days']}\n"
            f"- Challenging days: {context['challenging_days']}\n"
            f"- Threads opened: {context['threads_opened']}, resolved: {context['threads_resolved']}\n"
            f"What significant patterns emerged this month?",
            context,
        )

        # Journey Guide - monthly progress
        agent_outputs["journey"] = self.crew.journey_guide.generate(
            f"Monthly journey progress:\n"
            f"- Started at day {context['start_day']}, now at day {context['current_day']}\n"
            f"- Goal: {context['goal']}\n"
            f"- Success definition: {context['success_definition']}\n"
            f"- Threads resolved: {context['threads_resolved']}\n"
            f"How would you summarize their month and set up the next?",
            context,
        )

        # Coordinator synthesizes with monthly framing
        return self.crew.coordinator.generate(
            f"Create a monthly recap synthesizing these perspectives:\n\n"
            f"SCRIPTURE: {agent_outputs.get('scripture', 'No input')}\n\n"
            f"MENTOR: {agent_outputs.get('mentor', 'No input')}\n\n"
            f"PATTERNS: {agent_outputs.get('patterns', 'No input')}\n\n"
            f"JOURNEY: {agent_outputs.get('journey', 'No input')}\n\n"
            f"Create a unified monthly summary (max 200 words) that:\n"
            f"1. Celebrates progress\n"
            f"2. Acknowledges challenges honestly\n"
            f"3. Sets up the month ahead with hope\n"
            f"4. Ends with a forward-looking question",
            context,
        )

    def _build_context(self, user) -> dict:
        from ..models import AlignmentTrend, DailyReflection, OpenThread, UserJourney

        month_ago = date.today() - timedelta(days=30)

        reflections = DailyReflection.objects.filter(
            user=user, date__gte=month_ago
        ).order_by("date")

        journey = UserJourney.objects.filter(user=user, status="active").first()

        threads_opened = OpenThread.objects.filter(
            user=user, created_at__date__gte=month_ago
        ).count()

        threads_resolved = OpenThread.objects.filter(
            user=user, status="resolved", resolved_at__date__gte=month_ago
        ).count()

        # Collect themes
        all_themes = []
        for r in reflections:
            all_themes.extend(r.scripture_themes)
        theme_counts = {}
        for theme in all_themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        top_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        # Collect struggles
        struggles = [r.get_struggle_note() for r in reflections if r.encrypted_struggle]

        # Calculate consistency
        days_in_period = 30
        consistency_rate = round((reflections.count() / days_in_period) * 100, 1)

        # Weekly trends from AlignmentTrend
        weekly_trends = AlignmentTrend.objects.filter(
            user=user, period_type="week", period_start__gte=month_ago
        ).order_by("period_start")

        # Identify best/challenging days
        day_scores = {}
        for r in reflections:
            day_name = r.date.strftime("%A")
            if day_name not in day_scores:
                day_scores[day_name] = []
            avg_score = (
                sum(r.area_scores.values()) / len(r.area_scores) if r.area_scores else 0
            )
            day_scores[day_name].append(avg_score)

        day_averages = {
            day: sum(scores) / len(scores)
            for day, scores in day_scores.items()
            if scores
        }
        sorted_days = sorted(day_averages.items(), key=lambda x: x[1], reverse=True)

        return {
            "reflections": list(reflections),
            "reflection_count": reflections.count(),
            "consistency_rate": consistency_rate,
            "themes": (
                ", ".join([t[0] for t in top_themes]) if top_themes else "Various"
            ),
            "top_struggles": "; ".join(struggles[:3]) if struggles else "None noted",
            "growth_areas": (
                ", ".join(journey.focus_areas) if journey else "Not specified"
            ),
            "focus_areas": (
                ", ".join(journey.focus_areas) if journey else "Not specified"
            ),
            "weekly_trends": [
                {"week": t.period_start, "averages": t.area_averages}
                for t in weekly_trends
            ],
            "best_days": sorted_days[0][0] if sorted_days else "Unknown",
            "challenging_days": (
                sorted_days[-1][0] if len(sorted_days) > 1 else "Unknown"
            ),
            "threads_opened": threads_opened,
            "threads_resolved": threads_resolved,
            "goal": journey.goal_statement if journey else "Not specified",
            "success_definition": (
                journey.success_definition if journey else "Not specified"
            ),
            "start_day": max(0, (journey.current_day - 30) if journey else 0),
            "current_day": journey.current_day if journey else 0,
        }

"""
DevotionalCrew - Orchestrates AI agents for personalized guidance.
"""

import logging
from typing import Optional

from shared.llm import get_llm

from .agents import (
    Coordinator,
    JourneyGuide,
    MentorAgent,
    PatternAnalyst,
    ScriptureScholar,
)
from .tasks import (
    DailyInsightTask,
    MonthlyRecapTask,
    WeeklyReviewTask,
)

logger = logging.getLogger(__name__)


class DevotionalCrew:
    """
    AI Crew for personalized devotional guidance.

    All agents share one LLM client, resolved from the person's own provider
    settings (see shared.llm). Methods raise LLMError when the model cannot
    be used - callers decide how to tell the person.
    """

    def __init__(self, llm=None, user=None):
        self.user = user
        self._llm = llm
        self._create_agents()
        self._create_tasks()

    @property
    def llm(self):
        if self._llm is None:
            self._llm = get_llm(self.user)
        return self._llm

    def _create_agents(self):
        """Initialize all crew agents (they resolve the LLM lazily)."""
        kwargs = {"llm": self._llm, "user": self.user}
        self.scripture_scholar = ScriptureScholar(**kwargs)
        self.mentor = MentorAgent(**kwargs)
        self.pattern_analyst = PatternAnalyst(**kwargs)
        self.journey_guide = JourneyGuide(**kwargs)
        self.coordinator = Coordinator(**kwargs)

    def _create_tasks(self):
        """Initialize crew tasks."""
        self.daily_insight_task = DailyInsightTask(self)
        self.weekly_review_task = WeeklyReviewTask(self)
        self.monthly_recap_task = MonthlyRecapTask(self)

    def generate_daily_insight(self, user, reflection) -> Optional[str]:
        """Daily insight for a reflection (mentor + coordinator)."""
        return self.daily_insight_task.execute(user, reflection=reflection)

    def generate_weekly_review(self, user) -> Optional[str]:
        """Weekly review with full crew analysis."""
        return self.weekly_review_task.execute(user)

    def generate_monthly_recap(self, user) -> Optional[str]:
        """Monthly recap with trend analysis."""
        return self.monthly_recap_task.execute(user)

    def ask_specific_agent(
        self, agent_name: str, prompt: str, context: dict = None
    ) -> Optional[str]:
        """
        Ask a specific agent a question.

        agent_name: one of 'scripture', 'mentor', 'patterns', 'journey', 'coordinator'
        Returns None for an unknown agent name.
        """
        agents = {
            "scripture": self.scripture_scholar,
            "mentor": self.mentor,
            "patterns": self.pattern_analyst,
            "journey": self.journey_guide,
            "coordinator": self.coordinator,
        }

        agent = agents.get(agent_name)
        if not agent:
            logger.warning("Unknown agent: %s", agent_name)
            return None
        return agent.generate(prompt, context)

    def health_check(self) -> dict:
        """Whether this person's AI provider can be used right now. Never raises."""
        from shared.llm import ai_status

        info = ai_status(self.user)
        return {
            "status": "healthy" if info["reachable"] else "unhealthy",
            "provider": info["backend"],
            "model": info["model"],
            "local": info["local"],
            "model_available": info["reachable"],
            "code": info["code"],
            "error": info["message"],
            "suggestion": info["suggestion"],
        }


def get_crew(user=None) -> DevotionalCrew:
    """A DevotionalCrew that uses this person's AI provider settings."""
    return DevotionalCrew(user=user)

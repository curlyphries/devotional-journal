"""
Services for the Life Reflection system: study guides and thread follow-ups.

All model calls go through shared.llm, which applies the person's provider
choice and consent, and raises a coded LLMError when the model cannot be used.
"""

import logging
from typing import Optional

from shared.llm import LLMBadResponse, get_llm

logger = logging.getLogger(__name__)


class StudyGuideService:
    """
    Generates personalized deep-dive study guides from passages or journal entries.
    """

    STUDY_GUIDE_PROMPT = """You are a biblical study coach and reflective spiritual mentor.

Create a personalized deep-dive study guide based on this user context.

SOURCE TYPE: {source_type}
SOURCE DATA:
{source_context}

USER CONTEXT:
{user_context}

Return ONLY valid JSON with this exact shape:
{{
  "title": "Short study guide title",
  "insight_summary": "2-4 sentence summary of key spiritual insight",
  "analytical_insights": ["Insight 1", "Insight 2", "Insight 3"],
  "heart_check_questions": ["Question 1", "Question 2", "Question 3"],
  "study_plan": [
    {{"day": 1, "focus": "Focus for day 1", "scripture": "Book X:Y-Z", "practice": "Concrete practice", "journal_prompt": "Journal question"}},
    {{"day": 2, "focus": "Focus for day 2", "scripture": "Book X:Y-Z", "practice": "Concrete practice", "journal_prompt": "Journal question"}},
    {{"day": 3, "focus": "Focus for day 3", "scripture": "Book X:Y-Z", "practice": "Concrete practice", "journal_prompt": "Journal question"}}
  ],
  "prayer_focus": "A concise prayer direction",
  "next_step": "One specific next step for today"
}}

Requirements:
- Keep language pastoral but practical and grounded.
- Be specific to the provided source and user context.
- Avoid generic cliches.
- Keep each list item concise and actionable.
- "scripture" must be a reference only (e.g. "Psalm 46:1-3") to a passage you are
  certain exists. Never write out verse text.
- Never claim personal experiences.
"""

    def __init__(self, llm=None, user=None):
        self._llm = llm
        self.user = user

    @property
    def llm(self):
        if self._llm is None:
            self._llm = get_llm(self.user)
        return self._llm

    def generate_study_guide(
        self,
        source_type: str,
        source_context: dict,
        user_context: Optional[dict] = None,
    ) -> dict:
        """
        Generate a personalized deep-dive study guide.

        Raises LLMError if the model cannot be used or returns something
        unusable - a canned guide is never returned in its place.
        """
        from apps.bible.books import parse_reference

        user_context = user_context or {}

        prompt = self.STUDY_GUIDE_PROMPT.format(
            source_type=source_type,
            source_context=self._format_context(source_context),
            user_context=self._format_context(user_context),
        )

        source_reference = (
            source_context.get("scripture_reference")
            or source_context.get("entry_date")
            or source_context.get("title")
            or "Personal Reflection"
        )

        payload = self.llm.complete_json(prompt, max_tokens=1200, temperature=0.5)
        parsed = self._parse_guide(payload)
        if not parsed or not parsed["study_plan"]:
            raise LLMBadResponse("The model did not return a usable study guide.")

        for day in parsed["study_plan"]:
            # Keep only references that name a real book and chapter.
            reference = parse_reference(day["scripture"])
            day["scripture"] = reference.label if reference else ""

        parsed["source_type"] = source_type
        parsed["source_reference"] = source_reference
        return parsed

    def _format_context(self, context: dict) -> str:
        """Format dict context into readable prompt text."""
        lines = []
        for key, value in context.items():
            if value is None:
                continue
            if isinstance(value, list):
                if not value:
                    continue
                value_text = ", ".join([str(v) for v in value])
            else:
                value_text = str(value)

            value_text = value_text.strip()
            if not value_text:
                continue

            if len(value_text) > 2500:
                value_text = value_text[:2500] + "..."

            lines.append(f"- {key}: {value_text}")

        return "\n".join(lines) if lines else "- none provided"

    def _parse_guide(self, payload) -> Optional[dict]:
        """Normalise the model's JSON guide into the shape the app stores."""
        if not isinstance(payload, dict):
            return None

        insights = payload.get("analytical_insights")
        if not isinstance(insights, list):
            insights = []

        questions = payload.get("heart_check_questions")
        if not isinstance(questions, list):
            questions = []

        plan = payload.get("study_plan")
        if not isinstance(plan, list):
            plan = []

        normalized_plan = []
        for index, day in enumerate(plan[:7], start=1):
            if not isinstance(day, dict):
                continue

            normalized_plan.append(
                {
                    "day": index,
                    "focus": str(day.get("focus", "")).strip(),
                    "scripture": str(day.get("scripture", "")).strip(),
                    "practice": str(day.get("practice", "")).strip(),
                    "journal_prompt": str(day.get("journal_prompt", "")).strip(),
                }
            )

        return {
            "title": str(payload.get("title", "Personalized Deep Dive")).strip()
            or "Personalized Deep Dive",
            "insight_summary": str(payload.get("insight_summary", "")).strip(),
            "analytical_insights": [
                str(i).strip() for i in insights[:6] if str(i).strip()
            ],
            "heart_check_questions": [
                str(q).strip() for q in questions[:6] if str(q).strip()
            ],
            "study_plan": normalized_plan,
            "prayer_focus": str(payload.get("prayer_focus", "")).strip(),
            "next_step": str(payload.get("next_step", "")).strip(),
        }


class ThreadDetectionService:
    """
    Wording for thread follow-up questions.

    Detecting threads now happens as part of journal feedback
    (apps.journal.feedback), in the same model call that reads the entry.
    """

    def generate_followup_prompt(self, thread_type: str, summary: str) -> str:
        """Generate a follow-up prompt for a thread."""
        prompts = {
            "struggle": f"How's {summary} going?",
            "commitment": f"Did you follow through on {summary}?",
            "relationship": f"Any progress with {summary}?",
            "decision": f"Made a decision on {summary}?",
            "confession": f"How are you feeling about {summary}?",
        }
        return prompts.get(thread_type, f"How's {summary} going?")


class ThreadFollowupService:
    """
    Manages thread follow-ups and generates prompts for users.
    """

    def get_threads_needing_followup(self, user, max_prompts: int = 2) -> list:
        """
        Get threads that need follow-up for a user.

        Args:
            user: The user object
            max_prompts: Maximum number of prompts to return

        Returns:
            List of OpenThread objects needing follow-up
        """
        from .models import OpenThread

        threads = OpenThread.objects.filter(
            user=user, status__in=["open", "following_up", "progressing"]
        ).order_by(
            "last_mentioned_at"
        )  # Oldest first

        needing_followup = []
        for thread in threads:
            if thread.needs_followup:
                needing_followup.append(thread)
                if len(needing_followup) >= max_prompts:
                    break

        return needing_followup

    def create_thread_prompts(self, threads: list, reflection) -> list[dict]:
        """
        Create prompt data for threads.

        Returns:
            List of prompt dicts ready for API response
        """
        detection_service = ThreadDetectionService()
        prompts = []

        for thread in threads:
            prompt_text = detection_service.generate_followup_prompt(
                thread.thread_type, thread.get_summary()
            )

            # Determine response options based on thread type
            if thread.thread_type in ["struggle", "confession"]:
                options = ["better", "same", "worse", "skipped"]
            elif thread.thread_type == "commitment":
                options = ["yes", "no", "skipped"]
            elif thread.thread_type == "decision":
                options = ["yes", "same", "skipped"]
            else:
                options = ["better", "same", "worse", "skipped"]

            prompts.append(
                {
                    "thread_id": str(thread.id),
                    "thread_type": thread.thread_type,
                    "summary": thread.get_summary(),
                    "days_ago": thread.days_since_mentioned,
                    "prompt_text": prompt_text,
                    "response_options": options,
                    "can_expand": True,
                    "can_resolve": True,
                }
            )

        return prompts

    def process_thread_response(
        self,
        thread_id: str,
        response: str,
        expanded_text: str = "",
        reflection=None,
        user=None,
    ) -> dict:
        """
        Process a user's response to a thread prompt.

        Returns:
            Dict with status and any follow-up actions
        """
        from .models import OpenThread, ThreadPrompt

        lookup = {"id": thread_id}
        if user is not None:
            lookup["user"] = user
        try:
            thread = OpenThread.objects.get(**lookup)
        except OpenThread.DoesNotExist:
            return {"error": "Thread not found"}

        # Create ThreadPrompt record if reflection provided
        if reflection:
            prompt = ThreadPrompt.objects.create(
                thread=thread,
                reflection=reflection,
                prompt_text=ThreadDetectionService().generate_followup_prompt(
                    thread.thread_type, thread.get_summary()
                ),
            )
            prompt.record_response(response, expanded_text)
        else:
            # Update thread directly
            if response == "better":
                thread.mark_progressing()
            elif response == "resolved":
                thread.mark_resolved(expanded_text)
            elif response == "skipped":
                thread.record_skip()
            else:
                thread.mark_mentioned()

        return {
            "status": "success",
            "thread_status": thread.status,
            "message": self._get_response_message(response, thread),
        }

    def _get_response_message(self, response: str, thread) -> str:
        """Get a brief message based on response."""
        messages = {
            "better": "Great to hear you're making progress!",
            "same": "Hang in there. Growth takes time.",
            "worse": "Thanks for being honest. We'll check in again.",
            "yes": "Well done on following through!",
            "no": "No worries. Tomorrow is a new day.",
            "skipped": "Got it. We'll ask again later.",
            "resolved": "Congratulations on closing this chapter!",
        }
        return messages.get(response, "Response recorded.")


def get_thread_detection_service() -> ThreadDetectionService:
    """Factory function for thread wording service."""
    return ThreadDetectionService()


def get_thread_followup_service() -> ThreadFollowupService:
    """Factory function for thread follow-up service."""
    return ThreadFollowupService()


def get_study_guide_service(user=None) -> StudyGuideService:
    """Deep-dive study guide generation using this person's AI provider."""
    return StudyGuideService(user=user)

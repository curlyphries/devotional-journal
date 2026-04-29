"""
Services for the Life Reflection system.
Includes AI theme extraction and insight generation.
"""

import logging
from typing import Optional

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


class ThemeExtractionService:
    """
    Extracts themes from scripture passages using Ollama.
    """

    THEME_EXTRACTION_PROMPT = """You are analyzing a Bible passage to extract life-applicable themes.

Passage: {reference}
{text}

Extract 3-5 single-word or short-phrase themes that relate to practical daily living.
Focus on themes relevant to men's lives: integrity, relationships, work, self-control,
faith practice, service, and personal growth.

Return ONLY a JSON array of themes, e.g.: ["trust", "patience", "provision"]
Do not include any other text or explanation."""

    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or getattr(
            settings, "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        self.model = model or getattr(settings, "OLLAMA_MODEL", "llama3.1:8b")

    def extract_themes(self, reference: str, text: str) -> list[str]:
        """
        Extract themes from a scripture passage.

        Args:
            reference: Scripture reference (e.g., "Proverbs 3:5-6")
            text: The actual scripture text

        Returns:
            List of theme strings
        """
        prompt = self.THEME_EXTRACTION_PROMPT.format(reference=reference, text=text)

        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 100,
                    },
                },
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()

            raw_response = result.get("response", "").strip()
            themes = self._parse_themes(raw_response)

            logger.info(f"Extracted themes for {reference}: {themes}")
            return themes

        except httpx.TimeoutException:
            logger.warning(f"Timeout extracting themes for {reference}")
            return self._fallback_themes(reference, text)
        except Exception as e:
            logger.error(f"Error extracting themes: {e}")
            return self._fallback_themes(reference, text)

    def _parse_themes(self, raw_response: str) -> list[str]:
        """Parse the JSON array from the LLM response."""
        import json

        raw_response = raw_response.strip()
        if raw_response.startswith("[") and raw_response.endswith("]"):
            try:
                themes = json.loads(raw_response)
                if isinstance(themes, list):
                    return [str(t).lower().strip() for t in themes[:5]]
            except json.JSONDecodeError:
                pass

        start = raw_response.find("[")
        end = raw_response.rfind("]")
        if start != -1 and end != -1:
            try:
                themes = json.loads(raw_response[start : end + 1])
                if isinstance(themes, list):
                    return [str(t).lower().strip() for t in themes[:5]]
            except json.JSONDecodeError:
                pass

        return []

    def _fallback_themes(self, reference: str, text: str) -> list[str]:
        """
        Simple keyword-based fallback when LLM is unavailable.
        """
        from .models import LifeArea

        text_lower = text.lower()
        themes = []

        for area in LifeArea.objects.all():
            for tag in area.scripture_tags:
                if tag.lower() in text_lower and tag not in themes:
                    themes.append(tag)
                    if len(themes) >= 3:
                        break
            if len(themes) >= 3:
                break

        return themes if themes else ["reflection", "faith", "growth"]


class InsightGenerationService:
    """
    Generates AI insights for daily reflections.
    """

    DAILY_INSIGHT_PROMPT = """You are a wise, non-judgmental spiritual mentor helping a man reflect on his day.

TODAY'S SCRIPTURE: {reference}
Key themes: {themes}

HIS REFLECTION:
{reflection}

SELF-ASSESSMENT:
{area_scores}

GRATITUDE: {gratitude}
STRUGGLE: {struggle}

Provide a brief (2-3 sentences) encouraging insight that:
1. Acknowledges his honest self-assessment
2. Connects his experience to the scripture
3. Offers one practical thought for tomorrow

Tone: Like a trusted older brother or mentor - direct but kind, not preachy.
Do NOT quote scripture back at him. Speak naturally."""

    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or getattr(
            settings, "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        self.model = model or getattr(settings, "OLLAMA_MODEL", "llama3.1:8b")

    def generate_insight(
        self,
        reference: str,
        themes: list[str],
        reflection: str,
        area_scores: dict,
        gratitude: str = "",
        struggle: str = "",
    ) -> Optional[str]:
        """
        Generate an AI insight for a daily reflection.
        """
        scores_formatted = (
            "\n".join([f"- {area}: {score}/5" for area, score in area_scores.items()])
            if area_scores
            else "No scores provided"
        )

        prompt = self.DAILY_INSIGHT_PROMPT.format(
            reference=reference,
            themes=", ".join(themes) if themes else "general reflection",
            reflection=reflection or "No reflection provided",
            area_scores=scores_formatted,
            gratitude=gratitude or "Not specified",
            struggle=struggle or "Not specified",
        )

        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 200,
                    },
                },
                timeout=60.0,
            )
            response.raise_for_status()
            result = response.json()

            insight = result.get("response", "").strip()
            logger.info(f"Generated insight for {reference}")
            return insight

        except Exception as e:
            logger.error(f"Error generating insight: {e}")
            return None

    def health_check(self) -> bool:
        """Check if Ollama is accessible."""
        try:
            response = httpx.get(f"{self.base_url}/api/tags", timeout=5.0)
            response.raise_for_status()
            data = response.json()
            models = [m["name"] for m in data.get("models", [])]
            return any(self.model in m for m in models)
        except Exception as e:
            logger.warning(f"Ollama health check failed: {e}")
            return False


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
"""

    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or getattr(
            settings, "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        self.model = model or getattr(settings, "OLLAMA_MODEL", "llama3.1:8b")

    def generate_study_guide(
        self,
        source_type: str,
        source_context: dict,
        user_context: Optional[dict] = None,
    ) -> dict:
        """
        Generate a personalized deep-dive study guide.
        """
        user_context = user_context or {}

        source_context_text = self._format_context(source_context)
        user_context_text = self._format_context(user_context)

        prompt = self.STUDY_GUIDE_PROMPT.format(
            source_type=source_type,
            source_context=source_context_text,
            user_context=user_context_text,
        )

        source_reference = (
            source_context.get("scripture_reference")
            or source_context.get("entry_date")
            or source_context.get("title")
            or "Personal Reflection"
        )

        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.5,
                        "num_predict": 900,
                    },
                },
                timeout=90.0,
            )
            response.raise_for_status()
            result = response.json()

            raw_response = result.get("response", "").strip()
            parsed = self._parse_guide(raw_response)
            if parsed:
                parsed["source_type"] = source_type
                parsed["source_reference"] = source_reference
                return parsed

        except Exception as e:
            logger.error(f"Error generating study guide: {e}")

        return self._fallback_guide(
            source_type, source_reference, source_context, user_context
        )

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

    def _parse_guide(self, raw_response: str) -> Optional[dict]:
        """Parse JSON guide payload from model output."""
        import json

        start = raw_response.find("{")
        end = raw_response.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None

        try:
            payload = json.loads(raw_response[start : end + 1])
        except json.JSONDecodeError:
            return None

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
                    "day": int(day.get("day", index)),
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

    def _fallback_guide(
        self,
        source_type: str,
        source_reference: str,
        source_context: dict,
        user_context: dict,
    ) -> dict:
        """Fallback guide when model generation fails."""
        focus = user_context.get("focus_intention") or "walking closely with God"
        connection = (
            source_context.get("connection_to_focus")
            or source_context.get("theme")
            or "your current season"
        )

        return {
            "source_type": source_type,
            "source_reference": source_reference,
            "title": f"Deep Dive: {source_reference}",
            "insight_summary": (
                f"This passage and reflection point to a growth opportunity around {connection}. "
                f"Use this guide to move from reflection into intentional practice in your focus: {focus}."
            ),
            "analytical_insights": [
                "Notice what this reveals about God's character and invitation.",
                "Identify recurring emotional patterns and spiritual needs in your response.",
                "Translate conviction into one measurable act of obedience this week.",
            ],
            "heart_check_questions": [
                "What part of this truth am I resisting, and why?",
                "Where do I need repentance, trust, or surrender today?",
                "How can I practice this in one concrete relationship this week?",
            ],
            "study_plan": [
                {
                    "day": 1,
                    "focus": "Observe and understand the text",
                    "scripture": source_reference,
                    "practice": "Read slowly twice and write 3 key observations.",
                    "journal_prompt": "What is the core message of this passage for my life right now?",
                },
                {
                    "day": 2,
                    "focus": "Connect truth to your current focus",
                    "scripture": source_reference,
                    "practice": "Pray for clarity and identify one area to align.",
                    "journal_prompt": "How does this speak directly to my current intention?",
                },
                {
                    "day": 3,
                    "focus": "Practice and accountability",
                    "scripture": source_reference,
                    "practice": "Choose one practical action and complete it today.",
                    "journal_prompt": "What changed in my heart and behavior after practicing this?",
                },
            ],
            "prayer_focus": "Ask God for a tender heart, practical obedience, and consistent follow-through.",
            "next_step": "Pick one action from Day 3 and schedule it in your calendar now.",
        }


class ThreadDetectionService:
    """
    Detects open threads (struggles, commitments, etc.) from user reflections.
    """

    THREAD_DETECTION_PROMPT = """Analyze this user reflection for significant topics that should be tracked:

USER'S REFLECTION:
{reflection_text}

STRUGGLE NOTED: {struggle_note}

Look for:
1. STRUGGLES: Things they're battling ("I've been struggling with...", "I can't seem to...")
2. COMMITMENTS: Things they're committing to ("I'm going to...", "Starting tomorrow...")
3. RELATIONSHIP ISSUES: People/relationships with tension ("My wife and I...", "My son...")
4. DECISIONS: Choices they're wrestling with ("I don't know if I should...")
5. CONFESSIONS: Vulnerable shares ("I haven't told anyone...", "The truth is...")

For each significant item found, return a JSON object:
{{
    "threads": [
        {{
            "type": "struggle|commitment|relationship|decision|confession",
            "summary": "Brief 10-word max summary",
            "life_area": "integrity|relationships|work|self_control|faith|service|growth",
            "quote": "Exact words from their reflection (max 50 words)"
        }}
    ]
}}

If nothing significant, return: {{"threads": []}}
Be selective - not every mention is a thread. Only track things that warrant follow-up."""

    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or getattr(
            settings, "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        self.model = model or getattr(settings, "OLLAMA_MODEL", "llama3.1:8b")

    def detect_threads(
        self, reflection_text: str, struggle_note: str = ""
    ) -> list[dict]:
        """
        Detect threads from a reflection.

        Returns:
            List of thread dicts with type, summary, life_area, quote
        """
        if not reflection_text and not struggle_note:
            return []

        prompt = self.THREAD_DETECTION_PROMPT.format(
            reflection_text=reflection_text or "No reflection provided",
            struggle_note=struggle_note or "Not specified",
        )

        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 500,
                    },
                },
                timeout=45.0,
            )
            response.raise_for_status()
            result = response.json()

            raw_response = result.get("response", "").strip()
            threads = self._parse_threads(raw_response)

            logger.info(f"Detected {len(threads)} threads from reflection")
            return threads

        except httpx.TimeoutException:
            logger.warning("Timeout detecting threads")
            return []
        except Exception as e:
            logger.error(f"Error detecting threads: {e}")
            return []

    def _parse_threads(self, raw_response: str) -> list[dict]:
        """Parse the JSON response from the LLM."""
        import json

        # Try to find JSON in response
        start = raw_response.find("{")
        end = raw_response.rfind("}")

        if start == -1 or end == -1:
            return []

        try:
            data = json.loads(raw_response[start : end + 1])
            threads = data.get("threads", [])

            # Validate each thread
            valid_threads = []
            valid_types = [
                "struggle",
                "commitment",
                "relationship",
                "decision",
                "confession",
            ]
            valid_areas = [
                "integrity",
                "relationships",
                "work",
                "self_control",
                "faith",
                "service",
                "growth",
            ]

            for thread in threads:
                if not isinstance(thread, dict):
                    continue
                if thread.get("type") not in valid_types:
                    continue
                if not thread.get("summary"):
                    continue

                # Normalize life_area
                life_area = thread.get("life_area", "")
                if life_area not in valid_areas:
                    life_area = ""

                valid_threads.append(
                    {
                        "type": thread["type"],
                        "summary": thread["summary"][:100],  # Cap summary length
                        "life_area": life_area,
                        "quote": thread.get("quote", "")[:200],  # Cap quote length
                    }
                )

            return valid_threads

        except json.JSONDecodeError:
            logger.warning("Failed to parse thread detection response as JSON")
            return []

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
        self, thread_id: str, response: str, expanded_text: str = "", reflection=None
    ) -> dict:
        """
        Process a user's response to a thread prompt.

        Returns:
            Dict with status and any follow-up actions
        """
        from .models import OpenThread, ThreadPrompt

        try:
            thread = OpenThread.objects.get(id=thread_id)
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


def get_theme_service() -> ThemeExtractionService:
    """Factory function for theme extraction service."""
    return ThemeExtractionService()


def get_insight_service() -> InsightGenerationService:
    """Factory function for insight generation service."""
    return InsightGenerationService()


def get_thread_detection_service() -> ThreadDetectionService:
    """Factory function for thread detection service."""
    return ThreadDetectionService()


def get_thread_followup_service() -> ThreadFollowupService:
    """Factory function for thread follow-up service."""
    return ThreadFollowupService()


def get_study_guide_service() -> StudyGuideService:
    """Factory function for deep-dive study guide generation."""
    return StudyGuideService()

"""
AI Agents for the Devotional Guidance Crew.
Each agent has a specific role and personality.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional

from shared.llm import LLMError, get_llm

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all crew agents.

    Agents never talk to a model directly: they go through shared.llm, which
    applies the person's provider choice and consent. Failures raise LLMError
    (with a code and a suggestion) instead of returning nothing.
    """

    role: str = "Agent"
    goal: str = ""
    backstory: str = ""
    max_tokens: int = 500

    def __init__(self, llm=None, user=None):
        self._llm = llm
        self.user = user

    @property
    def llm(self):
        if self._llm is None:
            self._llm = get_llm(self.user)
        return self._llm

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    def generate(self, prompt: str, context: dict = None) -> str:
        """Generate a response from this agent. Raises LLMError on failure."""
        system_prompt = self.get_system_prompt()

        if context:
            system_prompt += f"\n\nCONTEXT:\n{self._format_context(context)}"

        return self.llm.complete(
            prompt, system_prompt, max_tokens=self.max_tokens, temperature=0.7
        )

    def generate_json(self, prompt: str, max_tokens: int = 800):
        return self.llm.complete_json(
            prompt, self.get_system_prompt(), max_tokens=max_tokens
        )

    def _format_context(self, context: dict) -> str:
        """Format context dict for inclusion in prompt."""
        lines = []
        for key, value in context.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            elif isinstance(value, dict):
                lines.append(f"{key}:")
                for k, v in value.items():
                    lines.append(f"  {k}: {v}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)


class ScriptureScholar(BaseAgent):
    """Biblical context and relevant passages."""

    role = "Scripture Scholar"
    goal = "Provide biblical context and relevant passages"
    backstory = """You are a biblical scholar who makes scripture accessible.
    You understand Hebrew and Greek context but explain things simply.
    You never preach - you illuminate. You connect ancient wisdom to modern struggles."""

    def get_system_prompt(self) -> str:
        return f"""You are the {self.role}.

ROLE: {self.goal}

PERSONALITY: {self.backstory}

GUIDELINES:
- Give scripture as references only (e.g. "Romans 8:28"); never write out verse text - the app looks up the exact words
- Explain cultural/historical context briefly
- Connect scripture to the user's specific situation
- Never be preachy or condescending
- Keep responses under 100 words
- Use plain language, not religious jargon"""


class MentorAgent(BaseAgent):
    """Practical life wisdom."""

    role = "Wise Mentor"
    goal = "Offer practical, grounded encouragement"
    backstory = """You speak the way a seasoned, trustworthy mentor would:
    direct but kind, never shaming. You are an AI and never claim experiences
    of your own - no invented life story, no "when I went through this"."""

    def get_system_prompt(self) -> str:
        return f"""You are the {self.role}.

ROLE: {self.goal}

PERSONALITY: {self.backstory}

GUIDELINES:
- Be direct but compassionate
- Offer practical, actionable advice
- Never lecture or moralize
- Acknowledge the difficulty of change
- Point toward the character of Jesus (humility, honesty, compassion, service)
- Never invent personal experiences or speak as if you have lived a human life
- Keep responses under 100 words"""


class PatternAnalyst(BaseAgent):
    """Detects trends, triggers, and patterns."""

    role = "Pattern Analyst"
    goal = "Identify trends, triggers, and patterns"
    backstory = """You analyze behavioral patterns without judgment. You notice
    what the user might not see - timing, triggers, correlations. You present
    observations as data, not accusations."""

    def get_system_prompt(self) -> str:
        return f"""You are the {self.role}.

ROLE: {self.goal}

PERSONALITY: {self.backstory}

GUIDELINES:
- Present observations objectively
- Note timing patterns (days of week, times of day)
- Identify potential triggers
- Highlight correlations without implying causation
- Never judge or shame
- Keep responses under 100 words
- Use phrases like "I notice..." or "The data shows..."
- Suggest hypotheses, not conclusions"""


class JourneyGuide(BaseAgent):
    """Tracks goal progress and manages accountability."""

    role = "Journey Guide"
    goal = "Track goal progress, manage open threads, suggest next steps"
    backstory = """You are an accountability partner who remembers the user's
    goal and gently keeps them oriented toward it. You track open threads
    and ensure nothing falls through the cracks. You celebrate wins."""

    def get_system_prompt(self) -> str:
        return f"""You are the {self.role}.

ROLE: {self.goal}

PERSONALITY: {self.backstory}

GUIDELINES:
- Reference the user's stated goals
- Track progress with specific numbers when available
- Acknowledge both successes and struggles
- Remind about open threads gently
- Suggest concrete next steps
- Keep responses under 100 words
- Celebrate progress, no matter how small"""


class Coordinator(BaseAgent):
    """Synthesizes insights into coherent guidance."""

    role = "Guidance Coordinator"
    goal = "Synthesize insights into coherent, actionable guidance"
    backstory = """You take multiple perspectives and weave them into a single,
    unified message. You're concise - never more than 150 words. You end with
    a question or gentle challenge, not a lecture."""

    def get_system_prompt(self) -> str:
        return f"""You are the {self.role}.

ROLE: {self.goal}

PERSONALITY: {self.backstory}

GUIDELINES:
- Synthesize multiple agent perspectives into one voice
- Be concise - MAXIMUM 150 words
- Start with the most relevant insight
- Include one practical suggestion
- End with a question or gentle challenge
- Never lecture or preach
- Speak as a trusted friend, not an authority
- Use "you" language, not "one should"
- Acknowledge difficulty while encouraging progress"""

    def synthesize(self, agent_outputs: dict, user_context: dict) -> Optional[str]:
        """Synthesize multiple agent outputs into unified guidance."""
        prompt = f"""Synthesize these perspectives into unified guidance for the user:

SCRIPTURE SCHOLAR:
{agent_outputs.get('scripture', 'No input')}

WISE MENTOR:
{agent_outputs.get('mentor', 'No input')}

PATTERN ANALYST:
{agent_outputs.get('patterns', 'No input')}

JOURNEY GUIDE:
{agent_outputs.get('journey', 'No input')}

USER'S CURRENT SITUATION:
- Goal: {user_context.get('goal', 'Not specified')}
- Days in journey: {user_context.get('days_in_journey', 'Unknown')}
- Recent struggles: {user_context.get('struggles', 'None noted')}
- Open threads: {user_context.get('open_threads', 'None')}

Create a unified, coherent message that:
1. Addresses their current situation
2. Incorporates the most relevant insights
3. Ends with a question or gentle challenge

MAXIMUM 150 WORDS. Do not exceed this limit."""

        return self.generate(prompt, user_context)


class DevotionalCurator(BaseAgent):
    """Curates scripture passages based on user's focus intention."""

    role = "Devotional Curator"
    goal = "Select relevant scripture passages with context and reflection prompts"
    backstory = """You are a thoughtful curator of scripture who understands that
    different seasons of life call for different passages. You select passages
    that speak directly to someone's current focus - whether they are seeking
    patience, healing, courage, or wisdom - and explain plainly why."""

    MAX_PER_CALL = 7

    def get_system_prompt(self) -> str:
        return f"""You are the {self.role}.

ROLE: {self.goal}

PERSONALITY: {self.backstory}

GUIDELINES:
- Select passages that directly relate to the user's stated focus
- Give references only (e.g. "James 1:2-4"). NEVER write out the verse text:
  the app retrieves the exact words from a Bible source itself
- Only cite passages you are certain exist, 1-8 verses each
- Provide brief historical/cultural context (1-2 sentences)
- Explain how the passage connects to their specific intention
- Generate 2-3 reflection questions that are personal and probing
- Suggest 1-2 practical applications for their daily life
- Never be preachy - let the scripture speak for itself
- Never claim personal experiences"""

    def curate_passages(
        self,
        intention: str,
        period_type: str,
        themes: list,
        num_passages: int = 7,
        avoid: Optional[list] = None,
    ) -> list:
        """
        Suggest passages for a focus intention and return them with their
        text fetched from the Bible source.

        Every returned item has a real `scripture_text` and the `translation`
        it actually came from. Suggestions whose reference does not exist are
        dropped. Raises LLMError if the model cannot be used.
        """
        from apps.bible.lookup import fetch_reference

        wanted = max(1, min(int(num_passages or 1), self.MAX_PER_CALL))
        avoid_line = (
            f"\nDo not repeat these (already given): {', '.join(avoid[:20])}"
            if avoid
            else ""
        )

        prompt = f"""The user has set a {period_type} focus intention:

"{intention}"

Identified themes: {', '.join(themes) if themes else 'general spiritual growth'}{avoid_line}

Suggest {wanted + 2} scripture passages that will guide them through this focus period.
Each passage should build on the previous, creating a journey of understanding.

Return ONLY a JSON object of this shape:
{{
  "passages": [
    {{
      "scripture_reference": "Book Chapter:Verse-Verse",
      "context_note": "1-2 sentences of historical/cultural context",
      "connection_to_focus": "How this specifically relates to their intention",
      "reflection_prompts": ["Question 1?", "Question 2?"],
      "application_suggestions": ["Practical action 1", "Practical action 2"]
    }}
  ]
}}"""

        data = self.generate_json(prompt, max_tokens=450 * (wanted + 2))
        items = data.get("passages") if isinstance(data, dict) else data
        if not isinstance(items, list):
            return []

        results = []
        seen = set(avoid or [])
        for item in items:
            if not isinstance(item, dict):
                continue
            passage = fetch_reference(str(item.get("scripture_reference", "")))
            if passage is None or passage.reference in seen:
                if passage is None:
                    logger.info(
                        "Dropped a suggested passage that is not in the Bible source"
                    )
                continue
            seen.add(passage.reference)

            def _strings(value, limit):
                if not isinstance(value, list):
                    return []
                return [str(v).strip()[:400] for v in value if str(v).strip()][:limit]

            results.append(
                {
                    "scripture_reference": passage.reference,
                    "scripture_text": passage.text,
                    "translation": passage.translation,
                    "stylized_quote": passage.text,
                    "context_note": str(item.get("context_note", "")).strip()[:800],
                    "connection_to_focus": str(
                        item.get("connection_to_focus", "")
                    ).strip()[:1000],
                    "reflection_prompts": _strings(item.get("reflection_prompts"), 3),
                    "application_suggestions": _strings(
                        item.get("application_suggestions"), 2
                    ),
                }
            )
            if len(results) >= wanted:
                break
        return results

    def extract_themes(self, intention: str) -> list:
        """Extract themes from a focus intention. Empty list if AI is unavailable."""
        prompt = f"""Analyze this focus intention and extract 3-5 spiritual/emotional themes:

"{intention}"

Return ONLY a JSON array of short lowercase theme strings, like:
["patience", "trust", "letting go"]"""
        try:
            data = self.generate_json(prompt, max_tokens=150)
        except LLMError as exc:
            logger.warning("Theme extraction unavailable: %s", exc.code)
            return []
        if isinstance(data, dict):
            data = next((v for v in data.values() if isinstance(v, list)), [])
        if not isinstance(data, list):
            return []
        return [str(t).strip().lower()[:40] for t in data if str(t).strip()][:5]

    def suggest_life_areas(self, intention: str, themes: list) -> list:
        """Suggest related life areas. Falls back to ["faith"]."""
        life_area_codes = [
            "faith",
            "integrity",
            "relationships",
            "purpose",
            "stewardship",
            "health",
            "growth",
            "service",
        ]
        prompt = f"""Given this focus intention and themes, which life areas are most relevant?

Intention: "{intention}"
Themes: {themes}

Available life areas: {life_area_codes}

Return ONLY a JSON array of 1-3 relevant life area codes, like:
["faith", "relationships"]"""
        try:
            data = self.generate_json(prompt, max_tokens=80)
        except LLMError as exc:
            logger.warning("Life-area suggestion unavailable: %s", exc.code)
            return ["faith"]
        if isinstance(data, dict):
            data = next((v for v in data.values() if isinstance(v, list)), [])
        areas = (
            [a for a in data if a in life_area_codes] if isinstance(data, list) else []
        )
        return areas[:3] or ["faith"]

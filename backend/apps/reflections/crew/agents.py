"""
AI Agents for the Devotional Guidance Crew.
Each agent has a specific role and personality.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all crew agents."""

    role: str = "Agent"
    goal: str = ""
    backstory: str = ""

    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or getattr(
            settings, "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        self.model = model or getattr(settings, "OLLAMA_MODEL", "llama3.1:8b")

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    def generate(self, prompt: str, context: dict = None) -> Optional[str]:
        """Generate a response from this agent."""
        system_prompt = self.get_system_prompt()

        if context:
            system_prompt += f"\n\nCONTEXT:\n{self._format_context(context)}"

        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 500,
                    },
                },
                timeout=60.0,
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()

        except Exception as e:
            logger.error(f"{self.role} generation failed: {e}")
            return None

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
- Reference specific verses when relevant
- Explain cultural/historical context briefly
- Connect scripture to the user's specific situation
- Never be preachy or condescending
- Keep responses under 100 words
- Use plain language, not religious jargon"""


class MentorAgent(BaseAgent):
    """Practical life wisdom from experience."""

    role = "Wise Mentor"
    goal = "Offer practical life wisdom"
    backstory = """You are a man who has lived through struggles - addiction,
    divorce, career failure, rebuilding. You speak from experience, not theory.
    You're direct but kind. You never shame. You've been where they are."""

    def get_system_prompt(self) -> str:
        return f"""You are the {self.role}.

ROLE: {self.goal}

PERSONALITY: {self.backstory}

GUIDELINES:
- Speak as someone who has been there
- Be direct but compassionate
- Offer practical, actionable advice
- Never lecture or moralize
- Acknowledge the difficulty of change
- Keep responses under 100 words
- Use "I" statements from experience when appropriate"""


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
    goal = "Select and present relevant scripture passages with context and reflection prompts"
    backstory = """You are a thoughtful curator of scripture who understands that
    different seasons of life call for different passages. You select verses that
    speak directly to someone's current focus - whether they're seeking patience,
    healing, courage, or wisdom. You present passages beautifully, with context
    that makes ancient words feel immediate and personal."""

    def get_system_prompt(self) -> str:
        return f"""You are the {self.role}.

ROLE: {self.goal}

PERSONALITY: {self.backstory}

GUIDELINES:
- Select passages that directly relate to the user's stated focus
- Provide brief historical/cultural context (1-2 sentences)
- Create a stylized quote format that highlights key phrases
- Explain how this passage connects to their specific intention
- Generate 2-3 reflection questions that are personal and probing
- Suggest 1-2 practical applications for their daily life
- Use various translations (NIV, ESV, NLT, MSG) based on what fits best
- Never be preachy - let the scripture speak for itself"""

    def curate_passages(
        self, intention: str, period_type: str, themes: list, num_passages: int = 7
    ) -> list:
        """Generate a series of devotional passages for a focus intention."""

        prompt = f"""The user has set a {period_type} focus intention:

"{intention}"

Identified themes: {', '.join(themes) if themes else 'general spiritual growth'}

Generate {num_passages} scripture passages that will guide them through this focus period.
Each passage should build on the previous, creating a journey of understanding.

For EACH passage, provide in this EXACT JSON format:
{{
    "scripture_reference": "Book Chapter:Verse-Verse",
    "scripture_text": "The full text of the passage",
    "translation": "NIV/ESV/NLT/MSG",
    "stylized_quote": "A beautifully formatted version highlighting key phrases with line breaks",
    "context_note": "1-2 sentences of historical/cultural context",
    "connection_to_focus": "How this specifically relates to their intention",
    "reflection_prompts": ["Question 1?", "Question 2?", "Question 3?"],
    "application_suggestions": ["Practical action 1", "Practical action 2"]
}}

Return a JSON array of {num_passages} passages. ONLY return valid JSON, no other text."""

        response = self.generate(prompt)

        if not response:
            return []

        # Parse JSON response
        import json
        import re

        try:
            # Try to extract JSON from response
            start = response.find("[")
            end = response.rfind("]") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                # Clean control characters that break JSON parsing
                json_str = re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", json_str)
                return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse devotional passages JSON: {e}")
            # Return a fallback passage
            return [
                {
                    "scripture_reference": "Philippians 4:6-7",
                    "scripture_text": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.",
                    "translation": "NIV",
                    "stylized_quote": "Do not be anxious about anything...\nthe peace of God will guard your hearts",
                    "context_note": "Paul wrote this while imprisoned, showing peace is possible in any circumstance.",
                    "connection_to_focus": "This passage speaks to finding peace and consistency in your spiritual walk.",
                    "reflection_prompts": [
                        "What causes you to feel anxious?",
                        "How can prayer help you find consistency?",
                    ],
                    "application_suggestions": [
                        "Start each day with a brief prayer",
                        "Write down one thing you're thankful for",
                    ],
                }
            ]

        return []

    def extract_themes(self, intention: str) -> list:
        """Extract themes from a user's focus intention."""

        prompt = f"""Analyze this focus intention and extract 3-5 spiritual/emotional themes:

"{intention}"

Return ONLY a JSON array of theme strings, like:
["patience", "trust", "letting go", "faith in uncertainty"]

No other text, just the JSON array."""

        response = self.generate(prompt)

        if not response:
            return []

        import json

        try:
            start = response.find("[")
            end = response.rfind("]") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except json.JSONDecodeError:
            pass

        return []

    def suggest_life_areas(self, intention: str, themes: list) -> list:
        """Suggest related life areas based on intention and themes."""

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
["faith", "relationships"]

No other text, just the JSON array."""

        response = self.generate(prompt)

        if not response:
            return ["faith"]

        import json

        try:
            start = response.find("[")
            end = response.rfind("]") + 1
            if start >= 0 and end > start:
                areas = json.loads(response[start:end])
                return [a for a in areas if a in life_area_codes]
        except json.JSONDecodeError:
            pass

        return ["faith"]

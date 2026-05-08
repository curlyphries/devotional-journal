"""
LLM prompt generation service with multiple backend support.
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

from django.conf import settings


class PromptService(ABC):
    """
    Abstract interface for LLM-backed prompt generation.
    """

    _PLAN_SYSTEM_PROMPT = """You are a biblical curriculum designer building structured devotional reading plans for men.

Given a topic, duration, and optional anchor passages, return a complete reading plan as valid JSON only.

The plan MUST have exactly {duration_days} days. Each day must have:
- day_number (int)
- passages: list of scripture references e.g. ["Romans 8:28-39"]
- theme_en: short phrase (max 60 chars) naming the day's theme
- theme_es: Spanish translation of theme_en
- reflection_prompt: one focused journal question tied to the passage

Return ONLY this JSON structure, no markdown, no explanation:
{{
  "title_en": "Plan title in English",
  "title_es": "Plan title in Spanish",
  "description_en": "2-3 sentence description in English",
  "description_es": "2-3 sentence description in Spanish",
  "days": [
    {{
      "day_number": 1,
      "passages": ["Book Chapter:Verses"],
      "theme_en": "Day theme",
      "theme_es": "Tema del día",
      "reflection_prompt": "Journal question for this day"
    }}
  ]
}}

Guidelines:
- Choose passages that progressively build on each other across weeks
- Prefer the Psalms, Proverbs, Gospels, and Epistles for practical application
- Anchor passages provided by the user must appear in the plan
- Keep themes direct and masculine — no religious jargon
- Reflection prompts must be specific, not generic ("What does faith mean to you?" is BAD)
"""

    def _parse_plan_response(self, text: str) -> Optional[dict]:
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(l for l in lines if not l.strip().startswith("```"))
        start = text.find("{")
        end = text.rfind("}") + 1
        if start < 0 or end <= start:
            return None
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            return None

    @abstractmethod
    def generate_reading_plan(
        self,
        topic: str,
        duration_days: int,
        category: str,
        anchor_passages: list[str],
        language: str,
    ) -> Optional[dict]:
        pass

    @abstractmethod
    def generate_reflection_prompts(
        self,
        passage_text: str,
        passage_reference: str,
        language: str,
        num_prompts: int = 3,
        context: Optional[str] = None,
    ) -> list[str]:
        pass

    @abstractmethod
    def generate_discussion_guide(
        self, passages: list[dict], group_size: int, language: str
    ) -> str:
        pass

    @abstractmethod
    def explore_heart_prompt(self, user_input: str, language: str) -> dict:
        pass

    def _get_explore_system_prompt(self, language: str) -> str:
        return f"""You are an intelligent Bible study agent for a men's devotional app.
The user will share what is on their mind — a struggle, question, topic, or life situation.

Your job is to:
1. Identify 5-8 specific Bible passages (book, chapter, verse_start, verse_end) that speak directly to their situation. Be thorough — cover different angles, books, and genres (narratives, psalms, proverbs, epistles, gospels). For broad topics like a person or theme, include ALL the major relevant passages across the Bible, not just a few. Be specific with verse ranges.
2. For each passage, write a one-sentence explanation of why it is relevant.
3. Generate 3-5 personal reflection prompts tailored to what they shared. Each prompt should push the user to examine a different aspect of their situation.
4. Suggest ONE reading plan category from this list: fatherhood, marriage, leadership, recovery, faith, general

Language: {language}
If "bilingual", naturally blend English and Spanish.

You MUST respond with valid JSON only, no markdown, no explanation outside the JSON:
{{
  "passages": [
    {{
      "book": "Romans",
      "chapter": 8,
      "verse_start": 28,
      "verse_end": 39,
      "reason": "Paul's powerful declaration that nothing can separate us from God's love"
    }}
  ],
  "prompts": [
    "Where in your life do you need to trust that God is working things for good?"
  ],
  "category": "faith",
  "summary": "A one-sentence summary of the spiritual theme you identified"
}}"""

    def _parse_explore_response(self, text: str) -> dict:
        text = text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            lines = text.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object in the text
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass
            logger.warning("AI explore response was not valid JSON: %s", text[:200])
            return {}


class OllamaPromptService(PromptService):
    """
    Ollama-based prompt generation for local development.
    """

    def __init__(self, base_url: str = "", model: str = ""):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model = model or settings.OLLAMA_MODEL

    def _get_system_prompt(self, language: str, num_prompts: int) -> str:
        return f"""You are a thoughtful men's devotional companion. Given a Bible passage,
generate {num_prompts} reflection questions that:
- Are direct and practical, not abstract or overly theological
- Connect scripture to real-world masculine experiences (work, leadership,
  fatherhood, integrity, struggle, purpose)
- Encourage honest self-examination without being preachy
- Are appropriate for men at varying levels of biblical literacy

Language: {language}
If "bilingual", naturally blend English and Spanish as a Valley/border
speaker would — not translated, but code-switched.

Respond with ONLY the questions, one per line, no numbering."""

    def generate_reflection_prompts(
        self,
        passage_text: str,
        passage_reference: str,
        language: str,
        num_prompts: int = 3,
        context: Optional[str] = None,
    ) -> list[str]:
        system_prompt = self._get_system_prompt(language, num_prompts)

        user_prompt = f"Passage: {passage_reference}\n\n{passage_text}"
        if context:
            user_prompt += f"\n\nContext: {context}"

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": user_prompt,
                        "system": system_prompt,
                        "stream": False,
                    },
                )
                response.raise_for_status()
                result = response.json()
                text = result.get("response", "")
                prompts = [
                    line.strip() for line in text.strip().split("\n") if line.strip()
                ]
                return prompts[:num_prompts]
        except Exception:
            return ["What does this passage reveal about God's character?"]

    def generate_discussion_guide(
        self, passages: list[dict], group_size: int, language: str
    ) -> str:
        system_prompt = f"""You are creating a discussion guide for a men's Bible study group of {group_size} members.
Create a structured discussion guide that:
- Opens with an icebreaker question
- Has 3-4 main discussion questions per passage
- Includes application questions
- Closes with a challenge for the week

Language: {language}
Format the output in clear sections with headers."""

        passages_text = "\n\n".join(
            [f"{p.get('reference', 'Unknown')}: {p.get('text', '')}" for p in passages]
        )

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"Create a discussion guide for these passages:\n\n{passages_text}",
                        "system": system_prompt,
                        "stream": False,
                    },
                )
                response.raise_for_status()
                result = response.json()
                return result.get("response", "")
        except Exception:
            return "Discussion guide generation failed. Please try again."

    def generate_reading_plan(
        self,
        topic: str,
        duration_days: int,
        category: str,
        anchor_passages: list[str],
        language: str,
    ) -> Optional[dict]:
        system = self._PLAN_SYSTEM_PROMPT.format(duration_days=duration_days)
        anchors = ", ".join(anchor_passages) if anchor_passages else "none"
        user_prompt = (
            f"Topic: {topic}\n"
            f"Duration: {duration_days} days\n"
            f"Category: {category}\n"
            f"Anchor passages: {anchors}\n"
            f"Language preference: {language}"
        )
        try:
            with httpx.Client(timeout=120.0) as client:
                response = client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": user_prompt,
                        "system": system,
                        "stream": False,
                        "format": "json",
                        "options": {"temperature": 0.5, "num_predict": 4000},
                    },
                )
                response.raise_for_status()
                result = response.json()
                return self._parse_plan_response(result.get("response", ""))
        except Exception:
            logger.exception("Ollama generate_reading_plan failed")
            return None

    def explore_heart_prompt(self, user_input: str, language: str) -> dict:
        system_prompt = self._get_explore_system_prompt(language)
        try:
            with httpx.Client(timeout=90.0) as client:
                response = client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": user_input,
                        "system": system_prompt,
                        "stream": False,
                        "format": "json",
                        "options": {"num_predict": 2000, "temperature": 0.7},
                    },
                )
                response.raise_for_status()
                result = response.json()
                return self._parse_explore_response(result.get("response", ""))
        except Exception:
            logger.exception("Ollama explore_heart_prompt failed")
            return {}


class AnthropicPromptService(PromptService):
    """
    Anthropic Claude-based prompt generation for production.
    """

    def __init__(self, api_key: str = "", model: str = ""):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.model = model or settings.ANTHROPIC_MODEL

    def _get_system_prompt(self, language: str, num_prompts: int) -> str:
        return f"""You are a thoughtful men's devotional companion. Given a Bible passage,
generate {num_prompts} reflection questions that:
- Are direct and practical, not abstract or overly theological
- Connect scripture to real-world masculine experiences (work, leadership,
  fatherhood, integrity, struggle, purpose)
- Encourage honest self-examination without being preachy
- Are appropriate for men at varying levels of biblical literacy

Language: {language}
If "bilingual", naturally blend English and Spanish as a Valley/border
speaker would — not translated, but code-switched.

Respond with ONLY the questions, one per line, no numbering."""

    def generate_reflection_prompts(
        self,
        passage_text: str,
        passage_reference: str,
        language: str,
        num_prompts: int = 3,
        context: Optional[str] = None,
    ) -> list[str]:
        user_prompt = f"Passage: {passage_reference}\n\n{passage_text}"
        if context:
            user_prompt += f"\n\nContext: {context}"

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "max_tokens": 500,
                        "system": self._get_system_prompt(language, num_prompts),
                        "messages": [{"role": "user", "content": user_prompt}],
                    },
                )
                response.raise_for_status()
                result = response.json()
                text = result["content"][0]["text"]
                prompts = [
                    line.strip() for line in text.strip().split("\n") if line.strip()
                ]
                return prompts[:num_prompts]
        except Exception:
            return ["What does this passage reveal about God's character?"]

    def generate_reading_plan(
        self,
        topic: str,
        duration_days: int,
        category: str,
        anchor_passages: list[str],
        language: str,
    ) -> Optional[dict]:
        system = self._PLAN_SYSTEM_PROMPT.format(duration_days=duration_days)
        anchors = ", ".join(anchor_passages) if anchor_passages else "none"
        user_prompt = (
            f"Topic: {topic}\n"
            f"Duration: {duration_days} days\n"
            f"Category: {category}\n"
            f"Anchor passages: {anchors}\n"
            f"Language preference: {language}"
        )
        try:
            with httpx.Client(timeout=120.0) as client:
                response = client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "max_tokens": 4000,
                        "system": system,
                        "messages": [{"role": "user", "content": user_prompt}],
                    },
                )
                response.raise_for_status()
                result = response.json()
                text = result["content"][0]["text"]
                return self._parse_plan_response(text)
        except Exception:
            logger.exception("Anthropic generate_reading_plan failed")
            return None

    def generate_discussion_guide(
        self, passages: list[dict], group_size: int, language: str
    ) -> str:
        return "Discussion guide generation not yet implemented for Anthropic."

    def explore_heart_prompt(self, user_input: str, language: str) -> dict:
        system_prompt = self._get_explore_system_prompt(language)
        try:
            with httpx.Client(timeout=45.0) as client:
                response = client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "max_tokens": 1200,
                        "system": system_prompt,
                        "messages": [{"role": "user", "content": user_input}],
                    },
                )
                response.raise_for_status()
                result = response.json()
                text = result["content"][0]["text"]
                return self._parse_explore_response(text)
        except Exception:
            logger.exception("Anthropic explore_heart_prompt failed")
            return {}


class OpenAICompatiblePromptService(PromptService):
    """
    OpenAI-compatible prompt generation (works with OpenAI, OpenRouter, and custom endpoints).
    """

    # Map provider names to their base URLs
    _PROVIDER_URLS = {
        "openai": "https://api.openai.com/v1",
        "openrouter": "https://openrouter.ai/api/v1",
    }

    def __init__(
        self,
        api_key: str,
        model: str = "",
        base_url: str = "",
        provider: str = "openai",
    ):
        self.api_key = api_key
        self.model = model or "gpt-4o-mini"
        self.base_url = base_url or self._PROVIDER_URLS.get(
            provider, self._PROVIDER_URLS["openai"]
        )

    def _chat(
        self,
        system: str,
        user_content: str,
        max_tokens: int = 1200,
        temperature: float = 0.7,
    ) -> str:
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "messages": [
                            {"role": "system", "content": system},
                            {"role": "user", "content": user_content},
                        ],
                    },
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except Exception:
            logger.exception(
                "OpenAI-compatible chat call failed (model=%s)", self.model
            )
            return ""

    def _get_system_prompt(self, language: str, num_prompts: int) -> str:
        return f"""You are a thoughtful men's devotional companion. Given a Bible passage,
generate {num_prompts} reflection questions that:
- Are direct and practical, not abstract or overly theological
- Connect scripture to real-world masculine experiences (work, leadership,
  fatherhood, integrity, struggle, purpose)
- Encourage honest self-examination without being preachy
- Are appropriate for men at varying levels of biblical literacy

Language: {language}
If "bilingual", naturally blend English and Spanish as a Valley/border
speaker would — not translated, but code-switched.

Respond with ONLY the questions, one per line, no numbering."""

    def generate_reflection_prompts(
        self,
        passage_text: str,
        passage_reference: str,
        language: str,
        num_prompts: int = 3,
        context: Optional[str] = None,
    ) -> list[str]:
        user_prompt = f"Passage: {passage_reference}\n\n{passage_text}"
        if context:
            user_prompt += f"\n\nContext: {context}"
        text = self._chat(
            self._get_system_prompt(language, num_prompts), user_prompt, max_tokens=500
        )
        if not text:
            return ["What does this passage reveal about God's character?"]
        prompts = [line.strip() for line in text.strip().split("\n") if line.strip()]
        return prompts[:num_prompts]

    def generate_reading_plan(
        self,
        topic: str,
        duration_days: int,
        category: str,
        anchor_passages: list[str],
        language: str,
    ) -> Optional[dict]:
        system = self._PLAN_SYSTEM_PROMPT.format(duration_days=duration_days)
        anchors = ", ".join(anchor_passages) if anchor_passages else "none"
        user_prompt = (
            f"Topic: {topic}\n"
            f"Duration: {duration_days} days\n"
            f"Category: {category}\n"
            f"Anchor passages: {anchors}\n"
            f"Language preference: {language}"
        )
        text = self._chat(system, user_prompt, max_tokens=4000, temperature=0.5)
        if not text:
            return None
        return self._parse_plan_response(text)

    def generate_discussion_guide(
        self, passages: list[dict], group_size: int, language: str
    ) -> str:
        system_prompt = f"""You are creating a discussion guide for a men's Bible study group of {group_size} members.
Create a structured discussion guide that:
- Opens with an icebreaker question
- Has 3-4 main discussion questions per passage
- Includes application questions
- Closes with a challenge for the week

Language: {language}
Format the output in clear sections with headers."""
        passages_text = "\n\n".join(
            [f"{p.get('reference', 'Unknown')}: {p.get('text', '')}" for p in passages]
        )
        text = self._chat(
            system_prompt,
            f"Create a discussion guide for these passages:\n\n{passages_text}",
            max_tokens=2000,
        )
        return text or "Discussion guide generation failed. Please try again."

    def explore_heart_prompt(self, user_input: str, language: str) -> dict:
        system_prompt = self._get_explore_system_prompt(language)
        text = self._chat(system_prompt, user_input, max_tokens=1200)
        if not text:
            return {}
        return self._parse_explore_response(text)


def get_prompt_service(user=None) -> PromptService:
    """
    Factory function to get the configured prompt service.
    Uses per-user AI settings when available, falling back to global config.
    """
    # Check per-user settings first
    if user and hasattr(user, "ai_provider") and user.ai_provider not in ("", "none"):
        provider = user.ai_provider
        api_key = user.get_ai_api_key() if hasattr(user, "get_ai_api_key") else ""
        model = user.ai_model or ""
        base_url = user.ai_base_url or ""

        if provider == "anthropic" and api_key:
            return AnthropicPromptService(api_key=api_key, model=model)
        elif provider == "ollama":
            return OllamaPromptService(base_url=base_url, model=model)
        elif provider in ("openai", "openrouter", "custom") and api_key:
            return OpenAICompatiblePromptService(
                api_key=api_key, model=model, base_url=base_url, provider=provider
            )
        # If user has a provider set but missing required key, fall through to global

    # Fall back to global settings
    backend = settings.LLM_BACKEND.lower()

    if backend == "ollama":
        return OllamaPromptService()
    elif backend == "anthropic":
        return AnthropicPromptService()
    else:
        return OllamaPromptService()

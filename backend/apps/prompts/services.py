"""
LLM prompt generation service with multiple backend support.
"""
import json
import logging
import httpx
from abc import ABC, abstractmethod
from typing import Optional

logger = logging.getLogger(__name__)

from django.conf import settings


class PromptService(ABC):
    """
    Abstract interface for LLM-backed prompt generation.
    """
    @abstractmethod
    def generate_reflection_prompts(
        self,
        passage_text: str,
        passage_reference: str,
        language: str,
        num_prompts: int = 3,
        context: Optional[str] = None
    ) -> list[str]:
        pass

    @abstractmethod
    def generate_discussion_guide(
        self,
        passages: list[dict],
        group_size: int,
        language: str
    ) -> str:
        pass

    @abstractmethod
    def explore_heart_prompt(self, user_input: str, language: str) -> dict:
        pass

    def _get_explore_system_prompt(self, language: str) -> str:
        return f"""You are an intelligent Bible study agent for a men's devotional app.
The user will share what is on their mind — a struggle, question, topic, or life situation.

Your job is to:
1. Identify 3-5 specific Bible passages (book, chapter, verse_start, verse_end) that speak directly to their situation. Include well-known stories, teachings, psalms, and proverbs. Be specific with verse ranges.
2. For each passage, write a one-sentence explanation of why it is relevant.
3. Generate 3 personal reflection prompts tailored to what they shared.
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
        if text.startswith('```'):
            lines = text.split('\n')
            lines = [l for l in lines if not l.strip().startswith('```')]
            text = '\n'.join(lines)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object in the text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass
            logger.warning('AI explore response was not valid JSON: %s', text[:200])
            return {}


class OllamaPromptService(PromptService):
    """
    Ollama-based prompt generation for local development.
    """
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

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
        context: Optional[str] = None
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
                        "stream": False
                    }
                )
                response.raise_for_status()
                result = response.json()
                text = result.get("response", "")
                prompts = [line.strip() for line in text.strip().split("\n") if line.strip()]
                return prompts[:num_prompts]
        except Exception as e:
            return [f"What does this passage reveal about God's character?"]

    def generate_discussion_guide(
        self,
        passages: list[dict],
        group_size: int,
        language: str
    ) -> str:
        system_prompt = f"""You are creating a discussion guide for a men's Bible study group of {group_size} members.
Create a structured discussion guide that:
- Opens with an icebreaker question
- Has 3-4 main discussion questions per passage
- Includes application questions
- Closes with a challenge for the week

Language: {language}
Format the output in clear sections with headers."""

        passages_text = "\n\n".join([
            f"{p.get('reference', 'Unknown')}: {p.get('text', '')}"
            for p in passages
        ])

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"Create a discussion guide for these passages:\n\n{passages_text}",
                        "system": system_prompt,
                        "stream": False
                    }
                )
                response.raise_for_status()
                result = response.json()
                return result.get("response", "")
        except Exception:
            return "Discussion guide generation failed. Please try again."

    def explore_heart_prompt(self, user_input: str, language: str) -> dict:
        system_prompt = self._get_explore_system_prompt(language)
        try:
            with httpx.Client(timeout=45.0) as client:
                response = client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": user_input,
                        "system": system_prompt,
                        "stream": False,
                        "format": "json",
                    }
                )
                response.raise_for_status()
                result = response.json()
                return self._parse_explore_response(result.get("response", ""))
        except Exception as e:
            logger.exception('Ollama explore_heart_prompt failed')
            return {}


class AnthropicPromptService(PromptService):
    """
    Anthropic Claude-based prompt generation for production.
    """
    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY
        self.model = settings.ANTHROPIC_MODEL

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
        context: Optional[str] = None
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
                        "content-type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "max_tokens": 500,
                        "system": self._get_system_prompt(language, num_prompts),
                        "messages": [{"role": "user", "content": user_prompt}]
                    }
                )
                response.raise_for_status()
                result = response.json()
                text = result["content"][0]["text"]
                prompts = [line.strip() for line in text.strip().split("\n") if line.strip()]
                return prompts[:num_prompts]
        except Exception:
            return [f"What does this passage reveal about God's character?"]

    def generate_discussion_guide(
        self,
        passages: list[dict],
        group_size: int,
        language: str
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
                        "content-type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "max_tokens": 1200,
                        "system": system_prompt,
                        "messages": [{"role": "user", "content": user_input}]
                    }
                )
                response.raise_for_status()
                result = response.json()
                text = result["content"][0]["text"]
                return self._parse_explore_response(text)
        except Exception as e:
            logger.exception('Anthropic explore_heart_prompt failed')
            return {}


def get_prompt_service() -> PromptService:
    """
    Factory function to get the configured prompt service.
    """
    backend = settings.LLM_BACKEND.lower()

    if backend == 'ollama':
        return OllamaPromptService()
    elif backend == 'anthropic':
        return AnthropicPromptService()
    else:
        return OllamaPromptService()

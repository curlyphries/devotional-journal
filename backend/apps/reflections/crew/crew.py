"""
DevotionalCrew - Orchestrates AI agents for personalized guidance.
"""
import logging
from typing import Optional

from django.conf import settings

from .agents import (
    ScriptureScholar,
    MentorAgent,
    PatternAnalyst,
    JourneyGuide,
    Coordinator,
)
from .tasks import (
    DailyInsightTask,
    WeeklyReviewTask,
    MonthlyRecapTask,
)

logger = logging.getLogger(__name__)


class DevotionalCrew:
    """
    AI Crew for personalized devotional guidance.
    
    Orchestrates multiple specialized agents to provide
    multi-perspective spiritual guidance.
    """
    
    def __init__(self, base_url: str = None, model: str = None):
        """
        Initialize the crew with LLM configuration.
        
        Args:
            base_url: Ollama API base URL
            model: Model name to use
        """
        self.base_url = base_url or getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = model or getattr(settings, 'OLLAMA_MODEL', 'llama3.1:8b')
        
        self._create_agents()
        self._create_tasks()
    
    def _create_agents(self):
        """Initialize all crew agents."""
        self.scripture_scholar = ScriptureScholar(self.base_url, self.model)
        self.mentor = MentorAgent(self.base_url, self.model)
        self.pattern_analyst = PatternAnalyst(self.base_url, self.model)
        self.journey_guide = JourneyGuide(self.base_url, self.model)
        self.coordinator = Coordinator(self.base_url, self.model)
        
        logger.info(f"Crew agents initialized with model {self.model}")
    
    def _create_tasks(self):
        """Initialize crew tasks."""
        self.daily_insight_task = DailyInsightTask(self)
        self.weekly_review_task = WeeklyReviewTask(self)
        self.monthly_recap_task = MonthlyRecapTask(self)
    
    def generate_daily_insight(self, user, reflection) -> Optional[str]:
        """
        Generate daily insight for a reflection.
        Lightweight - uses mentor + coordinator only.
        """
        try:
            return self.daily_insight_task.execute(user, reflection=reflection)
        except Exception as e:
            logger.error(f"Daily insight generation failed: {e}")
            return None
    
    def generate_weekly_review(self, user) -> Optional[str]:
        """
        Generate weekly review with full crew analysis.
        Runs all agents and synthesizes output.
        """
        try:
            return self.weekly_review_task.execute(user)
        except Exception as e:
            logger.error(f"Weekly review generation failed: {e}")
            return None
    
    def generate_monthly_recap(self, user) -> Optional[str]:
        """
        Generate monthly recap with trend analysis.
        Comprehensive analysis of the past month.
        """
        try:
            return self.monthly_recap_task.execute(user)
        except Exception as e:
            logger.error(f"Monthly recap generation failed: {e}")
            return None
    
    def ask_specific_agent(self, agent_name: str, prompt: str, context: dict = None) -> Optional[str]:
        """
        Ask a specific agent a question.
        
        Args:
            agent_name: One of 'scripture', 'mentor', 'patterns', 'journey', 'coordinator'
            prompt: The question or prompt
            context: Optional context dict
            
        Returns:
            Agent's response or None
        """
        agents = {
            'scripture': self.scripture_scholar,
            'mentor': self.mentor,
            'patterns': self.pattern_analyst,
            'journey': self.journey_guide,
            'coordinator': self.coordinator,
        }
        
        agent = agents.get(agent_name)
        if not agent:
            logger.warning(f"Unknown agent: {agent_name}")
            return None
        
        try:
            return agent.generate(prompt, context)
        except Exception as e:
            logger.error(f"Agent {agent_name} failed: {e}")
            return None
    
    def health_check(self) -> dict:
        """
        Check if the crew's LLM backend is accessible.
        
        Returns:
            Dict with status and details
        """
        import httpx
        
        try:
            response = httpx.get(
                f"{self.base_url}/api/tags",
                timeout=5.0
            )
            response.raise_for_status()
            data = response.json()
            models = [m['name'] for m in data.get('models', [])]
            
            model_available = any(self.model in m for m in models)
            
            return {
                'status': 'healthy' if model_available else 'degraded',
                'base_url': self.base_url,
                'model': self.model,
                'model_available': model_available,
                'available_models': models,
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'base_url': self.base_url,
                'model': self.model,
                'error': str(e),
            }


def get_crew(user=None) -> DevotionalCrew:
    """
    Factory function to get a DevotionalCrew instance.
    
    In the future, this will support user-specific AI provider configuration.
    For now, uses system Ollama.
    
    Args:
        user: Optional user for provider configuration (future)
        
    Returns:
        Configured DevotionalCrew instance
    """
    # Future: Check user's AI provider config
    # config = AIProviderConfig.objects.filter(user=user).first()
    # if config and config.provider != 'system_ollama':
    #     return DevotionalCrew(config.base_url, config.model)
    
    return DevotionalCrew()

import logging

from django.apps import AppConfig
from orchestrator import AgentOrchestrator

logger = logging.getLogger(__name__)


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    # Store global orchestrator instance
    orchestrator = None

    def ready(self):
        # Initialize orchestrator when app is ready
        # NOTE: In production with multiple workers, this creates separate instances per worker.
        # Since state is currently in-memory, this means state isn't shared across workers.
        # For a hackathon/demo, this is acceptable. For prod, use Redis/DB for state.
        if ApiConfig.orchestrator is None:
            try:
                ApiConfig.orchestrator = AgentOrchestrator()
                logger.info("AgentOrchestrator initialized in AppConfig.")
            except Exception as e:
                logger.error(f"Failed to initialize AgentOrchestrator: {e}")

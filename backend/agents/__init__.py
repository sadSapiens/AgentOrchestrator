"""
Пакет агентов для оркестратора
"""

from .analyzer import AnalyzerAgent
from .base_agent import BaseAgent
from .coordinator import CoordinatorAgent
from .generic import GenericAgent
from .researcher import ResearcherAgent
from .writer import WriterAgent

__all__ = [
    "BaseAgent",
    "ResearcherAgent",
    "AnalyzerAgent",
    "WriterAgent",
    "CoordinatorAgent",
    "GenericAgent",
]

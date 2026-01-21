"""
Пакет агентов для оркестратора
"""
from .base_agent import BaseAgent
from .researcher import ResearcherAgent
from .analyzer import AnalyzerAgent
from .writer import WriterAgent
from .coordinator import CoordinatorAgent

__all__ = [
    'BaseAgent',
    'ResearcherAgent',
    'AnalyzerAgent',
    'WriterAgent',
    'CoordinatorAgent'
]

"""
Универсальный агент для динамического создания
"""

from typing import Dict

from agents.base_agent import BaseAgent


class GenericAgent(BaseAgent):
    """Универсальный агент, параметры которого задаются при создании"""

    def __init__(
        self,
        name: str,
        role: str,
        system_prompt: str,
        capabilities: Dict[str, str] = None,
    ):
        super().__init__(name=name, role=role, system_prompt=system_prompt)
        self._capabilities = capabilities or {"general": "Выполнение инструкций"}

    def get_capabilities(self) -> Dict[str, str]:
        """Получить описание возможностей агента"""
        return self._capabilities

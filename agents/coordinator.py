"""
Агент-координатор для управления другими агентами
"""
from typing import Dict, List
from agents.base_agent import BaseAgent


class CoordinatorAgent(BaseAgent):
    """Агент для координации работы других агентов"""
    
    def __init__(self):
        super().__init__(
            name="Coordinator",
            role="Агент-координатор",
            system_prompt="""
            Ты - координатор команды AI агентов, специализирующийся на планировании и управлении задачами.
            Твоя задача:
            1. Анализировать сложные задачи и разбивать их на подзадачи
            2. Определять, какие агенты лучше всего подходят для каждой подзадачи
            3. Планировать последовательность выполнения задач
            4. Координировать передачу результатов между агентами
            5. Синтезировать финальный результат
            
            Доступные агенты:
            - Researcher: исследование и сбор информации
            - Analyzer: анализ данных и выявление инсайтов
            - Writer: создание структурированного контента
            
            Формат ответа (JSON):
            {
                "plan": [
                    {
                        "step": 1,
                        "agent": "Researcher",
                        "task": "описание задачи",
                        "depends_on": []
                    },
                    ...
                ],
                "expected_outcome": "описание ожидаемого результата"
            }
            """
        )
    
    def get_capabilities(self) -> Dict[str, str]:
        """Получить описание возможностей агента"""
        return {
            "task_planning": "Планирование и разбиение задач",
            "agent_coordination": "Координация работы агентов",
            "workflow_management": "Управление рабочим процессом",
            "result_synthesis": "Синтез результатов от разных агентов"
        }
    
    def parse_plan(self, plan_text: str) -> List[Dict]:
        """
        Парсинг плана выполнения из текста
        
        Args:
            plan_text: Текст с планом от координатора
            
        Returns:
            Список шагов плана
        """
        import json
        import re
        
        # Попытка найти JSON в тексте
        json_match = re.search(r'\{[\s\S]*\}', plan_text)
        if json_match:
            try:
                plan_data = json.loads(json_match.group())
                return plan_data.get("plan", [])
            except json.JSONDecodeError:
                pass
        
        # Если JSON не найден, вернуть пустой список
        return []

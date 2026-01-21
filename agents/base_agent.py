"""
Базовый класс для всех агентов
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import google.generativeai as genai
from utils.config import Config
from utils.logger import logger


class BaseAgent(ABC):
    """Базовый класс для всех AI агентов"""
    
    def __init__(self, name: str, role: str, system_prompt: str):
        """
        Инициализация агента
        
        Args:
            name: Имя агента
            role: Роль агента
            system_prompt: Системный промпт для агента
        """
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.history = []
        
        # Настройка Gemini API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # Создание модели
        self.model = genai.GenerativeModel(
            model_name=Config.MODEL_NAME,
            generation_config={
                "temperature": Config.TEMPERATURE,
                "max_output_tokens": Config.MAX_TOKENS,
            }
        )
        
        logger.info(f"[bold green]✓[/bold green] Агент '{self.name}' ({self.role}) инициализирован")
    
    def _create_prompt(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Создать полный промпт для модели
        
        Args:
            task: Задача для выполнения
            context: Дополнительный контекст
            
        Returns:
            Полный промпт
        """
        prompt_parts = [
            f"Ты - {self.role}.",
            f"Системная инструкция: {self.system_prompt}",
            "",
            f"Задача: {task}"
        ]
        
        if context:
            prompt_parts.append("")
            prompt_parts.append("Контекст:")
            for key, value in context.items():
                prompt_parts.append(f"- {key}: {value}")
        
        return "\n".join(prompt_parts)
    
    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Выполнить задачу
        
        Args:
            task: Задача для выполнения
            context: Дополнительный контекст
            
        Returns:
            Результат выполнения задачи
        """
        logger.agent_action(self.name, "Начало выполнения", task[:100])
        
        try:
            # Создать промпт
            prompt = self._create_prompt(task, context)
            
            # Выполнить запрос к модели
            response = await self.model.generate_content_async(prompt)
            result = response.text
            
            # Сохранить в историю
            self.history.append({
                "task": task,
                "context": context,
                "result": result
            })
            
            logger.agent_action(
                self.name, 
                "Завершено", 
                f"Результат: {len(result)} символов"
            )
            
            return result
            
        except Exception as e:
            error_msg = f"Ошибка при выполнении задачи: {str(e)}"
            logger.error(f"[bold red]✗[/bold red] {self.name}: {error_msg}")
            raise
    
    def get_history(self) -> list:
        """Получить историю выполнения задач"""
        return self.history
    
    @abstractmethod
    def get_capabilities(self) -> Dict[str, str]:
        """Получить описание возможностей агента"""
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', role='{self.role}')"

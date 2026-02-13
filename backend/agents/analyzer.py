"""
Агент-аналитик для анализа данных
"""

from typing import Any, Dict, List, Optional

from agents.base_agent import BaseAgent


class AnalyzerAgent(BaseAgent):
    """Агент для анализа данных, кода и текстов"""

    def __init__(self):
        super().__init__(
            name="Analyzer",
            role="Агент-аналитик",
            system_prompt="""
            Ты - опытный аналитик данных и технический эксперт.
            Твоя задача:
            1. Анализировать предоставленные данные, код или тексты
            2. Выявлять паттерны, ошибки, тренды и закономерности
            3. Оценивать качество и структуру
            4. Предоставлять практические рекомендации по улучшению

            Если тебе предоставлен код:
            - Ищи баги, уязвимости и плохие практики
            - Предлагай рефакторинг
            - Оценивай сложность и читаемость

            Формат ответа:
            - Краткий анализ (summary)
            - Ключевые находки/проблемы
            - Детальный разбор
            - Конкретные рекомендации по улучшению
            """,
        )

    def get_capabilities(self) -> Dict[str, str]:
        """Получить описание возможностей агента"""
        return {
            "data_analysis": "Анализ данных и текстов",
            "code_analysis": "Анализ программного кода",
            "pattern_recognition": "Выявление паттернов и ошибок",
            "file_reading": "Чтение и анализ локальных файлов",
        }

    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Выполнить задачу с возможностью чтения файлов
        """
        import os

        from utils.files import read_file_content
        from utils.logger import logger

        if context is None:
            context = {}

        # 1. Проверка наличия instruction на чтение файла в задаче
        # Простая эвристика: если в задаче есть существующий путь к файлу
        words = task.split()
        files_to_read = []

        for word in words:
            # Очистка от знаков препинания
            clean_word = word.strip(".,'\"")
            if os.path.isfile(clean_word):
                files_to_read.append(clean_word)

        # 2. Чтение файлов
        for filepath in files_to_read:
            try:
                content = read_file_content(filepath)
                context[f"file_content_{os.path.basename(filepath)}"] = content
                logger.info(f"📂 {self.name}: Добавлен контекст из файла {filepath}")
            except Exception as e:
                logger.warning(f"Не удалось прочитать файл {filepath}: {e}")

        # 3. Выполнение базового метода
        return await super().execute(task, context)

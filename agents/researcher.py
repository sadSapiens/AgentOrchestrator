"""
Агент-исследователь для сбора информации
"""
from typing import Dict, List, Optional, Any
from agents.base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    """Агент для исследования тем и сбора информации с доступом в интернет"""
    
    def __init__(self):
        super().__init__(
            name="Researcher",
            role="Агент-исследователь",
            system_prompt="""
            Ты - опытный исследователь с доступом в интернет.
            Твоя задача:
            1. Анализировать полученные поисковые результаты
            2. Отвечать на запрос пользователя, основываясь ИСКЛЮЧИТЕЛЬНО на найденных фактах
            3. Если информации недостаточно, честно об этом сообщать
            4. Обязательно указывать ссылки на источники
            
            Формат ответа:
            - Краткое резюме найденой информации
            - Основные факты (с указанием источника [1], [2]...)
            - Детальный разбор
            - Список использованных источников (URL)
            """
        )
        
    def get_capabilities(self) -> Dict[str, str]:
        """Получить описание возможностей агента"""
        return {
            "research": "Исследование тем с поиском в интернете",
            "fact_checking": "Проверка фактов",
            "market_analysis": "Анализ рынка по актуальным данным"
        }

    async def _generate_search_queries(self, task: str) -> List[str]:
        """Генерация поисковых запросов на основе задачи"""
        prompt = f"""
        На основе задачи "{task}", сформулируй 3 эффективных поисковых запроса для Google/DuckDuckGo.
        Верни только запросы, каждый с новой строки, без нумерации и лишних слов.
        Максимум 3 запроса.
        """
        response = await self.model.generate_content_async(prompt)
        queries = [line.strip() for line in response.text.split('\n') if line.strip()]
        return queries[:3]

    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Выполнить задачу с предварительным поиском
        """
        from utils.web_search import search_web, format_search_results
        from utils.logger import logger
        
        # 1. Генерация запросов
        logger.info(f"🤔 {self.name}: Формулирую поисковые запросы...")
        queries = await self._generate_search_queries(task)
        
        # 2. Поиск информации
        all_results = []
        for query in queries:
            results = search_web(query, max_results=3)
            all_results.extend(results)
            
        # Удаление дубликатов по URL
        unique_results = {r['href']: r for r in all_results}.values()
        
        # 3. Формирование контекста
        search_context = format_search_results(list(unique_results))
        
        # 4. Обновление контекста для основного запроса
        if context is None:
            context = {}
        
        context["search_results"] = search_context
        
        logger.info(f"📚 {self.name}: Анализирую {len(unique_results)} источников...")
        
        # 5. Выполнение базового метода generate
        return await super().execute(task, context)

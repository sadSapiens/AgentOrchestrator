from typing import Dict, List

from duckduckgo_search import DDGS
from utils.logger import logger


def search_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Поиск в интернете через DuckDuckGo

    Args:
        query: Поисковый запрос
        max_results: Максимальное количество результатов

    Returns:
        Список словарей с результатами (title, href, body)
    """
    logger.info(f"🔎 Поиск: {query}")
    results = []

    try:
        with DDGS() as ddgs:
            # Используем text() для текстового поиска
            # backend="api" обычно быстрее и стабильнее для простых запросов
            search_gen = ddgs.text(query, max_results=max_results, backend="api")

            for r in search_gen:
                results.append(
                    {
                        "title": r.get("title", ""),
                        "href": r.get("href", ""),
                        "body": r.get("body", ""),
                    }
                )

        logger.info(f"✓ Найдено результатов: {len(results)}")
        return results

    except Exception as e:
        logger.error(f"[bold red]✗[/bold red] Ошибка при поиске: {str(e)}")
        return []


def format_search_results(results: List[Dict[str, str]]) -> str:
    """
    Форматирование результатов поиска в строку

    Args:
        results: Список результатов

    Returns:
        Отформатированная строка
    """
    if not results:
        return "Результатов не найдено."

    formatted = []
    for i, r in enumerate(results, 1):
        formatted.append(f"Source {i}: {r['title']}")
        formatted.append(f"URL: {r['href']}")
        formatted.append(f"Content: {r['body']}\n")

    return "\n".join(formatted)

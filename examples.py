#!/usr/bin/env python3
"""
Примеры использования оркестратора агентов
"""
import asyncio
from orchestrator import AgentOrchestrator
from utils.logger import logger


async def example_single_agent():
    """Пример использования одного агента"""
    print("\n" + "="*60)
    print("ПРИМЕР 1: Использование одного агента (Researcher)")
    print("="*60 + "\n")
    
    orchestrator = AgentOrchestrator()
    
    # Выполнить задачу исследователем
    result = await orchestrator.execute_single_task(
        agent_name="researcher",
        task="Исследовать основные принципы квантовых вычислений"
    )
    
    print("\n--- Результат ---")
    print(result[:500] + "..." if len(result) > 500 else result)


async def example_analyzer():
    """Пример использования аналитика"""
    print("\n" + "="*60)
    print("ПРИМЕР 2: Использование агента-аналитика")
    print("="*60 + "\n")
    
    orchestrator = AgentOrchestrator()
    
    # Выполнить анализ
    result = await orchestrator.execute_single_task(
        agent_name="analyzer",
        task="Проанализировать текущие тренды в области искусственного интеллекта",
        context={
            "year": "2026",
            "focus_areas": ["LLM", "Computer Vision", "Robotics"]
        }
    )
    
    print("\n--- Результат ---")
    print(result[:500] + "..." if len(result) > 500 else result)


async def example_orchestration():
    """Пример оркестрации нескольких агентов"""
    print("\n" + "="*60)
    print("ПРИМЕР 3: Оркестрация нескольких агентов")
    print("="*60 + "\n")
    
    orchestrator = AgentOrchestrator()
    
    # Выполнить сложную задачу с оркестрацией
    results = await orchestrator.orchestrate_task(
        "Создать подробный отчет о влиянии блокчейн технологий на финансовую индустрию"
    )
    
    print("\n--- План выполнения ---")
    print(results.get("plan", "План не создан")[:300] + "...")
    
    print("\n--- Шаги выполнения ---")
    for step in results.get("steps", []):
        print(f"\nШаг {step['step']}: {step['agent']}")
        result = step.get("result", "")
        print(result[:200] + "..." if len(result) > 200 else result)
    
    print("\n--- Финальный результат ---")
    final = results.get("final_result", "")
    print(final[:500] + "..." if len(final) > 500 else final)


async def example_writer():
    """Пример использования писателя"""
    print("\n" + "="*60)
    print("ПРИМЕР 4: Использование агента-писателя")
    print("="*60 + "\n")
    
    orchestrator = AgentOrchestrator()
    
    # Создать контент
    result = await orchestrator.execute_single_task(
        agent_name="writer",
        task="Написать краткую статью о преимуществах использования AI агентов в бизнесе",
        context={
            "target_audience": "бизнес-руководители",
            "tone": "профессиональный, но доступный",
            "length": "500-700 слов"
        }
    )
    
    print("\n--- Результат ---")
    print(result)


async def example_list_agents():
    """Пример получения списка агентов"""
    print("\n" + "="*60)
    print("ПРИМЕР 5: Список доступных агентов")
    print("="*60 + "\n")
    
    orchestrator = AgentOrchestrator()
    
    agents_info = orchestrator.list_agents()
    
    for name, info in agents_info.items():
        print(f"\n{name.upper()}")
        print(f"  Роль: {info['role']}")
        print(f"  Возможности:")
        for cap_name, cap_desc in info['capabilities'].items():
            print(f"    - {cap_desc}")


async def main():
    """Запустить все примеры"""
    print("\n" + "="*60)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ОРКЕСТРАТОРА АГЕНТОВ")
    print("="*60)
    
    # Примечание: для работы примеров нужен API ключ Gemini
    print("\nПримечание: Убедитесь, что у вас установлен GEMINI_API_KEY в .env файле")
    print("Для получения ключа посетите: https://makersuite.google.com/app/apikey")
    
    try:
        # Запустить примеры
        await example_list_agents()
        
        # Раскомментируйте нужные примеры после настройки API ключа:
        # await example_single_agent()
        # await example_analyzer()
        # await example_writer()
        # await example_orchestration()
        
        print("\n" + "="*60)
        print("Примеры завершены!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\nОшибка: {str(e)}")
        print("\nПроверьте, что:")
        print("1. Установлен GEMINI_API_KEY в .env файле")
        print("2. Установлены все зависимости (pip install -r requirements.txt)")


if __name__ == "__main__":
    asyncio.run(main())

"""
Главный оркестратор для управления агентами
"""
import asyncio
from typing import Dict, List, Optional, Any
from agents import ResearcherAgent, AnalyzerAgent, WriterAgent, CoordinatorAgent
from utils.logger import logger
from utils.config import Config


class AgentOrchestrator:
    """Оркестратор для управления командой AI агентов"""
    
    def __init__(self):
        """Инициализация оркестратора"""
        # Проверка конфигурации
        Config.validate()
        
        # Инициализация агентов
        self.agents = {
            "researcher": ResearcherAgent(),
            "analyzer": AnalyzerAgent(),
            "writer": WriterAgent(),
            "coordinator": CoordinatorAgent()
        }
        
        logger.info("[bold green]✓[/bold green] Оркестратор инициализирован")
        logger.info(f"Доступно агентов: {len(self.agents)}")
    
    def get_agent(self, agent_name: str):
        """
        Получить агента по имени
        
        Args:
            agent_name: Имя агента
            
        Returns:
            Экземпляр агента
        """
        agent = self.agents.get(agent_name.lower())
        if not agent:
            raise ValueError(f"Агент '{agent_name}' не найден")
        return agent
    
    async def execute_single_task(
        self, 
        agent_name: str, 
        task: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Выполнить задачу одним агентом
        
        Args:
            agent_name: Имя агента
            task: Задача для выполнения
            context: Дополнительный контекст
            
        Returns:
            Результат выполнения
        """
        logger.task_start(f"Задача для {agent_name}")
        
        try:
            agent = self.get_agent(agent_name)
            result = await agent.execute(task, context)
            logger.task_end(f"Задача для {agent_name}", success=True)
            return result
        except Exception as e:
            logger.task_end(f"Задача для {agent_name}", success=False)
            raise
    
    async def orchestrate_task(self, task: str) -> Dict[str, Any]:
        """
        Оркестрировать выполнение сложной задачи несколькими агентами
        
        Args:
            task: Сложная задача для выполнения
            
        Returns:
            Словарь с результатами от всех агентов
        """
        logger.task_start("Оркестрация задачи")
        
        results = {
            "original_task": task,
            "steps": []
        }
        
        try:
            # Шаг 1: Координатор создает план
            logger.info("[bold yellow]Шаг 1:[/bold yellow] Создание плана выполнения")
            coordinator = self.get_agent("coordinator")
            plan_text = await coordinator.execute(
                f"Создай план выполнения следующей задачи: {task}"
            )
            
            plan = coordinator.parse_plan(plan_text)
            results["plan"] = plan_text
            
            # Если план не удалось распарсить, выполняем стандартный workflow
            if not plan:
                logger.warning("План не распознан, используется стандартный workflow")
                plan = [
                    {"step": 1, "agent": "researcher", "task": task},
                    {"step": 2, "agent": "analyzer", "task": "Проанализируй собранную информацию"},
                    {"step": 3, "agent": "writer", "task": "Создай финальный отчет"}
                ]
            
            # Шаг 2: Выполнение плана
            context = {}
            for step_info in plan:
                step_num = step_info.get("step", 0)
                agent_name = step_info.get("agent", "").lower()
                step_task = step_info.get("task", "")
                
                if not agent_name or not step_task:
                    continue
                
                logger.info(f"[bold yellow]Шаг {step_num}:[/bold yellow] {agent_name}")
                
                try:
                    agent = self.get_agent(agent_name)
                    result = await agent.execute(step_task, context)
                    
                    # Сохранить результат в контекст для следующих шагов
                    context[f"{agent_name}_result"] = result
                    
                    results["steps"].append({
                        "step": step_num,
                        "agent": agent_name,
                        "task": step_task,
                        "result": result
                    })
                    
                except Exception as e:
                    logger.error(f"Ошибка на шаге {step_num}: {str(e)}")
                    results["steps"].append({
                        "step": step_num,
                        "agent": agent_name,
                        "task": step_task,
                        "error": str(e)
                    })
            
            # Шаг 3: Финальный результат
            if results["steps"]:
                last_step = results["steps"][-1]
                results["final_result"] = last_step.get("result", "")
            
            logger.task_end("Оркестрация задачи", success=True)
            return results
            
        except Exception as e:
            logger.task_end("Оркестрация задачи", success=False)
            raise
    
    def list_agents(self) -> Dict[str, Dict[str, str]]:
        """
        Получить список всех агентов и их возможностей
        
        Returns:
            Словарь с информацией об агентах
        """
        agents_info = {}
        for name, agent in self.agents.items():
            agents_info[name] = {
                "name": agent.name,
                "role": agent.role,
                "capabilities": agent.get_capabilities()
            }
        return agents_info
    
    def get_agent_history(self, agent_name: str) -> List[Dict]:
        """
        Получить историю выполнения задач агента
        
        Args:
            agent_name: Имя агента
            
        Returns:
            История выполнения
        """
        agent = self.get_agent(agent_name)
        return agent.get_history()

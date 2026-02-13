"""
Главный оркестратор для управления агентами
"""

import asyncio
from typing import Any, Dict, List, Optional

from agents import AnalyzerAgent, CoordinatorAgent, ResearcherAgent, WriterAgent
from utils.config import Config
from utils.files import save_text_to_file
from utils.logger import logger


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
            "coordinator": CoordinatorAgent(),
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

    def add_agent(
        self,
        agent_name: str,
        role: str,
        system_prompt: str,
        capabilities: Dict[str, str] = None,
    ) -> Any:
        """
        Динамически добавить нового агента

        Args:
            agent_name: Имя агента
            role: Роль агента
            system_prompt: Системный промпт
            capabilities: Словарь возможностей

        Returns:
            Созданный экземпляр агента
        """
        from agents.generic import GenericAgent

        # Создаем нового агента
        new_agent = GenericAgent(
            name=agent_name.capitalize(),
            role=role,
            system_prompt=system_prompt,
            capabilities=capabilities,
        )

        self.agents[agent_name.lower()] = new_agent

        # Обновляем промпт координатора, чтобы он знал о новом агенте
        self._update_coordinator_knowledge()

        logger.info(
            f"[bold green]✓[/bold green] Добавлен новый агент: {agent_name} ({role})"
        )
        return new_agent

    def _update_coordinator_knowledge(self):
        """Обновить системный промпт координатора списком всех агентов"""
        try:
            coordinator = self.get_agent("coordinator")

            # Формируем список агентов
            agents_list = "Доступные агенты:\n"
            for name, agent in self.agents.items():
                if name == "coordinator":
                    continue
                agents_list += f"            - {agent.name}: {agent.role}\n"

            # Находим место в промпте и заменяем (упрощенная логика)
            # В идеале нужно использовать более надежный шаблон, но пока просто заменим блок "Доступные агенты"
            import re

            # Ищем блок начинающийся с "Доступные агенты:" и до "Формат ответа"
            pattern = r"(Доступные агенты:[\s\S]*?)(?=Формат ответа)"

            if re.search(pattern, coordinator.system_prompt):
                coordinator.system_prompt = re.sub(
                    pattern, f"{agents_list}\n            ", coordinator.system_prompt
                )
                logger.info("Промпт координатора обновлен")
            else:
                logger.warning("Не удалось найти секцию агентов в промпте координатора")

        except Exception as e:
            logger.error(f"Ошибка обновления координатора: {e}")

    async def execute_single_task(
        self,
        agent_name: str,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        output_dir: Optional[str] = None,
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

            if output_dir:
                agent.save_result(result, directory=output_dir)

            return result
        except Exception:
            logger.task_end(f"Задача для {agent_name}", success=False)
            raise

    async def orchestrate_task_stream(
        self, task: str, output_dir: Optional[str] = None
    ):
        """
        Orchestrate a complex task and stream progress updates.

        Args:
            task: Task to orchestrate
            output_dir: Output directory (optional)

        Yields:
            Progress events (dicts)
        """
        logger.task_start("Orchestration Stream")

        results = {"original_task": task, "steps": []}

        try:
            # Yield initial event
            yield {"type": "start", "task": task}

            # Step 1: Create Plan
            logger.info("[bold yellow]Step 1:[/bold yellow] Creating execution plan")
            yield {
                "type": "step_start",
                "step": 1,
                "agent": "coordinator",
                "task": "Creating plan",
            }

            coordinator = self.get_agent("coordinator")
            plan_text = await coordinator.execute(
                f"Создай план выполнения следующей задачи: {task}"
            )

            plan = coordinator.parse_plan(plan_text)
            results["plan"] = plan_text

            yield {
                "type": "step_complete",
                "step": 1,
                "agent": "coordinator",
                "result": plan_text,
            }

            # Fallback plan
            if not plan:
                logger.warning("Plan not recognized, using default workflow")
                plan = [
                    {"step": 1, "agent": "researcher", "task": task},
                    {
                        "step": 2,
                        "agent": "analyzer",
                        "task": "Validate and refine data",
                    },
                    {"step": 3, "agent": "writer", "task": "Create final report"},
                ]

            yield {"type": "plan_created", "plan": plan}

            # Step 2: Execute Plan
            context = {}
            steps_by_id = {}
            for step_info in plan:
                step_num = step_info.get("step", 0)
                if step_num not in steps_by_id:
                    steps_by_id[step_num] = []
                steps_by_id[step_num].append(step_info)

            sorted_step_nums = sorted(steps_by_id.keys())

            for step_num in sorted_step_nums:
                step_group = steps_by_id[step_num]

                # Single task
                if len(step_group) == 1:
                    step_info = step_group[0]
                    agent_name = step_info.get("agent", "").lower()
                    step_task = step_info.get("task", "")

                    if not agent_name or not step_task:
                        continue

                    logger.info(
                        f"[bold yellow]Step {step_num}:[/bold yellow] {agent_name}"
                    )
                    yield {
                        "type": "step_start",
                        "step": step_num,
                        "agent": agent_name,
                        "task": step_task,
                    }

                    try:
                        agent = self.get_agent(agent_name)
                        result = await agent.execute(step_task, context)

                        context[f"{agent_name}_result"] = result
                        step_result = {
                            "step": step_num,
                            "agent": agent_name,
                            "task": step_task,
                            "result": result,
                        }
                        results["steps"].append(step_result)
                        yield {"type": "step_complete", **step_result}

                    except Exception as e:
                        logger.error(f"Error at step {step_num}: {str(e)}")
                        error_result = {
                            "step": step_num,
                            "agent": agent_name,
                            "task": step_task,
                            "error": str(e),
                        }
                        results["steps"].append(error_result)
                        yield {"type": "error", **error_result}

                else:
                    # Parallel Execution
                    logger.info(
                        f"[bold yellow]Step {step_num}:[/bold yellow] Parallel execution of {len(step_group)} tasks"
                    )
                    yield {
                        "type": "step_group_start",
                        "step": step_num,
                        "count": len(step_group),
                    }

                    tasks = []
                    step_indices = []

                    for i, step_info in enumerate(step_group):
                        agent_name = step_info.get("agent", "").lower()
                        step_task = step_info.get("task", "")

                        logger.info(f"  • {agent_name}: {step_task[:50]}...")
                        yield {
                            "type": "step_start",
                            "step": step_num,
                            "agent": agent_name,
                            "task": step_task,
                            "is_parallel": True,
                        }

                        try:
                            agent = self.get_agent(agent_name)
                            tasks.append(agent.execute(step_task, context))
                            step_indices.append(i)
                        except Exception as e:
                            logger.error(f"Error preparing task for {agent_name}: {e}")
                            yield {
                                "type": "error",
                                "step": step_num,
                                "agent": agent_name,
                                "error": str(e),
                            }

                    if tasks:
                        # Use as_completed to stream parallel results as they finish?
                        # Or gather if we want simpler logic. Let's use gather for simplicity first,
                        # but yield "processing..."
                        group_results = await asyncio.gather(
                            *tasks, return_exceptions=True
                        )

                        for i, result in enumerate(group_results):
                            original_info = step_group[step_indices[i]]
                            agent_name = original_info.get("agent", "").lower()

                            if isinstance(result, Exception):
                                logger.error(
                                    f"Error in parallel task ({agent_name}): {result}"
                                )
                                error_result = {
                                    "step": step_num,
                                    "agent": agent_name,
                                    "task": original_info.get("task"),
                                    "error": str(result),
                                }
                                results["steps"].append(error_result)
                                yield {"type": "error", **error_result}
                            else:
                                context[f"{agent_name}_result_{i}"] = (
                                    result  # Unique key
                                )
                                step_result = {
                                    "step": step_num,
                                    "agent": agent_name,
                                    "task": original_info.get("task"),
                                    "result": result,
                                }
                                results["steps"].append(step_result)
                                yield {"type": "step_complete", **step_result}

            # Step 3: Final Result
            if results["steps"]:
                last_step = results["steps"][-1]
                results["final_result"] = last_step.get("result", "")

                if output_dir and results["final_result"]:
                    save_text_to_file(
                        results["final_result"],
                        directory=output_dir,
                        prefix="orchestrated_result",
                    )

            yield {
                "type": "final",
                "result": results.get("final_result", ""),
                "full_data": results,
            }
            logger.task_end("Orchestration Stream", success=True)

        except Exception as e:
            logger.task_end("Orchestration Stream", success=False)
            yield {"type": "fatal_error", "error": str(e)}
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
                "capabilities": agent.get_capabilities(),
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

    def save_session(self, filepath: str):
        """
        Сохранить сессию (состояние всех агентов)

        Args:
            filepath: Путь к файлу
        """
        import json

        try:
            state = {name: agent.get_state() for name, agent in self.agents.items()}

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)

            logger.info(f"[bold green]✓[/bold green] Сессия сохранена в {filepath}")

        except Exception as e:
            logger.error(f"[bold red]✗[/bold red] Ошибка сохранения сессии: {str(e)}")
            raise

    def load_session(self, filepath: str):
        """
        Загрузить сессию (состояние всех агентов)

        Args:
            filepath: Путь к файлу
        """
        import json
        import os

        if not os.path.exists(filepath):
            logger.error(f"[bold red]✗[/bold red] Файл сессии {filepath} не найден")
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                state = json.load(f)

            for name, agent_state in state.items():
                if name in self.agents:
                    self.agents[name].set_state(agent_state)

            logger.info(f"[bold green]✓[/bold green] Сессия загружена из {filepath}")

        except Exception as e:
            msg = f"[bold red]✗[/bold red] Ошибка загрузки сессии: {str(e)}"
            logger.error(msg)
            raise

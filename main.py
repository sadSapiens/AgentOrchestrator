#!/usr/bin/env python3
"""
CLI интерфейс для оркестратора агентов
"""
import asyncio
import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from orchestrator import AgentOrchestrator
from utils.logger import logger

console = Console()


def print_banner():
    """Вывести баннер приложения"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           🤖 Agent Orchestrator с Gemini API 🤖           ║
    ║                                                           ║
    ║         Оркестратор AI-агентов для сложных задач         ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def print_agents_table(orchestrator: AgentOrchestrator):
    """
    Вывести таблицу с доступными агентами
    
    Args:
        orchestrator: Экземпляр оркестратора
    """
    agents_info = orchestrator.list_agents()
    
    table = Table(title="Доступные агенты", show_header=True, header_style="bold magenta")
    table.add_column("Агент", style="cyan", width=15)
    table.add_column("Роль", style="green", width=20)
    table.add_column("Возможности", style="yellow")
    
    for name, info in agents_info.items():
        capabilities = "\n".join([f"• {cap}" for cap in info["capabilities"].values()])
        table.add_row(name, info["role"], capabilities)
    
    console.print(table)


async def run_single_task(orchestrator: AgentOrchestrator, agent_name: str, task: str, output_dir: str = None, input_file: str = None):
    """
    Выполнить задачу одним агентом
    
    Args:
        orchestrator: Экземпляр оркестратора
        agent_name: Имя агента
        task: Задача для выполнения
        output_dir: Директория для сохранения результата
        input_file: Путь к входному файлу
    """
    try:
        context = {}
        if input_file:
            from utils.files import read_file_content
            content = read_file_content(input_file)
            context["file_content"] = content
            context["file_path"] = input_file
            task = f"{task}\n\nАнализируй файл: {input_file}"
            
        result = await orchestrator.execute_single_task(agent_name, task, context=context, output_dir=output_dir)
        
        # Вывести результат
        console.print("\n")
        console.print(Panel(
            Markdown(result),
            title=f"[bold green]Результат от {agent_name}[/bold green]",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"\n[bold red]Ошибка:[/bold red] {str(e)}")
        sys.exit(1)


async def run_orchestrated_task(orchestrator: AgentOrchestrator, task: str, output_dir: str = None):
    """
    Выполнить оркестрированную задачу
    
    Args:
        orchestrator: Экземпляр оркестратора
        task: Задача для выполнения
        output_dir: Директория для сохранения результата
    """
    try:
        results = await orchestrator.orchestrate_task(task, output_dir=output_dir)
        
        # Вывести план
        console.print("\n")
        console.print(Panel(
            results.get("plan", "План не создан"),
            title="[bold yellow]План выполнения[/bold yellow]",
            border_style="yellow"
        ))
        
        # Вывести результаты каждого шага
        for step in results.get("steps", []):
            step_num = step.get("step", 0)
            agent = step.get("agent", "unknown")
            result = step.get("result", "")
            error = step.get("error")
            
            if error:
                console.print(Panel(
                    f"[bold red]Ошибка:[/bold red] {error}",
                    title=f"[bold red]Шаг {step_num}: {agent}[/bold red]",
                    border_style="red"
                ))
            else:
                console.print(Panel(
                    Markdown(result[:500] + "..." if len(result) > 500 else result),
                    title=f"[bold cyan]Шаг {step_num}: {agent}[/bold cyan]",
                    border_style="cyan"
                ))
        
        # Вывести финальный результат
        final_result = results.get("final_result", "")
        if final_result:
            console.print("\n")
            console.print(Panel(
                Markdown(final_result),
                title="[bold green]Финальный результат[/bold green]",
                border_style="green"
            ))
        
    except Exception as e:
        console.print(f"\n[bold red]Ошибка:[/bold red] {str(e)}")
        sys.exit(1)


async def interactive_mode(orchestrator: AgentOrchestrator):
    """
    Интерактивный режим работы
    
    Args:
        orchestrator: Экземпляр оркестратора
    """
    console.print("\n[bold green]Интерактивный режим[/bold green]")
    console.print("Введите 'help' для справки, 'quit' для выхода\n")
    
    while True:
        try:
            command = console.input("[bold cyan]>[/bold cyan] ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['quit', 'exit', 'q']:
                console.print("[bold yellow]До свидания![/bold yellow]")
                break
            
            if command.lower() == 'help':
                help_text = """
                Доступные команды:
                
                • list - показать список агентов
                • task <agent> <задача> - выполнить задачу одним агентом
                • orchestrate <задача> - выполнить оркестрированную задачу
                • history <agent> - показать историю агента
                • help - показать эту справку
                • quit - выйти
                
                Примеры:
                • task researcher Исследовать квантовые компьютеры
                • orchestrate Создать отчет о блокчейн технологиях
                """
                console.print(Panel(help_text, title="Справка", border_style="blue"))
                continue
            
            if command.lower() == 'list':
                print_agents_table(orchestrator)
                continue
            
            if command.lower().startswith('task '):
                parts = command.split(' ', 2)
                if len(parts) < 3:
                    console.print("[bold red]Ошибка:[/bold red] Неверный формат. Используйте: task <agent> <задача>")
                    continue
                
                agent_name = parts[1]
                task = parts[2]
                await run_single_task(orchestrator, agent_name, task)
                continue
            
            if command.lower().startswith('orchestrate '):
                task = command.split(' ', 1)[1]
                await run_orchestrated_task(orchestrator, task)
                continue
            
            if command.lower().startswith('history '):
                agent_name = command.split(' ', 1)[1]
                try:
                    history = orchestrator.get_agent_history(agent_name)
                    if not history:
                        console.print(f"[yellow]История агента {agent_name} пуста[/yellow]")
                    else:
                        for i, entry in enumerate(history, 1):
                            console.print(f"\n[bold cyan]Запись {i}:[/bold cyan]")
                            console.print(f"Задача: {entry['task'][:100]}...")
                            console.print(f"Результат: {entry['result'][:200]}...")
                except Exception as e:
                    console.print(f"[bold red]Ошибка:[/bold red] {str(e)}")
                continue
            
            console.print("[bold red]Неизвестная команда.[/bold red] Введите 'help' для справки.")
            
        except KeyboardInterrupt:
            console.print("\n[bold yellow]До свидания![/bold yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Ошибка:[/bold red] {str(e)}")


async def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description="Оркестратор AI-агентов с Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--agent',
        type=str,
        help='Имя агента для выполнения задачи (researcher, analyzer, writer, coordinator)'
    )
    
    parser.add_argument(
        '--task',
        type=str,
        help='Задача для выполнения'
    )
    
    parser.add_argument(
        '--orchestrate',
        action='store_true',
        help='Использовать оркестрацию (несколько агентов)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='Показать список доступных агентов'
    )
    
    parser.add_argument(
        '--interactive',
        '-i',
        action='store_true',
        help='Запустить в интерактивном режиме'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='Директория для сохранения результатов'
    )
    
    parser.add_argument(
        '--save-session',
        type=str,
        help='Сохранить контекст сессии в файл'
    )
    
    parser.add_argument(
        '--load-session',
        type=str,
        help='Загрузить контекст сессии из файла'
    )
    
    parser.add_argument(
        '--file',
        '-f',
        type=str,
        help='Входной файл для анализа'
    )
    
    args = parser.parse_args()
    
    # Вывести баннер
    print_banner()
    
    try:
        # Инициализировать оркестратор
        orchestrator = AgentOrchestrator()
        
        # Загрузка сессии
        if args.load_session:
            orchestrator.load_session(args.load_session)
        
        # Список агентов
        if args.list:
            print_agents_table(orchestrator)
            return
        
        # Интерактивный режим
        if args.interactive or (not args.task and not args.agent):
            await interactive_mode(orchestrator)
            return
        
        # Проверка наличия задачи
        if not args.task:
            console.print("[bold red]Ошибка:[/bold red] Не указана задача. Используйте --task")
            sys.exit(1)
        
        # Оркестрация
        if args.orchestrate:
            await run_orchestrated_task(orchestrator, args.task, args.output)
            return
        
        # Выполнение задачи одним агентом
        if args.agent:
            await run_single_task(orchestrator, args.agent, args.task, args.output, args.file)
            return
        
        # По умолчанию - оркестрация
        await run_orchestrated_task(orchestrator, args.task, args.output)
        
        # Сохранение сессии
        if args.save_session:
            orchestrator.save_session(args.save_session)
        
    except Exception as e:
        console.print(f"\n[bold red]Критическая ошибка:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

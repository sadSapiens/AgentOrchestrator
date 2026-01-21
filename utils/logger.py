"""
Утилиты для логирования
"""
import logging
import sys
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler
from utils.config import Config

console = Console()


class Logger:
    """Класс для логирования событий оркестратора"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        
        # Настройка логгера
        self.logger = logging.getLogger("AgentOrchestrator")
        self.logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Rich handler для красивого вывода в консоль
        rich_handler = RichHandler(
            console=console,
            show_time=True,
            show_path=False,
            markup=True
        )
        rich_handler.setFormatter(
            logging.Formatter("%(message)s", datefmt="[%X]")
        )
        
        # File handler для записи в файл
        file_handler = logging.FileHandler(Config.LOG_FILE)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        
        self.logger.addHandler(rich_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str, **kwargs):
        """Логировать информационное сообщение"""
        self.logger.info(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Логировать ошибку"""
        self.logger.error(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Логировать предупреждение"""
        self.logger.warning(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Логировать отладочное сообщение"""
        self.logger.debug(message, **kwargs)
    
    def agent_action(self, agent_name: str, action: str, details: str = ""):
        """Логировать действие агента"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"[bold cyan]{agent_name}[/bold cyan] → {action}"
        if details:
            message += f": {details}"
        self.info(message)
    
    def task_start(self, task_name: str):
        """Логировать начало задачи"""
        console.rule(f"[bold green]Начало задачи: {task_name}[/bold green]")
    
    def task_end(self, task_name: str, success: bool = True):
        """Логировать завершение задачи"""
        status = "[bold green]✓ Успешно[/bold green]" if success else "[bold red]✗ Ошибка[/bold red]"
        console.rule(f"{status}: {task_name}")


# Глобальный экземпляр логгера
logger = Logger()

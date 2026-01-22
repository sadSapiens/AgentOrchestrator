import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from utils.logger import logger

def save_text_to_file(
    content: str, 
    filename: Optional[str] = None, 
    directory: str = "results",
    prefix: str = "result"
) -> str:
    """
    Сохранить текстовый контент в файл
    
    Args:
        content: Текст для сохранения
        filename: Имя файла (если не указано, будет сгенерировано имя с timestamp)
        directory: Директория для сохранения
        prefix: Префикс для сгенерированного имени файла
        
    Returns:
        Путь к сохраненному файлу
    """
    try:
        # Создаем директорию, если она не существует
        os.makedirs(directory, exist_ok=True)
        
        # Если имя файла не указано, генерируем его
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{prefix}_{timestamp}.md"
            
        # Формируем полный путь
        file_path = os.path.join(directory, filename)
        
        # Сохраняем файл
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        logger.info(f"[bold green]✓[/bold green] Результат сохранен в файл: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"[bold red]✗[/bold red] Ошибка при сохранении файла: {str(e)}")
        raise e

def read_file_content(filepath: str) -> str:
    """
    Прочитать содержимое текстового файла
    
    Args:
        filepath: Путь к файлу
        
    Returns:
        Содержимое файла
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        logger.info(f"📄 Прочитан файл: {filepath} ({len(content)} символов)")
        return content
        
    except Exception as e:
        logger.error(f"[bold red]✗[/bold red] Ошибка чтения файла {filepath}: {str(e)}")
        raise e

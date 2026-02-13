"""
Утилиты для конфигурации оркестратора агентов
"""

import os

from dotenv import load_dotenv

# Загрузить переменные окружения
load_dotenv()


class Config:
    """Класс конфигурации для оркестратора"""

    # Gemini API настройки
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))

    # Настройки логирования
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "orchestrator.log")

    @classmethod
    def validate(cls):
        """Проверить валидность конфигурации"""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY не установлен. "
                "Пожалуйста, установите его в .env файле или переменных окружения."
            )
        return True

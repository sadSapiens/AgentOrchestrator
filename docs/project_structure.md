# Структура проекта

```
AgentOrchestrator/
│
├── README.md                   # Основная документация проекта
├── QUICKSTART.md              # Руководство по быстрому старту
├── ARCHITECTURE.md            # Описание архитектуры системы
├── CLI_GUIDE.md               # Руководство по использованию CLI
├── PROJECT_STRUCTURE.md       # Этот файл
│
├── requirements.txt           # Зависимости Python
├── .env.example              # Пример файла конфигурации
├── .env                      # Файл конфигурации (не в git)
├── .gitignore               # Игнорируемые файлы
│
├── run.sh                    # Скрипт быстрого запуска
├── main.py                   # Точка входа CLI приложения
├── orchestrator.py           # Главный оркестратор агентов
├── examples.py               # Примеры использования
│
├── agents/                   # Пакет с агентами
│   ├── __init__.py          # Инициализация пакета
│   ├── base_agent.py        # Базовый класс для всех агентов
│   ├── researcher.py        # Агент-исследователь
│   ├── analyzer.py          # Агент-аналитик
│   ├── writer.py            # Агент-писатель
│   └── coordinator.py       # Агент-координатор
│
├── utils/                    # Утилиты
│   ├── __init__.py          # Инициализация пакета
│   ├── config.py            # Конфигурация приложения
│   └── logger.py            # Логирование
│
├── venv/                     # Виртуальное окружение (не в git)
│   └── ...
│
└── orchestrator.log          # Файл логов (не в git)
```

## Описание файлов

### Корневые файлы

#### `README.md`
Основная документация проекта, включающая:
- Описание проекта
- Возможности системы
- Инструкции по установке
- Примеры использования
- Структуру проекта

#### `QUICKSTART.md`
Руководство по быстрому старту:
- Получение API ключа
- Настройка проекта
- Первые шаги
- Примеры команд
- Решение проблем

#### `ARCHITECTURE.md`
Подробное описание архитектуры:
- Компоненты системы
- Поток данных
- Расширение системы
- Обработка ошибок
- Производительность

#### `CLI_GUIDE.md`
Полное руководство по CLI:
- Интерактивный режим
- Командная строка
- Параметры
- Примеры использования
- Автоматизация

#### `requirements.txt`
Список зависимостей Python:
```
google-generativeai>=0.3.0
python-dotenv>=1.0.0
colorama>=0.4.6
rich>=13.7.0
```

#### `.env.example`
Шаблон файла конфигурации:
```env
GEMINI_API_KEY=your-api-key-here
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.7
MAX_TOKENS=2048
```

#### `.gitignore`
Файлы, игнорируемые git:
- `.env` (содержит секреты)
- `venv/` (виртуальное окружение)
- `__pycache__/` (кэш Python)
- `*.log` (файлы логов)

### Исполняемые файлы

#### `run.sh`
Скрипт быстрого запуска:
- Проверка окружения
- Установка зависимостей
- Проверка API ключа
- Запуск приложения

**Использование:**
```bash
./run.sh                    # Интерактивный режим
./run.sh --list            # Список агентов
./run.sh --task "..."      # Выполнить задачу
```

#### `main.py`
Точка входа CLI приложения:
- Парсинг аргументов командной строки
- Интерактивный режим
- Форматирование вывода
- Обработка ошибок

**Основные функции:**
- `print_banner()` - вывод баннера
- `print_agents_table()` - таблица агентов
- `run_single_task()` - выполнение одиночной задачи
- `run_orchestrated_task()` - оркестрация
- `interactive_mode()` - интерактивный режим
- `main()` - главная функция

#### `orchestrator.py`
Главный оркестратор агентов:
- Управление агентами
- Выполнение задач
- Оркестрация workflow
- История выполнения

**Класс `AgentOrchestrator`:**
- `__init__()` - инициализация агентов
- `get_agent()` - получить агента по имени
- `execute_single_task()` - выполнить задачу одним агентом
- `orchestrate_task()` - оркестрация нескольких агентов
- `list_agents()` - список агентов
- `get_agent_history()` - история агента

#### `examples.py`
Примеры использования API:
- Использование одиночных агентов
- Оркестрация задач
- Работа с контекстом
- Получение истории

**Функции:**
- `example_single_agent()` - пример с Researcher
- `example_analyzer()` - пример с Analyzer
- `example_writer()` - пример с Writer
- `example_orchestration()` - пример оркестрации
- `example_list_agents()` - список агентов

### Пакет `agents/`

#### `base_agent.py`
Базовый класс для всех агентов:
- Интеграция с Gemini API
- Асинхронное выполнение
- История задач
- Управление контекстом

**Класс `BaseAgent`:**
- `__init__()` - инициализация
- `_create_prompt()` - создание промпта
- `execute()` - выполнение задачи
- `get_history()` - получить историю
- `get_capabilities()` - возможности (абстрактный)

#### `researcher.py`
Агент-исследователь:
- Сбор информации
- Поиск фактов
- Структурирование данных

**Класс `ResearcherAgent(BaseAgent)`:**
- Специализированный system prompt
- Формат вывода: резюме, факты, детали, выводы

#### `analyzer.py`
Агент-аналитик:
- Анализ данных
- Выявление паттернов
- Генерация инсайтов

**Класс `AnalyzerAgent(BaseAgent)`:**
- Специализированный system prompt
- Формат вывода: анализ, находки, тренды, рекомендации

#### `writer.py`
Агент-писатель:
- Создание контента
- Редактирование текстов
- Форматирование

**Класс `WriterAgent(BaseAgent)`:**
- Специализированный system prompt
- Формат вывода: заголовок, введение, основная часть, заключение

#### `coordinator.py`
Агент-координатор:
- Планирование задач
- Координация агентов
- Синтез результатов

**Класс `CoordinatorAgent(BaseAgent)`:**
- Специализированный system prompt
- Формат вывода: JSON с планом выполнения
- `parse_plan()` - парсинг плана

### Пакет `utils/`

#### `config.py`
Конфигурация приложения:
- Загрузка переменных окружения
- Валидация настроек
- Доступ к конфигурации

**Класс `Config`:**
- `GEMINI_API_KEY` - API ключ
- `MODEL_NAME` - название модели
- `TEMPERATURE` - температура генерации
- `MAX_TOKENS` - максимум токенов
- `LOG_LEVEL` - уровень логирования
- `LOG_FILE` - файл логов
- `validate()` - проверка конфигурации

#### `logger.py`
Система логирования:
- Консольный вывод (Rich)
- Файловое логирование
- Форматирование сообщений

**Класс `Logger`:**
- `info()` - информационное сообщение
- `error()` - ошибка
- `warning()` - предупреждение
- `debug()` - отладка
- `agent_action()` - действие агента
- `task_start()` - начало задачи
- `task_end()` - завершение задачи

## Потоки данных

### Одиночная задача
```
main.py
  ↓
orchestrator.py (execute_single_task)
  ↓
agents/researcher.py (execute)
  ↓
base_agent.py (_create_prompt, Gemini API)
  ↓
Результат
```

### Оркестрация
```
main.py
  ↓
orchestrator.py (orchestrate_task)
  ↓
agents/coordinator.py (создание плана)
  ↓
agents/researcher.py (шаг 1)
  ↓ контекст
agents/analyzer.py (шаг 2)
  ↓ контекст
agents/writer.py (шаг 3)
  ↓
Финальный результат
```

## Зависимости между модулями

```
main.py
  ├─→ orchestrator.py
  │     ├─→ agents/__init__.py
  │     │     ├─→ base_agent.py
  │     │     ├─→ researcher.py
  │     │     ├─→ analyzer.py
  │     │     ├─→ writer.py
  │     │     └─→ coordinator.py
  │     └─→ utils/__init__.py
  │           ├─→ config.py
  │           └─→ logger.py
  └─→ utils/logger.py

base_agent.py
  ├─→ google.generativeai
  ├─→ utils/config.py
  └─→ utils/logger.py
```

## Файлы конфигурации

### `.env` (создается пользователем)
```env
GEMINI_API_KEY=ваш-реальный-ключ
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.7
MAX_TOKENS=2048
LOG_LEVEL=INFO
LOG_FILE=orchestrator.log
```

### `orchestrator.log` (создается автоматически)
Содержит все логи выполнения:
```
2026-01-21 08:49:41 - AgentOrchestrator - INFO - ✓ Агент 'Researcher' инициализирован
2026-01-21 08:49:42 - AgentOrchestrator - INFO - Researcher → Начало выполнения
...
```

## Расширение проекта

### Добавление нового агента

1. Создать файл `agents/my_agent.py`:
```python
from agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MyAgent",
            role="Моя роль",
            system_prompt="Инструкции"
        )

    def get_capabilities(self):
        return {"cap": "описание"}
```

2. Добавить в `agents/__init__.py`:
```python
from .my_agent import MyAgent
__all__ = [..., 'MyAgent']
```

3. Зарегистрировать в `orchestrator.py`:
```python
self.agents = {
    ...,
    "myagent": MyAgent()
}
```

### Добавление новой утилиты

1. Создать файл `utils/my_util.py`
2. Добавить в `utils/__init__.py`
3. Использовать в других модулях

## Лицензия

MIT License - см. файл LICENSE (если создан)

## Контакты и поддержка

- GitHub Issues - для багов и предложений
- Документация - см. файлы *.md
- Примеры - см. examples.py

#!/bin/bash

# Скрипт быстрого запуска оркестратора агентов

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║           🤖 Agent Orchestrator с Gemini API 🤖           ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Виртуальное окружение не найдено. Создаю...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Виртуальное окружение создано${NC}"
fi

# Активация виртуального окружения
source venv/bin/activate

# Проверка зависимостей
if ! python -c "import google.generativeai" 2>/dev/null; then
    echo -e "${YELLOW}Устанавливаю зависимости...${NC}"
    pip install -r requirements.txt > /dev/null 2>&1
    echo -e "${GREEN}✓ Зависимости установлены${NC}"
fi

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Файл .env не найден${NC}"
    echo -e "${YELLOW}Создаю из .env.example...${NC}"
    cp .env.example .env
    echo -e "${RED}⚠ ВАЖНО: Отредактируйте .env и добавьте ваш GEMINI_API_KEY${NC}"
    echo -e "${YELLOW}Получить ключ можно здесь: https://makersuite.google.com/app/apikey${NC}"
    echo ""
    read -p "Нажмите Enter после добавления API ключа..."
fi

# Проверка API ключа
if ! grep -q "GEMINI_API_KEY=.*[a-zA-Z0-9]" .env; then
    echo -e "${RED}✗ API ключ не установлен в .env файле${NC}"
    echo -e "${YELLOW}Пожалуйста, отредактируйте .env и добавьте ваш GEMINI_API_KEY${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Все проверки пройдены${NC}"
echo ""

# Запуск приложения
if [ $# -eq 0 ]; then
    # Без аргументов - интерактивный режим
    python main.py --interactive
else
    # С аргументами - передать их в main.py
    python main.py "$@"
fi

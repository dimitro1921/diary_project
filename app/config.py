from dotenv import load_dotenv
import os

# 1. Завантажує змінні середовища з .env
load_dotenv()

# 2. Основні налаштування
BOT_TOKEN = os.getenv("BOT_TOKEN")                 # Telegram токен
DATABASE_URL = os.getenv("DATABASE_URL")           # Шлях до SQLite файлу
PROMPT_HOUR = int(os.getenv("PROMPT_HOUR", 21))    # Година для щоденного запиту
PROMPT_MINUTE = int(os.getenv("PROMPT_MINUTE", 0)) # Хвилина
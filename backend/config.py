import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./wedding.db")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID", "")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

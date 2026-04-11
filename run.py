#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

# Добавляем backend в path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.main import app
from backend.database import init_db
from backend.bot import start_bot_polling, stop_bot
from backend.config import HOST, PORT
import uvicorn


async def main():
    # Инициализация БД
    print("🗄️  Инициализация базы данных...")
    await init_db()
    print("✅ База данных готова!")
    
    # Запуск бота в фоне
    print("🤖 Запуск Telegram бота...")
    bot_task = asyncio.create_task(start_bot_polling())
    
    # Запуск сервера
    print(f"🚀 Запуск сервера на {HOST}:{PORT}")
    print(f"📖 Документация API: http://{HOST}:{PORT}/docs")
    print(f"💍 Сайт: откройте wedding-invitation.html в браузере")
    print("\n⚠️  Нажмите Ctrl+C для остановки\n")
    
    config = uvicorn.Config(app, host=HOST, port=PORT, log_level="info")
    server = uvicorn.Server(config)
    
    try:
        await server.serve()
    except KeyboardInterrupt:
        print("\n🛑 Остановка сервера...")
    finally:
        await stop_bot()
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Пока!")

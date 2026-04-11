import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_CHAT_ID
from database import async_session_maker
from crud import get_all_guests, get_stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализируем бота только если токен предоставлен
bot = None
dp = None

if TELEGRAM_BOT_TOKEN and TELEGRAM_ADMIN_CHAT_ID:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    
    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        """Обработчик команды /start"""
        if str(message.chat.id) != str(TELEGRAM_ADMIN_CHAT_ID):
            await message.answer("У вас нет доступа к этому боту.")
            return
        
        await message.answer(
            "👋 Привет! Я бот для управления гостями свадьбы Антона и Вероники.\n\n"
            "Доступные команды:\n"
            "/guests - список всех гостей\n"
            "/stats - статистика по гостям\n"
            "/help - помощь"
        )

    @dp.message(Command("guests"))
    async def cmd_guests(message: Message):
        """Показывает список всех гостей"""
        if str(message.chat.id) != str(TELEGRAM_ADMIN_CHAT_ID):
            await message.answer("У вас нет доступа к этому боту.")
            return
        
        async with async_session_maker() as session:
            guests = await get_all_guests(session)
        
        if not guests:
            await message.answer("📭 Пока нет ни одного гостя в списке.")
            return
        
        text = "📋 <b>Список гостей:</b>\n\n"
        for i, guest in enumerate(guests, 1):
            status = "✅" if guest.will_attend else "❌"
            drinks = f"\n   🍷 {guest.drink_preference}" if guest.drink_preference else ""
            text += f"{i}. {status} <b>{guest.name}</b>{drinks}\n"
        
        for chunk in [text[i:i+4000] for i in range(0, len(text), 4000)]:
            await message.answer(chunk, parse_mode="HTML")

    @dp.message(Command("stats"))
    async def cmd_stats(message: Message):
        """Показывает статистику по гостям"""
        if str(message.chat.id) != str(TELEGRAM_ADMIN_CHAT_ID):
            await message.answer("У вас нет доступа к этому боту.")
            return
        
        async with async_session_maker() as session:
            stats = await get_stats(session)
        
        text = (
            "📊 <b>Статистика гостей:</b>\n\n"
            f"👥 Всего ответов: {stats['total_guests']}\n"
            f"✅ Придут: {stats['attending']}\n"
            f"❌ Не придут: {stats['not_attending']}"
        )
        
        await message.answer(text, parse_mode="HTML")

    @dp.message(Command("help"))
    async def cmd_help(message: Message):
        """Показывает справку"""
        if str(message.chat.id) != str(TELEGRAM_ADMIN_CHAT_ID):
            await message.answer("У вас нет доступа к этому боту.")
            return
        
        await message.answer(
            "📖 <b>Помощь</b>\n\n"
            "Я умею:\n"
            "• Уведомлять о новых ответах гостей\n"
            "• Показывать полный список гостей (/guests)\n"
            "• Показывать статистику (/stats)\n\n"
            "Все данные хранятся в базе данных и доступны через этот бот."
        )
else:
    logger.warning("Telegram bot not configured - set TELEGRAM_BOT_TOKEN and TELEGRAM_ADMIN_CHAT_ID in .env")


async def send_new_guest_notification(guest_name: str, will_attend: bool, drink_preference: str | None):
    """Отправляет уведомление о новом госте в админ чат"""
    if not bot or not TELEGRAM_ADMIN_CHAT_ID:
        logger.info(f"New guest (notification skipped): {guest_name}, attending={will_attend}")
        return
    
    status = "✅ Придет" if will_attend else "❌ Не придет"
    drinks = f"\n🍷 Напитки: {drink_preference}" if drink_preference else ""
    
    message = (
        f"🆕 <b>Новый ответ от гостя!</b>\n\n"
        f"👤 <b>Имя:</b> {guest_name}\n"
        f"📅 <b>Статус:</b> {status}{drinks}"
    )
    
    try:
        await bot.send_message(chat_id=int(TELEGRAM_ADMIN_CHAT_ID), text=message, parse_mode="HTML")
        logger.info(f"Notification sent for guest: {guest_name}")
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")


async def start_bot_polling():
    """Запускает бота в режиме polling"""
    if not bot or not dp:
        logger.warning("Telegram bot not configured, skipping polling")
        return
    
    logger.info("Starting Telegram bot polling...")
    await dp.start_polling(bot)


async def stop_bot():
    """Останавливает бота"""
    if bot:
        await bot.session.close()

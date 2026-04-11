import os
import telebot
import requests
from telebot import types

# Конфигурация
BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', '')
API_URL = os.environ.get('BACKEND_URL', 'http://backend:5000')
API_SECRET = os.environ.get('API_SECRET', 'secret')

bot = telebot.TeleBot(BOT_TOKEN)

# Создание основной клавиатуры
def create_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_stats = types.KeyboardButton('📊 Статистика')
    btn_list = types.KeyboardButton('📋 Список гостей')
    btn_help = types.KeyboardButton('📖 Помощь')
    keyboard.add(btn_stats, btn_list, btn_help)
    return keyboard

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🎉 <b>Бот свадебного приглашения Антона и Вероники!</b>

Доступные команды:
/stats - Статистика по гостям
/list - Список всех гостей
/help - Помощь

С любовью, Антон и Вероника 💚
    """
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=create_main_keyboard())

# Команда /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
<b>Доступные команды:</b>

/stats - Показать статистику ответов
• Общее количество ответов
• Сколько подтвердили присутствие
• Кто не сможет прийти

/list - Показать список всех гостей
• Имена гостей
• Статус присутствия
• Предпочтения по напиткам

/start - Главное меню
    """
    bot.send_message(message.chat.id, help_text, parse_mode='HTML', reply_markup=create_main_keyboard())

# Команда /stats
@bot.message_handler(commands=['stats'])
def send_stats(message):
    try:
        response = requests.get(
            f'{API_URL}/api/stats',
            headers={'Authorization': f'Bearer {API_SECRET}'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            stats_text = f"""
📊 <b>Статистика гостей</b>

👥 Всего ответов: {data['total']}
✅ Подтвердили: {data['attending_yes']}
❌ Не смогут: {data['attending_no']}
            """
            bot.send_message(message.chat.id, stats_text, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'Ошибка получения статистики')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {str(e)}')

# Команда /list
@bot.message_handler(commands=['list'])
def send_guest_list(message):
    try:
        response = requests.get(
            f'{API_URL}/api/guests',
            headers={'Authorization': f'Bearer {API_SECRET}'},
            timeout=10
        )
        
        if response.status_code == 200:
            guests = response.json()
            
            if not guests:
                bot.send_message(message.chat.id, 'Пока нет ответов от гостей')
                return
            
            # Разбиваем на сообщения по 10 гостей (ограничение Telegram)
            batch_size = 10
            for i in range(0, len(guests), batch_size):
                batch = guests[i:i+batch_size]
                list_text = f"<b>Гости ({i+1}-{min(i+batch_size, len(guests))} из {len(guests)})</b>\n\n"
                
                for guest in batch:
                    status = "✅" if guest['attending'] == 'yes' else "❌"
                    drinks = guest.get('drinks_preference', 'Не указано')
                    if not drinks:
                        drinks = 'Не указано'
                    
                    list_text += f"{status} <b>{guest['name']}</b>\n"
                    list_text += f"   🍷 Напитки: {drinks}\n\n"
                
                bot.send_message(message.chat.id, list_text, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'Ошибка получения списка гостей')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {str(e)}')

# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == '📊 Статистика':
        send_stats(message)
    elif message.text == '📋 Список гостей':
        send_guest_list(message)
    elif message.text == '📖 Помощь':
        send_help(message)
    else:
        bot.send_message(
            message.chat.id, 
            'Используйте команды:\n/stats - статистика\n/list - список гостей\n/help - помощь',
            parse_mode='HTML',
            reply_markup=create_main_keyboard()
        )

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()

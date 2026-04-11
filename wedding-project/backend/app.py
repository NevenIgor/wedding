from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Конфигурация
DB_PATH = os.environ.get('DB_PATH', '/data/wedding.db')
TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', '')
TG_USER_IDS = os.environ.get('TG_USER_IDS', '').split(',') if os.environ.get('TG_USER_IDS') else []

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            attending TEXT NOT NULL,
            drinks_preference TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Получение соединения с БД"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def send_telegram_notification(guest_data):
    """Отправка уведомления в Telegram всем пользователям из списка"""
    if not TG_BOT_TOKEN or not TG_USER_IDS:
        print("Telegram не настроен")
        return
    
    message = f"""
🎉 <b>Новый ответ на приглашение!</b>

👤 <b>Имя:</b> {guest_data['name']}
✅ <b>Присутствие:</b> {guest_data['attending']}
🍷 <b>Напитки:</b> {guest_data.get('drinks_preference', 'Не указано')}
⏰ <b>Время:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
    """
    
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    
    # Отправляем уведомление каждому пользователю из списка
    for user_id in TG_USER_IDS:
        user_id = user_id.strip()
        if not user_id:
            continue
            
        data = {
            'chat_id': user_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            if response.status_code != 200:
                print(f"Ошибка отправки в Telegram для пользователя {user_id}: {response.text}")
            else:
                print(f"Уведомление отправлено пользователю {user_id}")
        except Exception as e:
            print(f"Ошибка подключения к Telegram для пользователя {user_id}: {e}")

@app.route('/api/rsvp', methods=['POST'])
def submit_rsvp():
    """Обработка подтверждения присутствия"""
    data = request.json
    
    if not data or 'name' not in data or 'attending' not in data:
        return jsonify({'error': 'Некорректные данные'}), 400
    
    name = data['name'].strip()
    attending = data['attending']
    drinks = data.get('drinks_preference', '').strip()
    
    if not name or len(name) < 2:
        return jsonify({'error': 'Имя должно содержать минимум 2 символа'}), 400
    
    if attending not in ['yes', 'no']:
        return jsonify({'error': 'Некорректный статус присутствия'}), 400
    
    # Сохранение в БД
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO guests (name, attending, drinks_preference)
        VALUES (?, ?, ?)
    ''', (name, attending, drinks))
    
    guest_id = cursor.lastrowid
    conn.commit()
    
    guest_data = {
        'id': guest_id,
        'name': name,
        'attending': attending,
        'drinks_preference': drinks
    }
    
    conn.close()
    
    # Отправка уведомления в Telegram
    send_telegram_notification(guest_data)
    
    return jsonify({
        'success': True,
        'message': 'Спасибо! Ваш ответ записан.',
        'guest_id': guest_id
    })

@app.route('/api/guests', methods=['GET'])
def get_guests():
    """Получение списка гостей (для бота)"""
    auth_header = request.headers.get('Authorization')
    if auth_header != f"Bearer {os.environ.get('API_SECRET', 'secret')}":
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM guests ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    guests = []
    for row in rows:
        guests.append({
            'id': row['id'],
            'name': row['name'],
            'attending': row['attending'],
            'drinks_preference': row['drinks_preference'],
            'created_at': row['created_at']
        })
    
    return jsonify(guests)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Получение статистики (для бота)"""
    auth_header = request.headers.get('Authorization')
    if auth_header != f"Bearer {os.environ.get('API_SECRET', 'secret')}":
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM guests')
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM guests WHERE attending = 'yes'")
    yes_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM guests WHERE attending = 'no'")
    no_count = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total': total,
        'attending_yes': yes_count,
        'attending_no': no_count
    })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)

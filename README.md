# 🍃 Свадебное приглашение - Антон и Вероника

Сайт-приглашение на свадьбу с backend, базой данных и Telegram ботом.

## 📁 Структура проекта

```
/workspace
├── wedding-invitation.html    # Фронтенд (сайт)
├── run.py                     # Скрипт запуска
├── requirements.txt           # Зависимости
├── .env.example              # Пример конфигурации
└── backend/
    ├── main.py               # FastAPI приложение
    ├── config.py             # Конфигурация
    ├── database.py           # Подключение к БД
    ├── models.py             # Модели данных
    ├── schemas.py            # Pydantic схемы
    ├── crud.py               # Операции с БД
    └── bot.py                # Telegram бот
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` и укажите:
- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота
- `TELEGRAM_ADMIN_CHAT_ID` - ваш ID в Telegram

### 3. Получение токена Telegram бота

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте полученный токен в `.env`

### 4. Узнавание своего Chat ID

1. Откройте [@userinfobot](https://t.me/userinfobot)
2. Он отправит вам ваш ID
3. Скопируйте его в `.env`

### 5. Запуск

```bash
python run.py
```

Сервер запустится на `http://localhost:8000`

## 📖 API Endpoints

- `GET /` - Главная страница API
- `POST /api/guests` - Добавить гостя
- `GET /api/guests` - Список всех гостей
- `GET /api/guests/{id}` - Информация о госте
- `DELETE /api/guests/{id}` - Удалить гостя
- `GET /api/stats` - Статистика
- `GET /docs` - Swagger документация

## 🤖 Telegram бот

### Команды:

- `/start` - Приветствие и помощь
- `/guests` - Список всех гостей
- `/stats` - Статистика по гостям
- `/help` - Справка

### Уведомления:

Бот автоматически отправляет уведомления в админ-чат при каждом новом ответе гостя.

## 🌐 Как это работает

1. Гость заполняет форму на сайте
2. Данные отправляются на backend (FastAPI)
3. Backend сохраняет данные в SQLite базу
4. Backend отправляет уведомление в Telegram
5. Вы можете посмотреть статистику и список гостей через бота

## 🔧 Настройка для продакшена

### 1. Измените API_URL в wedding-invitation.html

```javascript
const API_URL = 'https://your-domain.com/api';
```

### 2. Используйте PostgreSQL вместо SQLite

В `.env`:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/wedding_db
```

Добавьте в `requirements.txt`:
```
asyncpg==0.29.0
```

### 3. Настройте CORS

В `backend/main.py` измените `allow_origins` на ваш домен.

## 📱 Мобильная версия

Сайт полностью адаптивен и отлично смотрится на мобильных устройствах.

## 🎨 Кастомизация

Вы можете легко изменить:
- Цветовую гамму (CSS переменные в `<style>`)
- Тексты и разделы
- Шрифты
- Добавить фото места проведения

## 🛠️ Технологии

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Database:** SQLite (или PostgreSQL)
- **Bot:** aiogram 3.x
- **Server:** Uvicorn

## 📝 Лицензия

Используйте для любых личных целей!

---

**С любовью, для Антона и Вероники 💚**

# 🎉 Свадебное приглашение - Docker проект

## Структура проекта

```
wedding-project/
├── backend/          # Flask API для обработки RSVP
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── bot/              # Telegram бот
│   ├── bot.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # HTML сайт
│   └── index.html
├── nginx.conf        # Конфигурация Nginx
├── docker-compose.yml
├── .env.example      # Шаблон переменных окружения
└── README.md         # Этот файл
```

## Быстрый старт

### 1. Настройка Telegram бота

1. Создайте бота через [@BotFather](https://t.me/BotFather):
   - Отправьте `/newbot`
   - Придумайте имя и username
   - Сохраните полученный токен

2. Узнайте свой User ID:
   - Напишите боту [@userinfobot](https://t.me/userinfobot) или любому другому сервису определения ID
   - Или отправьте сообщение своему боту и перейдите по ссылке: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Найдите `"from":{"id": ...}` - это ваш User ID
   - Для нескольких пользователей укажите их через запятую (например: 123456789,987654321)

### 2. Конфигурация

```bash
# Скопируйте шаблон переменных окружения
cp .env.example .env

# Отредактируйте .env файл
nano .env
```

Заполните:
- `TG_BOT_TOKEN` - токен вашего бота
- `TG_USER_IDS` - список User ID пользователей через запятую (например: 123456789,987654321)

### 3. Запуск

```bash
# Запуск всех сервисов
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

## Доступные сервисы

| Сервис | Порт | Описание |
|--------|------|----------|
| Frontend | http://localhost:80 | Сайт приглашения |
| Backend API | http://localhost:5000 | API для формы RSVP |
| Telegram Bot | - | Уведомления и статистика |

## Использование Telegram бота

После запуска бот будет доступен по username, который вы задали при создании.

### Команды бота:

- `/start` - Главное меню
- `/stats` - Статистика ответов гостей
- `/list` - Список всех гостей с деталями
- `/help` - Справка по командам

### Примеры уведомлений

При каждом новом ответе через форму на сайте, бот отправит уведомление:

```
🎉 Новый ответ на приглашение!

👤 Имя: Иван Иванов
✅ Присутствие: yes
🍷 Напитки: Шампанское, вино
⏰ Время: 05.09.2026 14:30
```

## API Endpoints

### POST /api/rsvp
Отправка подтверждения присутствия

```json
{
  "name": "Иван Иванов",
  "attending": "yes",
  "drinks_preference": "Шампанское"
}
```

### GET /api/guests
Получение списка гостей (требуется авторизация)

### GET /api/stats
Получение статистики (требуется авторизация)

## База данных

SQLite база хранится в Docker volume `backend_data` и содержит таблицу:

```sql
CREATE TABLE guests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    attending TEXT NOT NULL,
    drinks_preference TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Резервное копирование БД

```bash
# Копирование БД из контейнера
docker cp wedding-backend:/data/wedding.db ./backup.db
```

## Модификация сайта

### Изменение цветов
В `frontend/index.html` найдите секцию `:root` и измените цвета:

```css
:root {
    --dark-green: #2d5043;
    --medium-green: #4a7c6a;
    /* и т.д. */
}
```

### Добавление фото
Замените блоки `.image-placeholder` на реальные изображения:

```html
<img src="photo1.jpg" alt="Место торжества" style="width:100%; border-radius:10px;">
```

### Изменение текста
Просто отредактируйте текст в `frontend/index.html`

## Развёртывание на сервере

1. Загрузите файлы на сервер
2. Настройте `.env`
3. Запустите: `docker-compose up -d --build`
4. Настройте домен (опционально)

### Настройка домена

Измените `nginx.conf`:
```
server_name yourdomain.com www.yourdomain.com;
```

Используйте Certbot для HTTPS:
```bash
docker run --rm -v $(pwd)/frontend:/var/www/html certbot/certbot certonly --webroot
```

## Решение проблем

### Бот не отправляет уведомления
- Проверьте правильность токена в `.env`
- Убедитесь, что бот добавлен в чат
- Проверьте логи: `docker-compose logs bot`

### Форма не отправляет данные
- Проверьте доступность backend: `curl http://localhost:5000/api/stats`
- Посмотрите логи: `docker-compose logs backend`

### Ошибки портов
Если порт 80 занят, измените в `docker-compose.yml`:
```yaml
ports:
  - "8080:80"  # Вместо 80:80
```

## Безопасность

- Измените `API_SECRET` на уникальное значение
- Не коммитьте `.env` файл в git
- Используйте HTTPS в продакшене

---

С любовью, Антон и Вероника 💚

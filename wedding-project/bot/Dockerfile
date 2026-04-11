FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование бота
COPY bot.py .

EXPOSE 8080

CMD ["python", "bot.py"]

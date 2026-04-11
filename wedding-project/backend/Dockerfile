FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY app.py .

# Создание директории для данных
RUN mkdir -p /data

# Переменная окружения для пути к БД
ENV DB_PATH=/data/wedding.db

EXPOSE 5000

CMD ["python", "app.py"]

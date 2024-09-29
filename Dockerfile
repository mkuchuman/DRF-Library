# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект в рабочую директорию
COPY . /app/

# Открываем порт 8000 для приложения Django
EXPOSE 8000

# Команда для запуска приложения Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

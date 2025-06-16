# syntax=docker/dockerfile:1

# Базовый образ с Python 3.10 на Debian slim
FROM python:3.10-slim

# Установим системные зависимости:
#  - build-essential, gcc  — для сборки некоторых Python-модулей
#  - libpq-dev           — клиентская библиотека PostgreSQL (libpq >= 10)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Не будем генерировать .pyc-файлы и сделаем вывод немедленным
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Создаём рабочую директорию и копируем зависимости
WORKDIR /app
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости Python
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Копируем весь код приложения
COPY . .

# Открываем порт для Uvicorn
EXPOSE 5050

# Запуск сервера в режиме авто-перезагрузки при изменениях кода
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5050", "--reload"]

# fullstack/bookshop/Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Подготовка для сборки psycopg2 и добавление bash
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      bash \
 && rm -rf /var/lib/apt/lists/*

# 2. Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Копируем код
COPY . .

# 4. Запускаем Django сервер (с fallback на Flask)
EXPOSE 8000
WORKDIR /app/bookshop

# Создаём скрипт запуска с fallback
RUN echo '#!/bin/bash\n\
echo "🚀 Attempting to start Django..."\n\
python manage.py collectstatic --noinput --clear || echo "⚠️ Static files collection failed"\n\
python manage.py migrate --noinput || echo "⚠️ Migration failed"\n\
if python manage.py check --deploy; then\n\
    echo "✅ Django checks passed, starting Django server..."\n\
    python manage.py runserver 0.0.0.0:8000\n\
else\n\
    echo "❌ Django checks failed, falling back to Flask..."\n\
    cd /app\n\
    python simple_app.py\n\
fi' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
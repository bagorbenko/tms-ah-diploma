import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

# Добавляем проверку для тестового окружения
if "test" in DATABASE_URL.lower() or "memory" in DATABASE_URL.lower():
    engine = create_engine(DATABASE_URL, echo=False)
else:
    engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

# Функция для создания таблиц (используется в main.py)
def create_tables():
    """Создает таблицы в базе данных"""
    # Импортируем модели, чтобы они были зарегистрированы
    from app import models
    Base.metadata.create_all(bind=engine)


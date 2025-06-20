import os
from dotenv import load_dotenv

load_dotenv()  # автоматически подгрузит .env из ./app

# 1) Сначала пробуем взять готовый URL (например, sqlite:///:memory:)
DATABASE_URL = os.getenv("DATABASE_URL")

# 2) Если он не задан — строим Postgres-строку из DB_*
if not DATABASE_URL:
    db_user = os.getenv("DB_USER", "")
    db_pass = os.getenv("DB_PASS", "")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "")
    DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

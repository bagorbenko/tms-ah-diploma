# api-store/app/config.py
from dotenv import load_dotenv
import os

load_dotenv()  # автоматически найдёт ./app/.env

# читаем из отдельных переменных
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# собираем полную строку подключения
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Если вы предпочитаете сразу давать DATABASE_URL в .env,
# можно вместо этого просто:
# DATABASE_URL = os.getenv("DATABASE_URL")

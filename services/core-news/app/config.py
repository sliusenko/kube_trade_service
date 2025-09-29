import os
from sqlalchemy.ext.asyncio import create_async_engine

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "trade"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "postgres"),
    "port": os.getenv("DB_PORT", 5432),
}

AUTH_CRYPTONEW_TOKEN = os.getenv("AUTH_CRYPTONEW_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "1"))

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)

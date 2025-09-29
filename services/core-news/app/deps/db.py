# app/deps/db.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "trade"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "postgres"),
    "port": os.getenv("DB_PORT", 5432),
}

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

async def init_db():
    # Import models here to register them with Base
    from app.models.news_sentiment import NewsSentiment
    from app.models.price_history import PriceHistory
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

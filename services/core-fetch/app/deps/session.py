from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.deps.config import settings
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT','5432')}/{os.getenv('POSTGRES_DB')}"
)

engine = create_async_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


engine = create_async_engine(settings.POSTGRES_DSN, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

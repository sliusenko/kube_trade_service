from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core_fetch.utils.config import settings

engine = create_async_engine(settings.POSTGRES_DSN, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

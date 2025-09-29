from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.deps.config import settings

engine = create_async_engine(settings.POSTGRES_DSN, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

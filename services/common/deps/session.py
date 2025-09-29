from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from common.deps.config import settings

# Create async engine
engine = create_async_engine(
    settings.POSTGRES_DSN,
    echo=False,        # enable SQL logging if needed
    future=True,
    pool_pre_ping=True # keep-alive check
)

# Session factory
SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Dependency for FastAPI routes
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

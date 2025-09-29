from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from common.deps.config import settings

# Create async engine
engine = create_async_engine(
    settings.POSTGRES_DSN,
    echo=False,         # enable SQL logging if needed
    future=True,
    pool_pre_ping=True  # keep-alive check
)

# Session factory
AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Dependency for FastAPI
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

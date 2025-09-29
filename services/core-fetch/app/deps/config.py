import os

class Settings:
    # Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "app_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "trade")

    @property
    def POSTGRES_DSN(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Tables
    EXCHANGES_TABLE: str = os.getenv("EXCHANGES_TABLE", "exchanges")

    # Default fetch interval (fallback)
    FETCH_INTERVAL_DEFAULT: int = int(os.getenv("FETCH_INTERVAL_DEFAULT", "3600"))

    # Global price history fetch interval (applies to all exchanges/symbols)
    FETCH_PRICE_INTERVAL_MIN: int = int(os.getenv("FETCH_PRICE_INTERVAL_MIN", "10"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

settings = Settings()

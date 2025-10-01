import os


class Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "app_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "trade")

    # ⚡ нове поле для core-news (alias для NewsAPI)
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY")

    FETCH_PRICE_INTERVAL_MIN: int = int(os.getenv("FETCH_PRICE_INTERVAL_MIN", "10"))
    UPDATE_NEWS_PRICES_INTERVAL_HOURS: int = int(os.getenv("UPDATE_NEWS_PRICES_INTERVAL_HOURS", "10"))

    @property
    def POSTGRES_DSN(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()

import os

class BaseSettings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "app_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "trade")

    @property
    def POSTGRES_DSN(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = BaseSettings()

class CoreNewsSettings(BaseSettings):
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY")
    UPDATE_NEWS_PRICES_INTERVAL_HOURS: int = int(
        os.getenv("UPDATE_NEWS_PRICES_INTERVAL_HOURS", "10")
    )

class CoreAdminSettings(BaseSettings):
    ADMIN_DEFAULT_USER: str = os.getenv("ADMIN_DEFAULT_USER", "admin")
    ADMIN_DEFAULT_PASSWORD: str = os.getenv("ADMIN_DEFAULT_PASSWORD", "admin")
    ENABLE_SIGNUP: bool = os.getenv("ENABLE_SIGNUP", "false").lower() == "true"
    DASHBOARD_BASE_URL: str = os.getenv("DASHBOARD_BASE_URL", "http://kube-trade-bot-core-board:8000")
    NEWS_BASE_URL: str = os.getenv("NEWS_BASE_URL", "http://kube-trade-bot-core-news:8000")
    CONFIG_BASE_URL: str = os.getenv("CONFIG_BASE_URL", "http://kube-trade-bot-core-config:8000")


class CoreBoardSettings(BaseSettings):
    FETCH_PRICE_INTERVAL_MIN: int = int(os.getenv("FETCH_PRICE_INTERVAL_MIN", "10"))

class CoreFetchSettings(BaseSettings):
    FETCH_PRICE_INTERVAL_MIN: int = int(os.getenv("FETCH_PRICE_INTERVAL_MIN", "10"))

class CoreConfigSettings(BaseSettings):
    FETCH_PRICE_INTERVAL_MIN: int = int(os.getenv("FETCH_PRICE_INTERVAL_MIN", "10"))
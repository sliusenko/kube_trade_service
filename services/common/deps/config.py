import os, json
from typing import Optional, Set, Dict

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

    def dict(self) -> dict:
        data = {}
        for name in dir(self.__class__):
            if name.isupper():
                data[name] = getattr(self, name)
        for name, val in self.__dict__.items():
            if name.isupper():
                data[name] = val
        return data

settings = BaseSettings()

class CoreNewsSettings(BaseSettings):
    NEWSAPI_KEY: Optional[str] = os.getenv("NEWSAPI_KEY")
    NEWS_ENDPOINT: str = os.getenv("NEWS_ENDPOINT", "https://newsapi.org/v2/everything")

    UPDATE_NEWS_PRICES_INTERVAL_HOURS: int = int(os.getenv("UPDATE_NEWS_PRICES_INTERVAL_HOURS") or "4")
    FETCH_NEWS_INTERVAL_MIN: int = int(os.getenv("FETCH_NEWS_INTERVAL_MIN") or "15")

    NEWS_PARAMS: Dict = json.loads(os.getenv("NEWS_PARAMS", """
    {
        "q": "bitcoin OR ethereum OR binance OR sec OR hack",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10
    }
    """))
    NEWS_QUERY: str = os.getenv("NEWS_QUERY", "bitcoin OR ethereum OR binance OR sec OR hack")

    KEYWORD_TO_SYMBOL: Dict = json.loads(os.getenv("KEYWORD_TO_SYMBOL", """
    {
        "bitcoin": "BTC",
        "btc": "BTC",
        "solana": "SOL",
        "ethereum": "ETH",
        "eth": "ETH",
        "cardano": "ADA",
        "xrp": "XRP",
        "celrusdt": "CELR",
        "binance": "BNB",
        "bnb": "BNB",
        "sec": "BTC",
        "hack": null
    }
    """))

    DEFAULT_HALT_THRESHOLD: float = float(os.getenv("DEFAULT_HALT_THRESHOLD") or "-0.8")

    WHITELIST_SOURCES: Set[str] = set(json.loads(os.getenv("WHITELIST_SOURCES", """
    ["CoinDesk", "Cointelegraph", "Decrypt", "Bloomberg"]
    """)))

    BLACKLIST_SOURCES: Set[str] = set(json.loads(os.getenv("BLACKLIST_SOURCES", """
    ["reddit.com"]
    """)))

    SOURCE_WEIGHTS: Dict[str, float] = json.loads(os.getenv("SOURCE_WEIGHTS", """
    {
        "The Daily Caller": 1.0,
        "Newsweek": 0.95,
        "Financial Post": 0.9,
        "Tom's Hardware UK": 0.6,
        "ETF Daily News": 0.65,
        "Pypi.org": 0.7,
        "Coinjournal.net": 0.55,
        "Cryptoslate": 0.6,
        "Bitcoinist": 0.65,
        "Bleeding Cool News": 0.3,
        "CoinDesk": 0.7,
        "Cointelegraph": 0.7,
        "Decrypt": 0.7,
        "Bloomberg": 0.85,
        "default": 0.5
    }
    """))
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
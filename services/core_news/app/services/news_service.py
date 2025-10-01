import logging
import httpx
from datetime import datetime, timezone, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from common.models.markethistory import NewsSentiment, PriceHistory
from common.deps.config import settings

log = logging.getLogger(__name__)

# NewsAPI endpoint
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_PARAMS = {
    "q": "bitcoin OR ethereum OR binance OR sec OR hack",
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 10,
}

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Blacklist sources
BLACKLIST_SOURCES = {"reddit.com"}

# Default source weights
SOURCE_WEIGHTS = {
    "CoinDesk": 0.7,
    "Cointelegraph": 0.7,
    "Decrypt": 0.7,
    "Bloomberg": 0.85,
    "default": 0.5,
}


def _parse_ts(ts_str: str):
    """Convert ISO8601 string from NewsAPI to timezone-aware datetime."""
    if not ts_str:
        return None
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00")).astimezone(timezone.utc)


async def fetch_latest_news() -> list[dict]:
    """Fetch latest news from NewsAPI."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                NEWS_ENDPOINT,
                params=NEWS_PARAMS,
                headers={"X-Api-Key": settings.NEWSAPI_KEY},  # ✅ key у заголовку
            )
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])

        return [
            {
                "title": a.get("title", "") or "",
                "summary": a.get("description", "") or "",
                "published_at": _parse_ts(a.get("publishedAt")),
                "url": a.get("url", "") or "",
                "source": (a.get("source") or {}).get("name", "") or "",
            }
            for a in articles
            if (a.get("source") or {}).get("name", "") not in BLACKLIST_SOURCES
        ]

    except httpx.HTTPStatusError as e:
        log.error("❌ NewsAPI HTTP %s: %s", e.response.status_code, e.response.text[:400])
    except Exception:
        log.exception("❌ Error fetching news")
    return []


async def save_news_to_db(news_items: list[dict], session: AsyncSession):
    """Insert news into DB if not already present."""
    inserted_count = 0

    for news in news_items:
        if not news.get("published_at") or not news.get("title"):
            log.debug("⚠️ Skipped news due to missing fields: %s", news)
            continue

        # Перевірка на дублі (по published_at + title)
        q = select(NewsSentiment).where(
            NewsSentiment.published_at == news["published_at"],
            NewsSentiment.title == news["title"][:500],
        )
        existing = (await session.execute(q)).scalar_one_or_none()
        if existing:
            continue

        # Sentiment analysis
        text = f"{news['title']} {news.get('summary', '')}"
        score = analyzer.polarity_scores(text)

        db_news = NewsSentiment(
            published_at=news["published_at"],
            title=news["title"][:500],
            summary=news.get("summary", "")[:1000],
            sentiment=score["compound"],
            source=news.get("source", "newsapi"),
            symbol=news.get("symbol", None),
            url=news.get("url", ""),
        )

        session.add(db_news)
        inserted_count += 1

    await session.commit()
    log.info(f"✅ Inserted {inserted_count} news into DB")


async def check_news_and_halt_trading(session: AsyncSession):
    """Scheduled job: fetch news and save them to DB."""
    news = await fetch_latest_news()
    if news:
        await save_news_to_db(news, session)


async def update_news_prices(session: AsyncSession):
    """Fill price_before/after fields for news."""
    q = (
        select(NewsSentiment)
        .where(NewsSentiment.price_before.is_(None))
        .where(NewsSentiment.symbol.is_not(None))  # тільки новини з символом
        .limit(500)
    )
    news_items = (await session.execute(q)).scalars().all()

    for news in news_items:
        price_before = await get_price_at(session, news.symbol, news.published_at, 0)
        price_1h = await get_price_at(session, news.symbol, news.published_at, 60)
        price_6h = await get_price_at(session, news.symbol, news.published_at, 360)
        price_24h = await get_price_at(session, news.symbol, news.published_at, 1440)

        news.price_before = price_before
        news.price_after_1h = price_1h
        news.price_after_6h = price_6h
        news.price_after_24h = price_24h

        if price_before and price_1h:
            news.price_change_1h = round(100 * (float(price_1h) - float(price_before)) / float(price_before), 2)
        if price_before and price_6h:
            news.price_change_6h = round(100 * (float(price_6h) - float(price_before)) / float(price_before), 2)
        if price_before and price_24h:
            news.price_change_24h = round(100 * (float(price_24h) - float(price_before)) / float(price_before), 2)

    await session.commit()


async def get_price_at(session: AsyncSession, symbol: str, ts: datetime, offset_minutes: int):
    """Get closest price around target timestamp."""
    target = ts + timedelta(minutes=offset_minutes)
    window_start = target - timedelta(minutes=5)
    window_end = target + timedelta(minutes=5)

    result = await session.execute(
        select(PriceHistory.price)
        .where(PriceHistory.symbol == symbol)
        .where(PriceHistory.timestamp.between(window_start, window_end))
        .order_by(func.abs(func.extract("epoch", PriceHistory.timestamp - target)))
        .limit(1)
    )
    return result.scalar_one_or_none()

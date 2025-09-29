import logging
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.news_sentiment import NewsSentiment
from app.schemas.news_sentiment import NewsSentimentCreate
from app.deps.db import get_session
from app.config import AUTH_CRYPTONEW_TOKEN

log = logging.getLogger(__name__)

# Query to NewsAPI
NEWS_QUERY = "bitcoin OR ethereum OR binance OR sec OR hack"
NEWS_URL = (
    f"https://newsapi.org/v2/everything?q={NEWS_QUERY}"
    f"&language=en&sortBy=publishedAt&pageSize=10&apiKey={AUTH_CRYPTONEW_TOKEN}"
)

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Blacklist / whitelist for sources
BLACKLIST_SOURCES = {"reddit.com"}

# Default source weights
SOURCE_WEIGHTS = {
    "CoinDesk": 0.7,
    "Cointelegraph": 0.7,
    "Decrypt": 0.7,
    "Bloomberg": 0.85,
    "default": 0.5,
}


async def fetch_latest_news() -> list[dict]:
    """
    Fetch latest news from NewsAPI.
    Returns a list of news items with title, summary, publishedAt, url, source.
    """
    try:
        response = requests.get(NEWS_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])

        return [
            {
                "title": a.get("title", ""),
                "summary": a.get("description", "") or "",
                "published_at": a.get("publishedAt", ""),
                "url": a.get("url", ""),
                "source": a.get("source", {}).get("name", "")
            }
            for a in articles
            if a.get("source", {}).get("name", "") not in BLACKLIST_SOURCES
        ]

    except Exception as e:
        log.exception(f"❌ Error fetching news: {e}")
        return []


async def save_news_to_db(news_items: list[dict], session: AsyncSession):
    """
    Insert news into DB if not already present.
    """
    inserted_count = 0

    for news in news_items:
        if not all(k in news for k in ["published_at", "title"]):
            log.debug(f"⚠️ Skipped news due to missing fields: {news}")
            continue

        # Check if news already exists
        result = await session.execute(
            select(NewsSentiment).where(
                NewsSentiment.published_at == news["published_at"],
                NewsSentiment.title == news["title"]
            )
        )
        existing = result.scalar_one_or_none()
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
            pair=news.get("pair", None),
            url=news.get("url", ""),
        )

        session.add(db_news)
        inserted_count += 1

    await session.commit()
    log.info(f"✅ Inserted {inserted_count} news into DB")


async def check_news_and_halt_trading(session: AsyncSession):
    """
    Example scheduled job: fetch news and save them to DB.
    """
    news = await fetch_latest_news()
    if news:
        await save_news_to_db(news, session)


async def update_news_prices(session: AsyncSession):
    """
    Placeholder for price update logic.
    Will query analysis_data and update price_before/after fields.
    """
    log.info("🔄 [stub] Updating news prices (to be implemented)")

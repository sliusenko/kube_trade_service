import logging
import httpx
import uuid
import os
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
import datetime as dt

from common.models.markethistory import NewsSentiment, PriceHistory
from common.models.exchanges import ExchangeSymbol
from common.deps.config import CoreNewsSettings
from common.utils.config_resolver import ConfigResolver

# === дефолти з BaseSettings ===
settings = CoreNewsSettings()
resolver = ConfigResolver("core-news", settings.dict())

log = logging.getLogger(__name__)
analyzer = SentimentIntensityAnalyzer()

# ==============================
# JOB CONFIG
# ==============================
async def job_check_news(session: AsyncSession):
    NEWS_ENDPOINT = await resolver.get(session, "NEWS_ENDPOINT")
    NEWS_PARAMS = await resolver.get_dict(session, "NEWS_PARAMS") or settings.NEWS_PARAMS
    BLACKLIST_SOURCES = await resolver.get_dict(session, "BLACKLIST_SOURCES") or settings.BLACKLIST_SOURCES
    KEYWORD_TO_SYMBOL = await resolver.get_dict(session, "KEYWORD_TO_SYMBOL") or settings.KEYWORD_TO_SYMBOL
    DEFAULT_HALT_THRESHOLD = await resolver.get_float(session, "DEFAULT_HALT_THRESHOLD") or settings.DEFAULT_HALT_THRESHOLD
    UPDATE_NEWS_PRICES_INTERVAL_HOURS = await resolver.get_int(session, "UPDATE_NEWS_PRICES_INTERVAL_HOURS") or settings.UPDATE_NEWS_PRICES_INTERVAL_HOURS

    log.info(
        "📰 Config → endpoint=%s, params=%s, blacklist=%s, symbols=%s, halt=%.2f, update_h=%s",
        NEWS_ENDPOINT, NEWS_PARAMS, BLACKLIST_SOURCES, KEYWORD_TO_SYMBOL,
        DEFAULT_HALT_THRESHOLD, UPDATE_NEWS_PRICES_INTERVAL_HOURS
    )

    # виконуємо pipeline
    items = await fetch_latest_news(session, NEWS_ENDPOINT, NEWS_PARAMS, BLACKLIST_SOURCES)
    if not items:
        log.info("ℹ️ No fresh news fetched from NewsAPI")
    else:
        await save_news_to_db(items, session)

    try:
        await update_news_prices(session)
    except Exception as e:
        log.warning("⚠️ update_news_prices failed: %s", e)

    # обрахунок середнього сентименту
    lookback_h = int(os.getenv("NEWS_LOOKBACK_HOURS", UPDATE_NEWS_PRICES_INTERVAL_HOURS))
    avg_sent = await _avg_recent_sentiment(session, hours=lookback_h)

    if avg_sent is None:
        log.info("ℹ️ No news in the last %s hours to aggregate sentiment", lookback_h)
        return

    threshold_cfg = await resolver.get_float(session, "HALT_TRADE_NEG_SENTIMENT")
    threshold = threshold_cfg if threshold_cfg is not None else float(os.getenv("HALT_TRADE_NEG_SENTIMENT", DEFAULT_HALT_THRESHOLD))

    log.info("📰 Avg news sentiment (last %sh): %.3f; threshold: %.2f", lookback_h, avg_sent, threshold)

    if avg_sent <= threshold:
        log.warning("🚨 Negative average sentiment (%.3f <= %.2f) → HALT trading (TODO: persist/notify)", avg_sent, threshold)
    else:
        log.info("✅ Sentiment above threshold, trading stays enabled")
# ==============================
# HELPERS
# ==============================
def _parse_ts(ts_str: str) -> Optional[datetime]:
    if not ts_str:
        return None
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00")).astimezone(timezone.utc)

async def fetch_latest_news(session: AsyncSession, NEWS_ENDPOINT: str, NEWS_PARAMS: dict, BLACKLIST_SOURCES: set) -> List[dict]:
    """Тягне батч свіжих новин із NewsAPI та нормалізує поля."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                NEWS_ENDPOINT,
                params=NEWS_PARAMS,
                headers={"X-Api-Key": settings.NEWSAPI_KEY},
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

def detect_symbol_from_news(title: str, summary: str, KEYWORD_TO_SYMBOL: dict) -> str | None:
    """Визначає код символа з ключових слів у новині."""
    text = f"{title.lower()} {summary.lower()}"
    for keyword, symbol in KEYWORD_TO_SYMBOL.items():
        if keyword in text:
            return symbol
    return None

async def get_symbol_id_by_code(session: AsyncSession, symbol_code: str) -> str | None:
    base, _, quote = symbol_code.partition("/")
    if not quote:
        q = (
            select(ExchangeSymbol.id)
            .where(ExchangeSymbol.symbol.like(f"{base}/USDT"))
            .limit(1)
        )
    else:
        q = select(ExchangeSymbol.id).where(ExchangeSymbol.symbol == symbol_code).limit(1)

    res = await session.execute(q)
    return res.scalar_one_or_none()

async def save_news_to_db(news_items: List[dict], session: AsyncSession) -> None:
    """Зберігає новини у NewsSentiment (idempotent по published_at + title)."""
    inserted_count = 0
    for news in news_items:
        if not news.get("published_at") or not news.get("title"):
            continue

        q = select(NewsSentiment).where(
            NewsSentiment.published_at == news["published_at"],
            NewsSentiment.title == news["title"][:500],
        )
        existing = (await session.execute(q)).scalar_one_or_none()
        if existing:
            continue

        text = f"{news['title']} {news.get('summary', '')}"
        score = analyzer.polarity_scores(text)

        # 🟢 резолвимо символ
        symbol_code = detect_symbol_from_news(news["title"], news.get("summary", ""),
                                              await resolver.get_dict(session, "KEYWORD_TO_SYMBOL") or settings.KEYWORD_TO_SYMBOL)
        symbol_id = None
        if symbol_code:
            symbol_id = await get_symbol_id_by_code(session, symbol_code)
            log.info("🔎 News '%s' → matched symbol=%s, id=%s", news["title"], symbol_code, symbol_id)
        else:
            log.warning("⚠️ No symbol matched for news: '%s'", news["title"])

        db_news = NewsSentiment(
            published_at=news["published_at"],
            title=news["title"][:500],
            summary=news.get("summary", "")[:1000],
            sentiment=score["compound"],
            source=news.get("source", "newsapi"),
            url=news.get("url", ""),
            symbol_id=symbol_id,
        )
        session.add(db_news)
        inserted_count += 1

    await session.commit()
    log.info("✅ Inserted %s news into DB (with symbols)", inserted_count)

async def _get_price_at(session: AsyncSession, symbol_id: uuid.UUID, target_ts: datetime, before: bool = False) -> Optional[float]:
    """Отримати найближчу ціну до часу target_ts."""
    if before:
        q = (
            select(PriceHistory.price)
            .where(PriceHistory.symbol_id == symbol_id, PriceHistory.timestamp <= target_ts)
            .order_by(PriceHistory.timestamp.desc())
            .limit(1)
        )
    else:
        q = (
            select(PriceHistory.price)
            .where(PriceHistory.symbol_id == symbol_id, PriceHistory.timestamp >= target_ts)
            .order_by(PriceHistory.timestamp.asc())
            .limit(1)
        )
    res = await session.execute(q)
    return res.scalar_one_or_none()

async def update_news_prices(session: AsyncSession) -> None:
    """Проставляє ціни до/після для новин останніх 2 днів і прораховує % зміни."""
    now = dt.datetime.utcnow()

    q = select(NewsSentiment).where(NewsSentiment.published_at >= now - dt.timedelta(days=2))
    results = (await session.execute(q)).scalars().all()

    for news in results:
        if not news.symbol_id:
            continue

        ts = news.published_at

        price_before = await _get_price_at(session, news.symbol_id, ts, before=True)
        price_after_1h = await _get_price_at(session, news.symbol_id, ts + dt.timedelta(hours=1))
        price_after_6h = await _get_price_at(session, news.symbol_id, ts + dt.timedelta(hours=6))
        price_after_24h = await _get_price_at(session, news.symbol_id, ts + dt.timedelta(hours=24))

        news.price_before = price_before
        news.price_after_1h = price_after_1h
        news.price_after_6h = price_after_6h
        news.price_after_24h = price_after_24h

        if price_before and price_after_1h:
            news.price_change_1h = float((price_after_1h - price_before) / price_before * 100)
        if price_before and price_after_6h:
            news.price_change_6h = float((price_after_6h - price_before) / price_before * 100)
        if price_before and price_after_24h:
            news.price_change_24h = float((price_after_24h - price_before) / price_before * 100)

    await session.commit()
    log.info("✅ Updated prices for %s news items", len(results))

async def _avg_recent_sentiment(session: AsyncSession, hours: int) -> Optional[float]:
    """Середній compound-сентимент новин за останні N годин з NewsSentiment."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    q = select(func.avg(NewsSentiment.sentiment)).where(NewsSentiment.published_at >= cutoff)
    res = await session.execute(q)
    return res.scalar_one_or_none()

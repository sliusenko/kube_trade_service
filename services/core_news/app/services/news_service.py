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
settings = CoreNewsSettings()

log = logging.getLogger(__name__)
analyzer = SentimentIntensityAnalyzer()

# === NewsAPI config ===
NEWS_ENDPOINT = settings.NEWS_ENDPOINT
NEWS_PARAMS = settings.NEWS_PARAMS
BLACKLIST_SOURCES = settings.BLACKLIST_SOURCES
KEYWORD_TO_SYMBOL = settings.KEYWORD_TO_SYMBOL
DEFAULT_HALT_THRESHOLD = settings.DEFAULT_HALT_THRESHOLD
DEFAULT_LOOKBACK_HOURS = settings.DEFAULT_LOOKBACK_HOURS

def _parse_ts(ts_str: str) -> Optional[datetime]:
    if not ts_str:
        return None
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00")).astimezone(timezone.utc)

async def fetch_latest_news() -> List[dict]:
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

async def get_symbol_id(session: AsyncSession, text: str) -> Optional[uuid.UUID]:
    """Шукає відповідний exchange_symbols.id за ключовими словами у тексті новини."""
    if not text:
        return None

    text_lower = text.lower()
    for keyword, mapped_symbol in KEYWORD_TO_SYMBOL.items():
        if keyword in text_lower and mapped_symbol:
            q = sa.select(ExchangeSymbol.id).where(ExchangeSymbol.symbol == mapped_symbol)
            res = await session.execute(q)
            symbol_id = res.scalar_one_or_none()
            if symbol_id:
                return symbol_id
    return None

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

        symbol_id = await get_symbol_id(session, news["title"])

        db_news = NewsSentiment(
            published_at=news["published_at"],
            title=news["title"][:500],
            summary=news.get("summary", "")[:1000],
            sentiment=score["compound"],
            source=news.get("source", "newsapi"),
            symbol_id=symbol_id,
            url=news.get("url", ""),
        )
        session.add(db_news)
        inserted_count += 1

    await session.commit()
    log.info("✅ Inserted %s news into DB", inserted_count)

async def _get_price_at(session: AsyncSession, symbol_id: uuid.UUID, target_ts: datetime, before: bool = False) -> Optional[float]:
    """Отримати найближчу ціну до часу target_ts."""
    if before:
        # ціна ≤ published_at (останній запис перед новиною)
        q = (
            select(PriceHistory.price)
            .where(PriceHistory.symbol_id == symbol_id, PriceHistory.timestamp <= target_ts)
            .order_by(PriceHistory.timestamp.desc())
            .limit(1)
        )
    else:
        # ціна найближча після target_ts
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
            continue  # новина не прив’язана до символа

        ts = news.published_at

        # Ціна до новини
        price_before = await _get_price_at(session, news.symbol_id, ts, before=True)

        # Ціни після новини
        price_after_1h = await _get_price_at(session, news.symbol_id, ts + dt.timedelta(hours=1))
        price_after_6h = await _get_price_at(session, news.symbol_id, ts + dt.timedelta(hours=6))
        price_after_24h = await _get_price_at(session, news.symbol_id, ts + dt.timedelta(hours=24))

        # Записати в модель
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

# === Агрегація сентименту та HALT-логіка ===
async def _avg_recent_sentiment(session: AsyncSession, hours: int = DEFAULT_LOOKBACK_HOURS) -> Optional[float]:
    """Середній compound-сентимент новин за останні N годин з NewsSentiment."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    q = select(func.avg(NewsSentiment.sentiment)).where(NewsSentiment.published_at >= cutoff)
    res = await session.execute(q)
    return res.scalar_one_or_none()

async def check_news_and_halt_trading(session: AsyncSession) -> None:
    """
    Оркестрація:
      1) fetch свіжих новин
      2) save у БД із compound-сентиментом
      3) update цін до/після
      4) aggregate sentiment (за вікно lookback) та, якщо нижче порога — HALT (поки лог/TODO)
    """
    # 1) fetch
    items = await fetch_latest_news()
    if not items:
        log.info("ℹ️ No fresh news fetched from NewsAPI")
    else:
        # 2) save
        await save_news_to_db(items, session)

    # 3) update prices (опційно; не блокуємо цикл у випадку помилки)
    try:
        await update_news_prices(session)
    except Exception as e:
        log.warning("⚠️ update_news_prices failed: %s", e)

    # 4) aggregate & decision
    lookback_h = getattr(settings, "NEWS_LOOKBACK_HOURS", None) or int(os.getenv("NEWS_LOOKBACK_HOURS", DEFAULT_LOOKBACK_HOURS))
    avg_sent = await _avg_recent_sentiment(session, hours=lookback_h)
    if avg_sent is None:
        log.info("ℹ️ No news in the last %s hours to aggregate sentiment", lookback_h)
        return

    threshold_cfg = getattr(settings, "HALT_TRADE_NEG_SENTIMENT", None)
    threshold = float(threshold_cfg) if threshold_cfg is not None else float(os.getenv("HALT_TRADE_NEG_SENTIMENT", DEFAULT_HALT_THRESHOLD))

    log.info("📰 Avg news sentiment (last %sh): %.3f; threshold: %.2f", lookback_h, avg_sent, threshold)

    if avg_sent <= threshold:
        # TODO: Реальна імплементація зупинки торгівлі:
        # await set_global_trading_halt(session, reason="news_negative",
        #                               until=datetime.utcnow() + timedelta(hours=1))
        log.warning("🚨 Negative average sentiment (%.3f <= %.2f) → HALT trading (TODO: persist/notify)", avg_sent, threshold)
    else:
        log.info("✅ Sentiment above threshold, trading stays enabled")


# Приклад заглушки для майбутнього:
# async def set_global_trading_halt(session: AsyncSession, reason: str, until: datetime) -> None:
#     """
#     Встановити прапор HALT у вашій таблиці конфігів/фіч-флагів або надіслати подію в інший сервіс.
#     """
#     ...

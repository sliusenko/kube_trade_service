import logging
import httpx
import uuid
import re
from datetime import datetime, timezone, timedelta
from typing import Optional
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import sqlalchemy as sa
import datetime as dt
from common.models.markethistory import NewsSentiment, PriceHistory
from common.models.exchanges import ExchangeSymbol
from common.deps.config import settings

log = logging.getLogger(__name__)

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_PARAMS = {
    "q": "bitcoin OR ethereum OR binance OR sec OR hack",
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 10,
}

analyzer = SentimentIntensityAnalyzer()
BLACKLIST_SOURCES = {"reddit.com"}


def _parse_ts(ts_str: str):
    if not ts_str:
        return None
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00")).astimezone(timezone.utc)


async def fetch_latest_news() -> list[dict]:
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


# 🔑 Мапа ключових слів → торгові символи
KEYWORD_TO_SYMBOL = {
    "bitcoin": "BTCUSDT",
    "btc": "BTCUSDT",
    "ethereum": "ETHUSDT",
    "eth": "ETHUSDT",
    "binance": "BNBUSDT",
    "bnb": "BNBUSDT",
    "sec": "BTCUSDT",     # умовно тягнемо до BTC
    "hack": None,         # загальні новини про хак не мапимо на конкретний символ
}


async def get_symbol_id(session: AsyncSession, text: str) -> Optional[uuid.UUID]:
    """Шукає відповідний symbol_id по ключовим словам у тексті новини"""
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

async def save_news_to_db(news_items: list[dict], session: AsyncSession):
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
    log.info(f"✅ Inserted {inserted_count} news into DB")

async def update_news_prices(session):
    now = dt.datetime.utcnow()

    # Вибрати всі новини без цін або нові (наприклад за 2 дні)
    q = select(NewsSentiment).where(
        NewsSentiment.published_at >= now - dt.timedelta(days=2)
    )
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
    log.info(f"✅ Updated prices for {len(results)} news items")

async def _get_price_at(session, symbol_id, target_ts, before=False):
    """Отримати найближчу ціну до часу target_ts"""
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

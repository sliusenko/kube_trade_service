import logging
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.exchanges_symbols import Exchange, ExchangeCredential


async def get_exchange_client(session: AsyncSession, exchange: Exchange):
    """
    Універсальний клієнт для будь-якої біржі.
    Будує httpx.AsyncClient з base_url з таблиці exchange + креденшли.
    """
    res = await session.execute(
        select(ExchangeCredential)
        .where(ExchangeCredential.exchange_id == exchange.id)
        .where(ExchangeCredential.is_service == True)
        .where(ExchangeCredential.is_active == True)
        .limit(1)
    )
    cred = res.scalar_one_or_none()

    if not cred:
        logging.warning(f"⚠️ Немає сервісного акаунту для {exchange.code}")
        return None

    base_url = getattr(exchange, "base_url_private", None) or getattr(exchange, "base_url_public", None)
    if not base_url:
        logging.warning(f"⚠️ У {exchange.code} не задано base_url у таблиці exchanges")
        return None

    client = {
        "exchange_code": exchange.code,
        "exchange_id": exchange.id,
        "api_key": cred.api_key,
        "api_secret": cred.api_secret,
        "api_passphrase": cred.api_passphrase,
        "http": httpx.AsyncClient(base_url=base_url)
    }

    return client

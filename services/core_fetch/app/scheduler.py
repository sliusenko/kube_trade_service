import os
import asyncio
import logging
import uuid
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from core_fetch.app.services.universal_fetcher import (
    fetch_and_store_price, refresh_symbols,
    refresh_limits, refresh_fees
)
from common.deps.session import SessionLocal
from common.models.exchanges import Exchange, ExchangeSymbol
from common.models import ExchangeStatusHistory
from common.deps.clients import get_exchange_client
from common.utils.config_resolver import ConfigResolver
from common.deps.config import CoreFetchSettings
settings = CoreFetchSettings()
SERVICE_NAME = os.getenv("SERVICE_NAME", "core-fetch")
resolver = ConfigResolver(SERVICE_NAME, settings.dict(), extra_service_names=[f"kube-trade-bot-{SERVICE_NAME}"])

log = logging.getLogger(__name__)

# Make scheduler global
scheduler = AsyncIOScheduler()

async def fetch_and_store_exchange_prices(exchange_code: str, exchange_id: uuid.UUID) -> None:
    """Fetch latest prices for all active symbols of a given exchange."""
    try:
        async with SessionLocal() as session:
            res = await session.execute(
                select(ExchangeSymbol.symbol_id)
                .where(
                    ExchangeSymbol.exchange_id == exchange_id,
                    ExchangeSymbol.status == "TRADING"
                )
            )
            symbols = [row[0] for row in res.all()]

        log.info(f"💰 Fetching prices for {exchange_code}: {len(symbols)} pairs")

        ok_count = 0
        fail_count = 0

        for symbol_id in symbols:
            try:
                await fetch_and_store_price(exchange_code, symbol_id)
                ok_count += 1
            except Exception as e:
                fail_count += 1
                log.error(f"❌ {exchange_code}:{symbol_id} failed: {e}")

        # aggregated log
        async with SessionLocal() as session:
            session.add(
                ExchangeStatusHistory(
                    exchange_id=exchange_id,
                    event="price_fetch",
                    status="ok" if fail_count == 0 else "partial",
                    message=f"Fetched prices for {exchange_code}: {ok_count} ok, {fail_count} failed",
                )
            )
            await session.commit()

        log.info(f"✅ {exchange_code} prices done: {ok_count} ok, {fail_count} failed")

    except Exception as e:
        log.exception(f"❌ fetch_and_store_exchange_prices error for {exchange_code}: {e}")
        async with SessionLocal() as session:
            session.add(
                ExchangeStatusHistory(
                    exchange_id=exchange_id,
                    event="price_fetch",
                    status="error",
                    message=str(e),
                )
            )
            await session.commit()

async def load_jobs(scheduler: AsyncIOScheduler):
    async with SessionLocal() as session:
        res = await session.execute(select(Exchange))
        exchanges = res.scalars().all()
        log.info(f"📊 Found {len(exchanges)} exchanges in DB")

        for ex in exchanges:
            log.info(f"➡️ Processing exchange {ex.code} ({ex.name})")
            client = await get_exchange_client(session, ex)
            if not client:
                log.warning(f"⚠️ Skipping {ex.code}, no client")
                continue

            scheduler.add_job(
                refresh_symbols,
                "interval",
                minutes=int(ex.fetch_symbols_interval_min),
                args=[client, ex.id],
                id=f"symbols_{ex.code}_{ex.id}",
                replace_existing=True,
            )
            scheduler.add_job(
                refresh_limits,
                "interval",
                minutes=int(ex.fetch_limits_interval_min),
                args=[client, ex.id],
                id=f"limits_{ex.code}_{ex.id}",
                replace_existing=True,
            )
            scheduler.add_job(
                refresh_fees,
                "interval",
                minutes=int(ex.fetch_fees_interval_min),
                args=[client, ex.id],
                id=f"fees_{ex.code}_{ex.id}",
                replace_existing=True,
            )
            fetch_interval = await resolver.get_int(session, "FETCH_NEWS_INTERVAL_MIN") or settings.FETCH_NEWS_INTERVAL_MIN
            scheduler.add_job(
                fetch_and_store_exchange_prices,
                "interval",
                minutes=int(fetch_interval),
                args=[ex.code, ex.id],
                id=f"prices_{ex.code}_{ex.id}",
                replace_existing=True,
                max_instances=1,
                misfire_grace_time=30,
            )

        log.info(
            f"🕑 Added {len(exchanges)} grouped price jobs "
            f"(every {fetch_interval}m)"
        )

    log.info("✅ Jobs loaded")

def start_scheduler():
    log.info("🟢 Starting AsyncIOScheduler")
    asyncio.create_task(load_jobs(scheduler))
    scheduler.start()
    log.info("✅ Scheduler started")

import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from core_fetch.app.services.universal_fetcher import (
    fetch_and_store_price, refresh_symbols,
    refresh_limits, refresh_fees
)
from common.deps.session import SessionLocal
from common.models.exchanges import Exchange, ExchangeSymbol
from common.deps.clients import get_exchange_client
from common.deps.config import settings

log = logging.getLogger(__name__)

# Make scheduler global
scheduler = AsyncIOScheduler()

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

            # ---- symbols ----
            scheduler.add_job(
                refresh_symbols,
                "interval",
                minutes=int(ex.fetch_symbols_interval_min),
                args=[client, ex.id],
                id=f"symbols_{ex.code}_{ex.id}",
                replace_existing=True,
            )

            # ---- limits ----
            scheduler.add_job(
                refresh_limits,
                "interval",
                minutes=int(ex.fetch_limits_interval_min),
                args=[client, ex.id],
                id=f"limits_{ex.code}_{ex.id}",
                replace_existing=True,
            )

            # ---- fees ----
            scheduler.add_job(
                refresh_fees,
                "interval",
                minutes=int(ex.fetch_fees_interval_min),
                args=[client, ex.id],
                id=f"fees_{ex.code}_{ex.id}",
                replace_existing=True,
            )

        # ---- prices (global) ----
        res = await session.execute(
            select(Exchange.code, ExchangeSymbol.symbol_id)
            .join(Exchange, Exchange.id == ExchangeSymbol.exchange_id)
            .where(ExchangeSymbol.status == "TRADING")
        )
        symbols = res.all()

        for exchange_code, symbol_id in symbols:
            scheduler.add_job(
                fetch_and_store_price,
                "interval",
                minutes=int(settings.FETCH_PRICE_INTERVAL_MIN),
                args=[exchange_code, symbol_id],
                id=f"price_{exchange_code.lower()}_{symbol_id.lower()}",
                replace_existing=True,
            )

        log.info(
            f"🕑 Added {len(symbols)} price jobs "
            f"(every {settings.FETCH_PRICE_INTERVAL_MIN}m)"
        )

    log.info("✅ Jobs loaded")

def start_scheduler():
    log.info("🟢 Starting AsyncIOScheduler")
    asyncio.create_task(load_jobs(scheduler))
    scheduler.start()
    log.info("✅ Scheduler started")

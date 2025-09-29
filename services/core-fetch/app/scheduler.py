import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services import universal_fetcher
from app.services.fetch_price import fetch_and_store_price
from app.deps.session import SessionLocal
from sqlalchemy import select
from app.models.exchanges_symbols import Exchange
from app.deps.clients import get_exchange_client

log = logging.getLogger(__name__)

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

            # Symbols
            if hasattr(universal_fetcher, "refresh_symbols"):
                scheduler.add_job(
                    universal_fetcher.refresh_symbols,
                    "interval",
                    minutes=ex.fetch_symbols_interval_min,
                    args=[client, ex.id],
                    id=f"symbols_{ex.code}_{ex.id}",
                    replace_existing=True,
                )

            # Limits
            if hasattr(universal_fetcher, "refresh_limits"):
                scheduler.add_job(
                    universal_fetcher.refresh_limits,
                    "interval",
                    minutes=ex.fetch_limits_interval_min,
                    args=[client, ex.id],
                    id=f"limits_{ex.code}_{ex.id}",
                    replace_existing=True,
                )

            # Fees
            if hasattr(universal_fetcher, "refresh_fees"):
                scheduler.add_job(
                    universal_fetcher.refresh_fees,
                    "interval",
                    minutes=ex.fetch_fees_interval_min,
                    args=[client, ex.id],
                    id=f"fees_{ex.code}_{ex.id}",
                    replace_existing=True,
                )

        # Global job: fetch prices
        scheduler.add_job(
            fetch_and_store_price,
            "interval",
            minutes=10,   # later make configurable
            args=["BINANCE", "BTCUSDT"],
            id="price_binance_btcusdt",
            replace_existing=True,
        )

    log.info("✅ Jobs loaded")

def start_scheduler():
    log.info("🟢 Starting AsyncIOScheduler")
    scheduler = AsyncIOScheduler()
    asyncio.create_task(load_jobs(scheduler))
    scheduler.start()
    log.info("✅ Scheduler started")

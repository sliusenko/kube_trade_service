import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from app.models.exchanges_symbols import Exchange
from app.deps.clients import get_exchange_client
from app.services import universal_fetcher
from app.deps.session import SessionLocal

log = logging.getLogger(__name__)

async def load_jobs(scheduler: AsyncIOScheduler):
    log.info("🚀 Loading jobs")

    async with SessionLocal() as session:
        res = await session.execute(select(Exchange))
        exchanges = res.scalars().all()

        log.info(f"📊 Found {len(exchanges)} exchanges")

        for ex in exchanges:
            log.info(f"➡️ Processing exchange {ex.code} ({ex.name})")

            client = await get_exchange_client(session, ex)
            if not client:
                log.warning(f"⚠️ Skipping {ex.code}, no client")
                continue

            module = universal_fetcher

            # ---- symbols ----
            if hasattr(module, "refresh_symbols"):
                scheduler.add_job(
                    module.refresh_symbols,
                    "interval",
                    minutes=ex.fetch_symbols_interval_min,
                    args=[client, ex.id],
                    id=f"symbols_{ex.code}_{ex.id}",
                    replace_existing=True,
                )
                log.info(f"🕑 Added job symbols for {ex.code} ({ex.fetch_symbols_interval_min}m)")

            # ---- limits ----
            if hasattr(module, "refresh_limits"):
                scheduler.add_job(
                    module.refresh_limits,
                    "interval",
                    minutes=ex.fetch_limits_interval_min,
                    args=[client, ex.id],
                    id=f"limits_{ex.code}_{ex.id}",
                    replace_existing=True,
                )
                log.info(f"🕑 Added job limits for {ex.code} ({ex.fetch_limits_interval_min}m)")

            # ---- fees ----
            if hasattr(module, "refresh_fees"):
                scheduler.add_job(
                    module.refresh_fees,
                    "interval",
                    minutes=ex.fetch_fees_interval_min,
                    args=[client, ex.id],
                    id=f"fees_{ex.code}_{ex.id}",
                    replace_existing=True,
                )
                log.info(f"🕑 Added job fees for {ex.code} ({ex.fetch_fees_interval_min}m)")

    log.info("✅ Jobs loaded")


def start_scheduler():
    log.info("🟢 Starting AsyncIOScheduler")
    scheduler = AsyncIOScheduler()

    # Run async job loader inside loop
    asyncio.create_task(load_jobs(scheduler))

    scheduler.start()
    log.info("✅ Scheduler started")

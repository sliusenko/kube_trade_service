import asyncio
import logging
import importlib
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from core_fetch.db.session import SessionLocal
from core_fetch.db.models import Exchange
from core_fetch.services.clients import get_exchange_client


async def load_jobs(scheduler: AsyncIOScheduler):
    async with SessionLocal() as session:
        res = await session.execute(select(Exchange))
        exchanges = res.scalars().all()

        for ex in exchanges:
            client = await get_exchange_client(session, ex)
            if not client:
                logging.warning(f"⚠️ Пропускаю {ex.code}, немає клієнта")
                continue

            try:
                module = importlib.import_module(f"core_fetch.services.{ex.code}_fetcher")
            except Exception as e:
                logging.error(f"❌ Не знайшов fetcher для {ex.code}: {e}")
                continue

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
                logging.info(
                    f"🕑 Job symbols для {ex.code} ({ex.name}) "
                    f"кожні {ex.fetch_symbols_interval_min} хв"
                )

            # ---- filters ----
            if hasattr(module, "refresh_filters"):
                scheduler.add_job(
                    module.refresh_filters,
                    "interval",
                    minutes=ex.fetch_filters_interval_min,
                    args=[client, ex.id],
                    id=f"filters_{ex.code}_{ex.id}",
                    replace_existing=True,
                )
                logging.info(
                    f"🕑 Job filters для {ex.code} ({ex.name}) "
                    f"кожні {ex.fetch_filters_interval_min} хв"
                )

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
                logging.info(
                    f"🕑 Job limits для {ex.code} ({ex.name}) "
                    f"кожні {ex.fetch_limits_interval_min} хв"
                )


def start_scheduler():
    scheduler = AsyncIOScheduler()
    loop = asyncio.get_event_loop()
    loop.create_task(load_jobs(scheduler))
    scheduler.start()
    loop.run_forever()

import asyncio
import logging
import importlib
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from core_fetch.db.session import SessionLocal
from core_fetch.db.models import Exchange
from core_fetch.services.clients import get_exchange_client
from core_fetch.utils.config import settings


async def load_jobs(scheduler: AsyncIOScheduler):
    async with SessionLocal() as session:
        res = await session.execute(select(Exchange))
        exchanges = res.scalars().all()

        for ex in exchanges:
            # 1. будуємо client з credentials
            client = await get_exchange_client(session, ex)
            if not client:
                logging.warning(f"⚠️ Пропускаю {ex.code}, немає клієнта")
                continue

            # 2. динамічно імпортуємо fetcher за code
            try:
                module = importlib.import_module(f"core_fetch.services.{ex.code}_fetcher")
                fetcher = getattr(module, f"refresh_{ex.code}")
            except Exception as e:
                logging.error(f"❌ Не знайшов fetcher для {ex.code}: {e}")
                continue

            # 3. створюємо job з конкретним fetcher
            scheduler.add_job(
                fetcher,
                trigger="interval",
                seconds=ex.refresh_interval or settings.FETCH_INTERVAL_DEFAULT,
                args=[client, ex.id],
                id=f"job_{ex.code}_{ex.id}",
                replace_existing=True,
            )

            logging.info(
                f"🕑 Додано job для {ex.code} ({ex.name}) "
                f"кожні {ex.refresh_interval or settings.FETCH_INTERVAL_DEFAULT} сек"
            )


def start_scheduler():
    scheduler = AsyncIOScheduler()
    loop = asyncio.get_event_loop()
    loop.create_task(load_jobs(scheduler))
    scheduler.start()
    loop.run_forever()


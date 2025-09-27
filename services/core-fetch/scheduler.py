import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from core_fetch.db.session import SessionLocal
from core_fetch.db.models import Exchange
from core_fetch.services.clients import get_exchange_client
from core_fetch.services import universal_fetcher


async def load_jobs(scheduler: AsyncIOScheduler):
    logging.info("🚀 Починаю завантаження jobs")

    async with SessionLocal() as session:
        res = await session.execute(select(Exchange))
        exchanges = res.scalars().all()

        logging.info(f"📊 Знайдено {len(exchanges)} бірж у таблиці exchanges")

        for ex in exchanges:
            logging.info(f"➡️ Обробка біржі {ex.code} ({ex.name})")

            client = await get_exchange_client(session, ex)
            if not client:
                logging.warning(f"⚠️ Пропускаю {ex.code}, немає клієнта")
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
                logging.info(
                    f"🕑 Додав job symbols для {ex.code} "
                    f"(кожні {ex.fetch_symbols_interval_min} хв)"
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
                    f"🕑 Додав job limits для {ex.code} "
                    f"(кожні {ex.fetch_limits_interval_min} хв)"
                )

    logging.info("✅ Завантаження jobs завершено")


def start_scheduler():
    logging.info("🟢 Стартую AsyncIOScheduler")
    scheduler = AsyncIOScheduler()
    loop = asyncio.get_event_loop()
    loop.create_task(load_jobs(scheduler))
    scheduler.start()
    logging.info("✅ Scheduler запущено")
    loop.run_forever()

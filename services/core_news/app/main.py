import logging
import asyncio
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ⚠️ Підстав свій фабричний метод створення сесії:
# Якщо у тебе async_session() — заміни на нього.
from common.deps.db import AsyncSessionLocal

from core_news.app.services.news_service import check_news_and_halt_trading

log = logging.getLogger(__name__)
app = FastAPI(title="core-news")
scheduler = AsyncIOScheduler()

# ——— Health ———
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

# ——— APScheduler jobs ———
async def job_check_news():
    async with AsyncSessionLocal() as session:
        await check_news_and_halt_trading(session)

@app.on_event("startup")
async def startup_event():
    # інтервал можна конфігурити через env/values, тут 10 хв як у тебе в логах
    scheduler.add_job(job_check_news, "interval", minutes=10, id="check_news_interval")
    scheduler.start()
    log.info("🗓️ APScheduler started (check_news every 10 minutes)")

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown(wait=False)
    log.info("🛑 APScheduler stopped")

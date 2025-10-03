import logging
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ⚠️ Підстав свій фабричний метод створення сесії:
# Якщо у тебе async_session() — заміни на нього.
from common.deps.db import AsyncSessionLocal
from core_news.app.routers import news
from core_news.app.services.news_service import job_check_news

log = logging.getLogger(__name__)
app = FastAPI(title="core-news")
scheduler = AsyncIOScheduler()

# Register routers
app.include_router(news.router)

# ——— Health ———
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

# ——— APScheduler jobs ———
async def job_check_news_wrapper():
    async with AsyncSessionLocal() as session:
        await job_check_news(session)

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(job_check_news_wrapper, "interval", minutes=10, id="check_news_interval")
    scheduler.start()
    log.info("🗓️ APScheduler started (job_check_news every 10 minutes)")

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown(wait=False)
    log.info("🛑 APScheduler stopped")

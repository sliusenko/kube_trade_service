import os
import logging
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from common.deps.db import AsyncSessionLocal
from core_news.app.routers import news
from core_news.app.services.news_service import job_check_news
from common.utils.config_resolver import ConfigResolver
from common.deps.config import CoreNewsSettings
settings = CoreNewsSettings()
SERVICE_NAME = os.getenv("SERVICE_NAME", "core-news")
resolver = ConfigResolver(SERVICE_NAME, settings.dict(), extra_service_names=[f"kube-trade-bot-{SERVICE_NAME}"])

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
    async with AsyncSessionLocal() as session:
        interval_min = await resolver.get_int(session, "FETCH_NEWS_INTERVAL_MIN") or settings.FETCH_NEWS_INTERVAL_MIN

    scheduler.add_job(job_check_news_wrapper, "interval", minutes=interval_min, id="check_news_interval")
    scheduler.start()
    log.info("🗓️ APScheduler started (job_check_news every %s minutes)", interval_min)


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown(wait=False)
    log.info("🛑 APScheduler stopped")

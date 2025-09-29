# app/main.py
import os
import logging
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.routers import news
from app.services import news_service
from app.deps.db import async_session_maker, init_db

log = logging.getLogger(__name__)

# Global settings from env (Helm values)
FETCH_NEWS_INTERVAL_MIN = int(os.getenv("FETCH_NEWS_INTERVAL_MIN", "10"))
UPDATE_NEWS_PRICES_INTERVAL_HOURS = int(os.getenv("UPDATE_NEWS_PRICES_INTERVAL_HOURS", "1"))

app = FastAPI(title="core-news")

# Register routers
app.include_router(news.router)


@app.on_event("startup")
async def startup_event():
    log.info("🚀 Starting core-news service")

    # Ensure tables exist
    await init_db()

    scheduler = AsyncIOScheduler()

    # Job: fetch and store latest news
    async def job_check_news():
        async with async_session_maker() as session:
            await news_service.check_news_and_halt_trading(session)

    # Job: update price_before/after for saved news
    async def job_update_prices():
        async with async_session_maker() as session:
            await news_service.update_news_prices(session)

    # Add jobs to scheduler
    scheduler.add_job(job_check_news, "interval", minutes=FETCH_NEWS_INTERVAL_MIN)
    scheduler.add_job(job_update_prices, "interval", hours=UPDATE_NEWS_PRICES_INTERVAL_HOURS)

    scheduler.start()
    log.info(
        f"✅ Scheduler started with jobs: "
        f"news interval={FETCH_NEWS_INTERVAL_MIN}m, "
        f"update_prices interval={UPDATE_NEWS_PRICES_INTERVAL_HOURS}h"
    )


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}

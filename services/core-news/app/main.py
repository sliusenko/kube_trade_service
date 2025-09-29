import logging
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.news_service import check_news_and_halt_trading, update_news_prices

log = logging.getLogger(__name__)

app = FastAPI(title="core-news")

@app.on_event("startup")
async def startup_event():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_news_and_halt_trading, "interval", minutes=10)
    scheduler.add_job(update_news_prices, "interval", hours=1)
    scheduler.start()
    log.info("✅ Scheduler started")

@app.get("/health")
async def health():
    return {"status": "ok"}

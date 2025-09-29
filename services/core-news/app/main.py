from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.routers import news
from app.services.news_service import check_news_and_halt_trading, update_news_prices

app = FastAPI(title="core-news")

# Include routes
app.include_router(news.router)

@app.on_event("startup")
async def startup_event():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_news_and_halt_trading, "interval", minutes=10)
    scheduler.add_job(update_news_prices, "interval", hours=1)
    scheduler.start()

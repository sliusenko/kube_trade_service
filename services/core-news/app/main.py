from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.routers import news
from app.services import news_service
from app.deps.db import async_session_maker

app = FastAPI(title="core-news")

app.include_router(news.router)

@app.on_event("startup")
async def startup_event():
    scheduler = AsyncIOScheduler()

    async def job_check_news():
        async with async_session_maker() as session:
            await news_service.check_news_and_halt_trading(session)

    async def job_update_prices():
        async with async_session_maker() as session:
            await news_service.update_news_prices(session)

    scheduler.add_job(job_check_news, "interval", minutes=10)
    scheduler.add_job(job_update_prices, "interval", hours=1)
    scheduler.start()

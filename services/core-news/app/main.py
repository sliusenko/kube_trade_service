from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.news_service import check_news_and_halt_trading, update_news_prices

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_news_and_halt_trading, "interval", minutes=10)
    scheduler.add_job(update_news_prices, "interval", hours=1)
    scheduler.start()

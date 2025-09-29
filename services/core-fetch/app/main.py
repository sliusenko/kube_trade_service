import logging
from fastapi import FastAPI
from app.scheduler import start_scheduler
from app.routers import price_history

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="core-fetch",
    description="Microservice for fetching exchange data (symbols, limits, fees, prices)",
    version="0.1.0",
)

# Routers
app.include_router(price_history.router)

@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    start_scheduler()

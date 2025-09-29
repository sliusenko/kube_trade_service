from fastapi import FastAPI
from app.scheduler import start_scheduler
from app.routers import price_history, jobs

app = FastAPI(title="core-fetch")

# Register routers
app.include_router(price_history.router)
app.include_router(jobs.router)

@app.on_event("startup")
async def startup_event():
    start_scheduler()

@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}

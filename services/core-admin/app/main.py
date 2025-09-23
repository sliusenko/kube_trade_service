from fastapi import FastAPI
from app.models import Base
from app.deps.db import engine
from app.routers import users, roles, permissions, scheduler

app = FastAPI(title="Admin-core API")

@app.on_event("startup")
async def startup_event():
    # створюємо таблиці якщо їх нема
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)
app.include_router(roles.router)
app.include_router(permissions.router)
app.include_router(scheduler.router)

@app.get("/")
async def root():
    return {"message": "Admin-core API running"}

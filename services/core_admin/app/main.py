from fastapi import FastAPI
#from app import models
# from app.models.base import Base
# from app.deps.db import engine
from core_admin.app.routers import (
    users, roles, permissions,
    role_permissions, scheduler, exchanges, news, dashboard, config
)

app = FastAPI(title="Admin-core API")

# @app.on_event("startup")
# async def startup_event():

    # async with engine.begin() as conn:
    #     print(Base.metadata.tables.keys())
    #     await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)
app.include_router(roles.router)
app.include_router(permissions.router)
app.include_router(role_permissions.router)
app.include_router(scheduler.router)
app.include_router(exchanges.router)
app.include_router(news.router)
app.include_router(dashboard.router)
app.include_router(config.router)

@app.get("/")
async def root():
    return {"message": "core_admin API running"}

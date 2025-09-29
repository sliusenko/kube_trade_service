from fastapi import FastAPI
#from app import models
# from app.models.base import Base
# from app.deps.db import engine
from app.routers import (
    users, roles, permissions,
    role_permissions, scheduler, exchanges
)

app = FastAPI(title="Admin-core API")

@app.on_event("startup")
async def startup_event():

    # async with engine.begin() as conn:
    #     print(Base.metadata.tables.keys())
    #     await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)
app.include_router(roles.router)
app.include_router(permissions.router)
app.include_router(role_permissions.router)
app.include_router(scheduler.router)
app.include_router(exchanges.router)

@app.get("/")
async def root():
    return {"message": "core-admin API running"}

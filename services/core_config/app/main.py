from fastapi import FastAPI
from core_config.app.routers import (
    config_parameters,
    commands,
    group_icons,
    timeframes,
    reasons,
    trade_profiles,
    trade_conditions,
)

app = FastAPI(title="core-config")

# Підключаємо роути
app.include_router(config_parameters.router)
app.include_router(commands.router)
app.include_router(group_icons.router)
app.include_router(timeframes.router)
app.include_router(reasons.router)
app.include_router(trade_profiles.router)
app.include_router(trade_conditions.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

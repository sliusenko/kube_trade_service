from fastapi import FastAPI
from core_board.app.routers import dashboard

app = FastAPI(title="core-admin")

# Routers
app.include_router(dashboard.router)

from fastapi import FastAPI
from app.routers import settings

app = FastAPI(title="Admin Core")

# підключаємо маршрути
app.include_router(settings.router)

@app.get("/")
async def root():
    return {"message": "Admin-core API running"}

# core_admin/app/routers/news.py
from fastapi import APIRouter, HTTPException
from common.deps.config import CoreAdminSettings
settings = CoreAdminSettings()
import httpx

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/")
async def list_news():
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{settings.NEWS_BASE_URL}/news/")
        resp.raise_for_status()
        return resp.json()

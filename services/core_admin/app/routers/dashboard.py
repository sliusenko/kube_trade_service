# core_admin/app/routers/news.py
from fastapi import APIRouter, HTTPException
from common.deps.config import CoreAdminSettings
settings = CoreAdminSettings()
import httpx

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats")
async def dashboard_stats():
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{settings.DASHBOARD_BASE_URL}/dashboard/stats")
        resp.raise_for_status()
        return resp.json()

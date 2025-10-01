# core_admin/app/routers/news.py
from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
BASE_URL = "http://kube-trade-bot-core-board:8000"

@router.get("/stats")
async def dashboard_stats():
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{BASE_URL}/dashboard/stats")
        resp.raise_for_status()
        return resp.json()

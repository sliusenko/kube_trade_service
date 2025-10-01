# core_admin/app/routers/news.py
from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/news", tags=["news"])
BASE_URL = "http://kube-trade-bot-core-news:8000"

@router.get("/")
async def list_news():
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{BASE_URL}/news/")
        resp.raise_for_status()
        return resp.json()

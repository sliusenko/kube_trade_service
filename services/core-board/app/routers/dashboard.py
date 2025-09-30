from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from common.deps.db import get_session
from app.services.dashboard_service import get_dashboard_stats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats")
async def dashboard_stats(session: AsyncSession = Depends(get_session)):
    return await get_dashboard_stats(session)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List

from app.deps.db import get_session
from common.models.scheduler import ApschedulerJob
from common.schemas.scheduler import JobOut

router = APIRouter(prefix="/scheduler", tags=["Scheduler"])

@router.get("/jobs", response_model=List[JobOut])
async def list_jobs(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(ApschedulerJob))
    return res.scalars().all()

@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str, session: AsyncSession = Depends(get_session)):
    obj = await session.get(ApschedulerJob, job_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Job not found")
    await session.delete(obj)
    await session.commit()
    return {"ok": True}

from fastapi import APIRouter
from core_fetch.app.scheduler import scheduler

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/")
async def list_jobs():
    """
    List all active jobs from APScheduler
    """
    jobs_info = []
    for job in scheduler.get_jobs():
        jobs_info.append({
            "id": job.id,
            "name": job.name,
            "next_run_time": str(job.next_run_time),
            "trigger": str(job.trigger),
        })
    return jobs_info

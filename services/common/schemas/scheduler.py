# app/schemas/apscheduler_job.py
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ApschedulerJobBase(BaseModel):
    id: str
    next_run_time: Optional[float] = None
class ApschedulerJobCreate(ApschedulerJobBase):
    job_state: bytes  # у create можна приймати raw state
class ApschedulerJobOut(ApschedulerJobBase):
    model_config = ConfigDict(from_attributes=True)

    job_state: bytes

from pydantic import BaseModel
from typing import Optional

class JobOut(BaseModel):
    id: str
    next_run_time: Optional[float] = None
    job_state: bytes

    class Config:
        from_attributes = True

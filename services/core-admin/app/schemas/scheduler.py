from pydantic import BaseModel
from typing import Optional

class JobOut(BaseModel):
    id: str
    next_run_time: Optional[float] = None

    class Config:
        from_attributes = True

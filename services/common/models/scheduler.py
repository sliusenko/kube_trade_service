# app/models/apscheduler_job.py
from typing import Optional
from sqlalchemy import String, Float, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class ApschedulerJob(Base):
    __tablename__ = "apscheduler_jobs"

    id: Mapped[str] = mapped_column(String(191), primary_key=True)
    next_run_time: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    job_state: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    def __repr__(self) -> str:
        return f"<ApschedulerJob id={self.id} next_run_time={self.next_run_time}>"

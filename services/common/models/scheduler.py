from sqlalchemy import Column, String, Float, LargeBinary
from common.models.base import Base

class ApschedulerJob(Base):
    __tablename__ = "apscheduler_jobs"

    id = Column(String(191), primary_key=True)
    next_run_time = Column(Float, nullable=True)
    job_state = Column(LargeBinary, nullable=False)

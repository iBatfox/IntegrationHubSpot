from sqlalchemy import Column, Integer, String, DateTime

from app.models import Base


class PipelineStage(Base):
    __tablename__ = "pipeline_stages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    step_order = Column(Integer, nullable=False)

    hubspot_id = Column(String(255), nullable=True)
    source = Column(String(50), nullable=True)
    last_synced_at = Column(DateTime, nullable=True)

from datetime import datetime
from pydantic import BaseModel


class PipelineStageBase(BaseModel):
    name: str
    step_order: int
    hubspot_id: str | None = None
    source: str | None = None
    last_synced_at: datetime | None = None


class PipelineStageCreate(PipelineStageBase):
    pass


class PipelineStageUpdate(PipelineStageBase):
    pass


class PipelineStageRead(PipelineStageBase):
    id: int

    class Config:
        orm_mode = True

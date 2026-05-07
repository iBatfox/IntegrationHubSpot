from datetime import datetime
from pydantic import BaseModel, HttpUrl


class CompanyBase(BaseModel):
    name: str
    industry: str | None = None
    website: HttpUrl | None = None
    hubspot_id: str | None = None
    source: str | None = None
    last_synced_at: datetime | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

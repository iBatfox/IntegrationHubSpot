from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class DealBase(BaseModel):
    title: str
    amount: Decimal
    stage: str
    status: str
    contact_id: int | None = None
    company_id: int | None = None
    hubspot_id: str | None = None
    source: str | None = None
    last_synced_at: datetime | None = None


class DealCreate(DealBase):
    pass


class DealUpdate(DealBase):
    pass


class DealRead(DealBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

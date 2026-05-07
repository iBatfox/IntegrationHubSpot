from datetime import datetime
from pydantic import BaseModel


class EmailTemplateBase(BaseModel):
    name: str
    subject: str
    body: str


class EmailTemplateCreate(EmailTemplateBase):
    pass


class EmailTemplateRead(EmailTemplateBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    event_type: str
    payload: str | None = None
    contact_id: int | None = None
    deal_id: int | None = None


class ActivityRead(BaseModel):
    id: int
    event_type: str
    payload: str | None = None
    contact_id: int | None = None
    deal_id: int | None = None
    user_id: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True

from datetime import datetime
from pydantic import BaseModel, EmailStr


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr | None = None
    phone: str | None = None
    company_id: int | None = None
    hubspot_id: str | None = None
    source: str | None = None
    last_synced_at: datetime | None = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactRead(ContactBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

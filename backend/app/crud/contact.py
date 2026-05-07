from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


async def get_contacts(db: AsyncSession, skip: int = 0, limit: int = 50) -> list[Contact]:
    result = await db.execute(select(Contact).offset(skip).limit(limit))
    return result.scalars().all()


async def get_contact(db: AsyncSession, contact_id: int) -> Contact | None:
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    return result.scalars().first()


async def create_contact(db: AsyncSession, contact_in: ContactCreate) -> Contact:
    contact = Contact(**contact_in.model_dump())
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(db: AsyncSession, contact_id: int, contact_in: ContactUpdate) -> Contact | None:
    contact = await get_contact(db, contact_id)
    if not contact:
        return None
    for field, value in contact_in.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    await db.commit()
    await db.refresh(contact)
    return contact


async def delete_contact(db: AsyncSession, contact_id: int) -> bool:
    contact = await get_contact(db, contact_id)
    if not contact:
        return False
    await db.delete(contact)
    await db.commit()
    return True

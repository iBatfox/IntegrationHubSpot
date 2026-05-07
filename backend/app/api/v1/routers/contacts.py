from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.crud.contact import create_contact, delete_contact, get_contact, get_contacts, update_contact
from app.schemas.contact import ContactCreate, ContactRead, ContactUpdate

router = APIRouter()


@router.get("/", response_model=List[ContactRead])
async def read_contacts(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    return await get_contacts(db, skip=skip, limit=limit)


@router.post("/", response_model=ContactRead)
async def create_new_contact(
    contact_in: ContactCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return await create_contact(db, contact_in)


@router.get("/{contact_id}", response_model=ContactRead)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactRead)
async def update_existing_contact(
    contact_id: int,
    contact_in: ContactUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    contact = await update_contact(db, contact_id, contact_in)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=204)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    success = await delete_contact(db, contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return None

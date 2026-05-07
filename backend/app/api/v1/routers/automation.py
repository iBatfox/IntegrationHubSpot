from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.crud.automation import (
    create_email_template,
    create_event,
    get_activity_timeline,
    get_email_templates,
    get_email_template,
)
from app.schemas.automation import EmailTemplateCreate, EmailTemplateRead, EventCreate, ActivityRead

router = APIRouter()


@router.get("/templates", response_model=List[EmailTemplateRead])
async def read_templates(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    return await get_email_templates(db)


@router.post("/templates", response_model=EmailTemplateRead)
async def create_template(
    template_in: EmailTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return await create_email_template(db, template_in)


@router.get("/templates/{template_id}", response_model=EmailTemplateRead)
async def read_template(template_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    template = await get_email_template(db, template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email template not found")
    return template


@router.post("/webhook", status_code=202)
async def receive_webhook(event_in: EventCreate, db: AsyncSession = Depends(get_db)):
    await create_event(db, event_in)
    return {"status": "accepted"}


@router.get("/timeline", response_model=List[ActivityRead])
async def activity_timeline(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    return await get_activity_timeline(db)

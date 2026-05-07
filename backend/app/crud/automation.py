from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity
from app.models.email_template import EmailTemplate
from app.schemas.automation import EmailTemplateCreate, EventCreate


async def get_email_templates(db: AsyncSession) -> list[EmailTemplate]:
    result = await db.execute(select(EmailTemplate).order_by(EmailTemplate.created_at.desc()))
    return result.scalars().all()


async def get_email_template(db: AsyncSession, template_id: int) -> EmailTemplate | None:
    result = await db.execute(select(EmailTemplate).where(EmailTemplate.id == template_id))
    return result.scalars().first()


async def create_email_template(db: AsyncSession, template_in: EmailTemplateCreate) -> EmailTemplate:
    template = EmailTemplate(**template_in.model_dump())
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template


async def create_event(db: AsyncSession, event_in: EventCreate) -> Activity:
    activity = Activity(**event_in.model_dump())
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity


async def get_activity_timeline(db: AsyncSession) -> list[Activity]:
    result = await db.execute(select(Activity).order_by(Activity.created_at.desc()).limit(100))
    return result.scalars().all()

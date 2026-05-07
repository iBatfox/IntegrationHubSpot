from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.deal import Deal
from app.schemas.deal import DealCreate, DealUpdate


async def get_deals(db: AsyncSession, skip: int = 0, limit: int = 50) -> list[Deal]:
    result = await db.execute(select(Deal).offset(skip).limit(limit))
    return result.scalars().all()


async def get_deal(db: AsyncSession, deal_id: int) -> Deal | None:
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    return result.scalars().first()


async def create_deal(db: AsyncSession, deal_in: DealCreate) -> Deal:
    deal = Deal(**deal_in.model_dump())
    db.add(deal)
    await db.commit()
    await db.refresh(deal)
    return deal


async def update_deal(db: AsyncSession, deal_id: int, deal_in: DealUpdate) -> Deal | None:
    deal = await get_deal(db, deal_id)
    if not deal:
        return None
    for field, value in deal_in.model_dump(exclude_unset=True).items():
        setattr(deal, field, value)
    await db.commit()
    await db.refresh(deal)
    return deal


async def delete_deal(db: AsyncSession, deal_id: int) -> bool:
    deal = await get_deal(db, deal_id)
    if not deal:
        return False
    await db.delete(deal)
    await db.commit()
    return True

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity
from app.models.contact import Contact
from app.models.deal import Deal


async def get_deals_by_stage(db: AsyncSession) -> dict[str, int]:
    result = await db.execute(select(Deal.stage, func.count(Deal.id)).group_by(Deal.stage))
    return {stage: count for stage, count in result.all()}


async def get_revenue_overview(db: AsyncSession) -> float:
    result = await db.execute(select(func.coalesce(func.sum(Deal.amount), 0)))
    return float(result.scalar_one())


async def count_active_contacts(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(Contact.id)).where(Contact.email.is_not(None)))
    return int(result.scalar_one())


async def get_conversion_rate(db: AsyncSession) -> float:
    total_deals = await db.execute(select(func.count(Deal.id)))
    won_deals = await db.execute(select(func.count(Deal.id)).where(Deal.status == "Won"))
    total = int(total_deals.scalar_one())
    won = int(won_deals.scalar_one())
    return float(won) / total * 100 if total else 0.0

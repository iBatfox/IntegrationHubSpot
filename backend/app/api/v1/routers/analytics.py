from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.crud.analytics import count_active_contacts, get_deals_by_stage, get_revenue_overview, get_conversion_rate
from app.schemas.analytics import AnalyticsOverview

router = APIRouter()


@router.get("/overview", response_model=AnalyticsOverview)
async def read_overview(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    return AnalyticsOverview(
        deals_by_stage=await get_deals_by_stage(db),
        revenue=await get_revenue_overview(db),
        conversion_rate=await get_conversion_rate(db),
        active_contacts=await count_active_contacts(db),
    )

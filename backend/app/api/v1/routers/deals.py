from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.crud.deal import create_deal, delete_deal, get_deal, get_deals, update_deal
from app.schemas.deal import DealCreate, DealRead, DealUpdate

router = APIRouter()


@router.get("/", response_model=List[DealRead])
async def read_deals(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    return await get_deals(db, skip=skip, limit=limit)


@router.post("/", response_model=DealRead)
async def create_new_deal(
    deal_in: DealCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return await create_deal(db, deal_in)


@router.get("/{deal_id}", response_model=DealRead)
async def read_deal(deal_id: int, db: AsyncSession = Depends(get_db)):
    deal = await get_deal(db, deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.put("/{deal_id}", response_model=DealRead)
async def update_existing_deal(
    deal_id: int,
    deal_in: DealUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    deal = await update_deal(db, deal_id, deal_in)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.delete("/{deal_id}", status_code=204)
async def remove_deal(deal_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    success = await delete_deal(db, deal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Deal not found")
    return None

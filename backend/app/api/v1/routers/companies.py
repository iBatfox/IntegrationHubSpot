from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.crud.company import create_company, delete_company, get_company, get_companies, update_company
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate

router = APIRouter()


@router.get("/", response_model=List[CompanyRead])
async def read_companies(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    return await get_companies(db, skip=skip, limit=limit)


@router.post("/", response_model=CompanyRead)
async def create_new_company(
    company_in: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return await create_company(db, company_in)


@router.get("/{company_id}", response_model=CompanyRead)
async def read_company(company_id: int, db: AsyncSession = Depends(get_db)):
    company = await get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.put("/{company_id}", response_model=CompanyRead)
async def update_existing_company(
    company_id: int,
    company_in: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    company = await update_company(db, company_id, company_in)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.delete("/{company_id}", status_code=204)
async def remove_company(company_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    success = await delete_company(db, company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Company not found")
    return None

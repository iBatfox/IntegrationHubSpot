from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


async def get_companies(db: AsyncSession, skip: int = 0, limit: int = 50) -> list[Company]:
    result = await db.execute(select(Company).offset(skip).limit(limit))
    return result.scalars().all()


async def get_company(db: AsyncSession, company_id: int) -> Company | None:
    result = await db.execute(select(Company).where(Company.id == company_id))
    return result.scalars().first()


async def create_company(db: AsyncSession, company_in: CompanyCreate) -> Company:
    company = Company(**company_in.model_dump())
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company


async def update_company(db: AsyncSession, company_id: int, company_in: CompanyUpdate) -> Company | None:
    company = await get_company(db, company_id)
    if not company:
        return None
    for field, value in company_in.model_dump(exclude_unset=True).items():
        setattr(company, field, value)
    await db.commit()
    await db.refresh(company)
    return company


async def delete_company(db: AsyncSession, company_id: int) -> bool:
    company = await get_company(db, company_id)
    if not company:
        return False
    await db.delete(company)
    await db.commit()
    return True

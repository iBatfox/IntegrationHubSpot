from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.crud.pipeline import create_pipeline_stage, delete_pipeline_stage, get_pipeline_stage, get_pipeline_stages, update_pipeline_stage
from app.schemas.pipeline import PipelineStageCreate, PipelineStageRead, PipelineStageUpdate

router = APIRouter()


@router.get("/", response_model=List[PipelineStageRead])
async def read_pipeline_stages(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    return await get_pipeline_stages(db, skip=skip, limit=limit)


@router.post("/", response_model=PipelineStageRead)
async def create_stage(
    stage_in: PipelineStageCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return await create_pipeline_stage(db, stage_in)


@router.get("/{stage_id}", response_model=PipelineStageRead)
async def read_stage(stage_id: int, db: AsyncSession = Depends(get_db)):
    stage = await get_pipeline_stage(db, stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Pipeline stage not found")
    return stage


@router.put("/{stage_id}", response_model=PipelineStageRead)
async def update_stage(
    stage_id: int,
    stage_in: PipelineStageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    stage = await update_pipeline_stage(db, stage_id, stage_in)
    if not stage:
        raise HTTPException(status_code=404, detail="Pipeline stage not found")
    return stage


@router.delete("/{stage_id}", status_code=204)
async def remove_stage(stage_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    success = await delete_pipeline_stage(db, stage_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pipeline stage not found")
    return None

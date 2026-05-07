from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pipeline import PipelineStage
from app.schemas.pipeline import PipelineStageCreate, PipelineStageUpdate


async def get_pipeline_stages(db: AsyncSession, skip: int = 0, limit: int = 50) -> list[PipelineStage]:
    result = await db.execute(select(PipelineStage).order_by(PipelineStage.step_order).offset(skip).limit(limit))
    return result.scalars().all()


async def get_pipeline_stage(db: AsyncSession, stage_id: int) -> PipelineStage | None:
    result = await db.execute(select(PipelineStage).where(PipelineStage.id == stage_id))
    return result.scalars().first()


async def create_pipeline_stage(db: AsyncSession, stage_in: PipelineStageCreate) -> PipelineStage:
    stage = PipelineStage(**stage_in.model_dump())
    db.add(stage)
    await db.commit()
    await db.refresh(stage)
    return stage


async def update_pipeline_stage(db: AsyncSession, stage_id: int, stage_in: PipelineStageUpdate) -> PipelineStage | None:
    stage = await get_pipeline_stage(db, stage_id)
    if not stage:
        return None
    for field, value in stage_in.model_dump(exclude_unset=True).items():
        setattr(stage, field, value)
    await db.commit()
    await db.refresh(stage)
    return stage


async def delete_pipeline_stage(db: AsyncSession, stage_id: int) -> bool:
    stage = await get_pipeline_stage(db, stage_id)
    if not stage:
        return False
    await db.delete(stage)
    await db.commit()
    return True

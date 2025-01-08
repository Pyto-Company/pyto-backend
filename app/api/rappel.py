from fastapi import APIRouter, Query, Depends
from typing import Annotated
from model.rappel import Rappel
from repository.rappel import RappelRepository
from database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/rappel", tags=["rappel"])

@router.post("/")
async def create(
    rappel: Rappel,
    session: AsyncSession = Depends(get_session)
) -> Rappel:
    repository = RappelRepository(session)
    return await repository.create(rappel)

@router.get("/")
async def get_all(
    session: AsyncSession = Depends(get_session),
    offset: int = 0, 
    limit: Annotated[int, Query(le=100)] = 100
) -> list[Rappel]:
    repository = RappelRepository(session)
    return await repository.get_all(offset, limit)

@router.get("/{rappel_id}")
async def get_by_id(
    rappel_id: int,
    session: AsyncSession = Depends(get_session)
) -> Rappel:
    repository = RappelRepository(session)
    return await repository.get_by_id(rappel_id)

@router.put("/{rappel_id}")
async def update(
    rappel_id: int,
    updated_data: dict,
    session: AsyncSession = Depends(get_session)
) -> Rappel:
    repository = RappelRepository(session)
    return await repository.update(rappel_id, updated_data)

@router.delete("/{rappel_id}")
async def delete(
    rappel_id: int,
    session: AsyncSession = Depends(get_session)
) -> dict:
    repository = RappelRepository(session)
    return await repository.delete(rappel_id)
from fastapi import APIRouter, Query, Depends
from typing import Annotated
from model.plante import Plante
from repository.plante import PlanteRepository
from database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/plante", tags=["plante"])

@router.get("/")
async def get_all(
    session: AsyncSession = Depends(get_session),
    offset: int = 0, 
    limit: Annotated[int, Query(le=100)] = 100
) -> list[Plante]:
    repository = PlanteRepository(session)
    return await repository.get_all(offset, limit)

@router.post("/")
async def create(
    plante: Plante, 
    session: AsyncSession = Depends(get_session)
) -> Plante:
    repository = PlanteRepository(session)
    return await repository.create(plante)

@router.get("/{plante_id}")
async def get_by_id(
    plante_id: int,
    session: AsyncSession = Depends(get_session)
) -> Plante:
    repository = PlanteRepository(session)
    return await repository.get_by_id(plante_id)

@router.put("/{plante_id}")
async def update(
    plante_id: int,
    updated_data: dict,
    session: AsyncSession = Depends(get_session)
) -> Plante:
    repository = PlanteRepository(session)
    return await repository.update(plante_id, updated_data)

@router.delete("/{plante_id}")
async def delete(
    plante_id: int,
    session: AsyncSession = Depends(get_session)
) -> dict:
    repository = PlanteRepository(session)
    return await repository.delete(plante_id)
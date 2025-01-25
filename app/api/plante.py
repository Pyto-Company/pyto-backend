from fastapi import APIRouter, Query, Depends
from typing import Annotated
from repository.rappel import RappelRepository
from repository.scan import ScanRepository
from service.plante import PlanteService
from model.plante import Plante
from repository.plante import PlanteRepository
from database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import APIRouter, Request, Depends
from dto.plante_jardin import PlanteJardinDTO
from database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/plante", tags=["plante"])

@router.get("/")
async def get_all(
    session: AsyncSession = Depends(get_session),
    offset: int = 0, 
    limit: Annotated[int, Query(le=100)] = 100
) -> list[Plante]:
    return await PlanteRepository(session).get_all(offset, limit)

@router.post("/")
async def create(
    plante: Plante, 
    session: AsyncSession = Depends(get_session)
) -> Plante:
    return await PlanteRepository(session).create(plante)

@router.get("/{plante_id}")
async def get_by_id(
    plante_id: int,
    session: AsyncSession = Depends(get_session)
) -> Plante:
    return await PlanteRepository(session).get_by_id(plante_id)

@router.put("/{plante_id}")
async def update(
    plante_id: int,
    updated_data: dict,
    session: AsyncSession = Depends(get_session)
) -> Plante:
    return await PlanteRepository(session).update(plante_id, updated_data)

@router.delete("/{plante_id}")
async def delete(
    plante_id: int,
    session: AsyncSession = Depends(get_session)
) -> dict:
    return await PlanteRepository(session).delete(plante_id)

@router.get("/jardin", response_model=List[PlanteJardinDTO])
async def getMonJardin(request: Request, session: AsyncSession = Depends(get_session)):
    user_id = request.state.user_id
    return await PlanteRepository(session).get_jardin(user_id)

@router.get("/{plante_id}/rappels")
async def getRappels(plante_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    return await RappelRepository(session).get_rappels_by_plante_id(plante_id)

@router.get("/plante/{plante_id}/scans")
async def getScans(plante_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    return await ScanRepository(session).get_scans_by_plante_id(plante_id)


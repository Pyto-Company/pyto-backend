from fastapi import APIRouter, Query, Depends
from typing import Annotated
from app.repository.rappel import RappelRepository
from app.repository.scan import ScanRepository
from app.service.plante import PlanteService
from app.model.plante import Plante
from app.repository.plante import PlanteRepository
from app.database.database import get_session
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Request, Depends
from app.dto.PlanteJardinDTO import PlanteJardinDTO
from app.database.database import get_session
from sqlalchemy.orm import Session

router = APIRouter(prefix="/plante", tags=["plante"])

@router.get("/")
def get_all(
    session: Session = Depends(get_session),
    offset: int = 0, 
    limit: Annotated[int, Query(le=100)] = 100
) -> list[Plante]:
    return PlanteRepository(session).get_all(offset, limit)

@router.post("/")
def create(
    plante: Plante, 
    session: Session = Depends(get_session)
) -> Plante:
    return PlanteRepository(session).create(plante)

@router.get("/{plante_id}")
def get_by_id(
    plante_id: int,
    session: Session = Depends(get_session)
) -> Plante:
    return PlanteRepository(session).get_by_id(plante_id)

@router.put("/{plante_id}")
def update(
    plante_id: int,
    updated_data: dict,
    session: Session = Depends(get_session)
) -> Plante:
    return PlanteRepository(session).update(plante_id, updated_data)

@router.delete("/{plante_id}")
def delete(
    plante_id: int,
    session: Session = Depends(get_session)
) -> dict:
    return PlanteRepository(session).delete(plante_id)

@router.get("/jardin", response_model=List[PlanteJardinDTO])
def getMonJardin(request: Request, session: Session = Depends(get_session)):
    user_uid = request.state.user_uid
    return PlanteRepository(session).get_jardin(user_uid)

@router.get("/{plante_id}/rappels")
def getRappels(plante_id: int, request: Request, session: Session = Depends(get_session)):
    return RappelRepository(session).get_rappels_by_plante_id(plante_id)

@router.get("/plante/{plante_id}/scans")
def getScans(plante_id: int, request: Request, session: Session = Depends(get_session)):
    return ScanRepository(session).get_scans_by_plante_id(plante_id)


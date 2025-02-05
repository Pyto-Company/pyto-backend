from datetime import time
from fastapi import APIRouter, Depends, Request
from app.dto.RappelPrevuDTO import RappelPrevuDTO
from app.model.rappel import Rappel
from app.repository.rappel import RappelRepository
from app.database.database import get_session
from sqlalchemy.orm import Session

router = APIRouter(prefix="/rappel", tags=["rappel"])

@router.post("/")
def create(
    rappel: Rappel,
    session: Session = Depends(get_session)
) -> Rappel:
    rappel.heure = time.fromisoformat(rappel.heure)
    return RappelRepository(session).create(rappel)

@router.get("/")
def get_rappels(
    request: Request,
    session: Session = Depends(get_session)
) -> list[RappelPrevuDTO]:
    user_uid = request.state.user_uid
    return RappelRepository(session).get_rappels_by_user_id(user_uid)

@router.get("/{rappel_id}")
def get_by_id(
    rappel_id: int,
    session: Session = Depends(get_session)
) -> Rappel:
    return RappelRepository(session).get_by_id(rappel_id)

@router.put("/{rappel_id}")
def update(
    rappel_id: int,
    updated_data: dict,
    session: Session = Depends(get_session)
) -> Rappel:
    return RappelRepository(session).update(rappel_id, updated_data)

@router.delete("/{rappel_id}")
def delete(
    rappel_id: int,
    session: Session = Depends(get_session)
) -> dict:
    return RappelRepository(session).delete(rappel_id)


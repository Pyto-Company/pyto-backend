from datetime import time
from fastapi import APIRouter, Depends, Request
from app.dto.RappelPrevuDTO import RappelPrevuDTO
from app.model.rappel import Rappel
from app.repository.rappel import RappelRepository
from app.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/rappel", tags=["rappel"])

@router.post("/")
async def create(
    rappel: Rappel,
    session: AsyncSession = Depends(get_session)
) -> Rappel:
    rappel.heure = time.fromisoformat(rappel.heure)
    return await RappelRepository(session).create(rappel)

@router.get("/")
async def get_rappels(
    request: Request,
    session: AsyncSession = Depends(get_session)
) -> list[RappelPrevuDTO]:
    user_id = request.state.user_id
    return await RappelRepository(session).get_rappels_by_user_id(user_id)

@router.get("/{rappel_id}")
async def get_by_id(
    rappel_id: int,
    session: AsyncSession = Depends(get_session)
) -> Rappel:
    return await RappelRepository(session).get_by_id(rappel_id)

@router.put("/{rappel_id}")
async def update(
    rappel_id: int,
    updated_data: dict,
    session: AsyncSession = Depends(get_session)
) -> Rappel:
    return await RappelRepository(session).update(rappel_id, updated_data)

@router.delete("/{rappel_id}")
async def delete(
    rappel_id: int,
    session: AsyncSession = Depends(get_session)
) -> dict:
    return await RappelRepository(session).delete(rappel_id)


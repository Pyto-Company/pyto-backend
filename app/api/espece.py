from fastapi import APIRouter, Query, Depends
from typing import List
from dto.EspeceDTO import EspeceDTO
from database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from repository.espece import EspeceRepository

router = APIRouter(prefix="/espece", tags=["espece"])

@router.get("/moment", response_model=List[EspeceDTO])
async def getPlantesMoment(
    session: AsyncSession = Depends(get_session)
):
    return await EspeceRepository(session).getPlantesMoment()

@router.get("/search", response_model=List[EspeceDTO])
async def search_especes(
    q: str = Query(..., description="Terme de recherche pour le nom commun"),
    session: AsyncSession = Depends(get_session)
):
    """
    Recherche les espèces dont le nom commun commence par la chaîne de caractères fournie
    """
    return await EspeceRepository(session).search_by_nom_commun(q)
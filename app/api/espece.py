from fastapi import APIRouter, Query, Depends
from typing import List
from app.service.plante import PlanteService
from app.repository.entretien import EntretienRepository
from app.repository.maladie import MaladieRepository
from app.dto.EspeceDTO import EspeceDTO
from app.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.espece import EspeceRepository

router = APIRouter(prefix="/espece", tags=["espece"])


@router.get("/{espece_id}")
async def getEspece(
    espece_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await EspeceRepository(session).get_by_id(espece_id)

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

@router.get("/{espece_id}/maladies")
async def getEspeceMaladies(
    espece_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await MaladieRepository(session).get_maladies_by_espece_id(espece_id)


@router.get("/{espece_id}/entretiens")
async def getEspeceEntretiens(
    espece_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await PlanteService(session).getEntretiensPrincipaux(espece_id)

@router.get("/{espece_id}/conditions-meteo")
async def getEspeceConditionsMeteo(
    espece_id: int,
    session: AsyncSession = Depends(get_session)
):
    pass





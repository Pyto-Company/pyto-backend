from fastapi import APIRouter, Depends
from dto.ConnexionDTO import ConnexionDTO
from service.connexion import ConnexionService
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session

router = APIRouter(prefix="/connexion", tags=["connexion"])

@router.post("/")
async def login_for_access_token(infoConnexion: ConnexionDTO, session: AsyncSession = Depends(get_session)):
    return await ConnexionService(session).login(infoConnexion)

@router.post("/refresh-token")
async def refresh_access_token(refresh_token: str):
    return ConnexionService.refresh_access_token(refresh_token)
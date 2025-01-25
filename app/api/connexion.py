from fastapi import APIRouter, Depends
from app.dto.ConnexionDTO import ConnexionEmailDTO, ConnexionSocialDTO
from app.service.connexion import ConnexionService
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_session

router = APIRouter(prefix="/connexion", tags=["connexion"])

@router.post("/email")
async def login_email(infoConnexion: ConnexionEmailDTO, session: AsyncSession = Depends(get_session)):
    return await ConnexionService(session).login(infoConnexion)

@router.post("/google")
async def login_google(infoConnexion: ConnexionSocialDTO, session: AsyncSession = Depends(get_session)):
    return await ConnexionService(session).login_social(infoConnexion)

@router.post("/facebook")
async def login_facebook(infoConnexion: ConnexionSocialDTO, session: AsyncSession = Depends(get_session)):
    return await ConnexionService(session).login_social(infoConnexion)

@router.post("/apple")
async def login_apple(infoConnexion: ConnexionSocialDTO, session: AsyncSession = Depends(get_session)):
    return await ConnexionService(session).login_social(infoConnexion)

@router.post("/refresh-token")
async def refresh_access_token(refresh_token: str):
    return ConnexionService.refresh_access_token(refresh_token)
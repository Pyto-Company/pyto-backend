from fastapi import APIRouter, Depends, Request
from model.utilisateur import ProviderType
from database.database import get_session
from dto.InscriptionDTO import InscriptionDTO, InscriptionEmailDTO, InscriptionSocialDTO
from client.google import GoogleClient
from service.utilisateur import UtilisateurService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/inscription", tags=["inscription"])

@router.post("/email")
async def inscription_email(request: InscriptionEmailDTO, session: AsyncSession = Depends(get_session)):
    return await UtilisateurService(session).createUser(request, ProviderType.EMAIL)

@router.post("/google")
async def inscription_google(request: InscriptionSocialDTO, session: AsyncSession = Depends(get_session)):
    return await UtilisateurService(session).createUser(request, ProviderType.GOOGLE)

@router.post("/facebook")
async def inscription_facebook(request: InscriptionSocialDTO, session: AsyncSession = Depends(get_session)):
    return await UtilisateurService(session).createUser(request, ProviderType.FACEBOOK)

@router.post("/apple")
async def inscription_apple(request: InscriptionSocialDTO, session: AsyncSession = Depends(get_session)):
    return await UtilisateurService(session).createUser(request, ProviderType.APPLE)

# Route pour démarrer le processus d'inscription avec Google
@router.get("/auth/google")
async def login_via_google(request: Request):
    return await GoogleClient.login_via_google(request)

# Callback après authentification avec Google
@router.get("/auth/google/callback")
async def google_callback(request: Request):
    return await GoogleClient.google_callback(request)
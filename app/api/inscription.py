from fastapi import APIRouter, Depends, Request
from database.database import get_session
from dto.InscriptionDTO import InscriptionDTO
from client.google import GoogleClient
from service.utilisateur import UtilisateurService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/inscription", tags=["inscription"])

@router.post("/")
async def inscription(request: InscriptionDTO, session: AsyncSession = Depends(get_session)):
    return await UtilisateurService(session).createUser(request)

# Route pour démarrer le processus d'inscription avec Google
@router.get("/auth/google")
async def login_via_google(request: Request):
    return await GoogleClient.login_via_google(request)

# Callback après authentification avec Google
@router.get("/auth/google/callback")
async def google_callback(request: Request):
    return await GoogleClient.google_callback(request)
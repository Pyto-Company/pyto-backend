from fastapi import APIRouter, Depends, Request
from app.model.utilisateur import ProviderType
from app.database.database import get_session
from app.dto.InscriptionDTO import InscriptionDTO, InscriptionEmailDTO, InscriptionSocialDTO
from app.client.google import GoogleClient
from app.service.utilisateur import UtilisateurService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/inscription", tags=["inscription"])

@router.post("/email")
def inscription_email(request: InscriptionEmailDTO, session: Session = Depends(get_session)):
    return UtilisateurService(session).createUser(request, ProviderType.EMAIL)

@router.post("/google")
def inscription_google(request: InscriptionSocialDTO, session: Session = Depends(get_session)):
    return UtilisateurService(session).createUser(request, ProviderType.GOOGLE)

@router.post("/facebook")
def inscription_facebook(request: InscriptionSocialDTO, session: Session = Depends(get_session)):
    return UtilisateurService(session).createUser(request, ProviderType.FACEBOOK)

@router.post("/apple")
def inscription_apple(request: InscriptionSocialDTO, session: Session = Depends(get_session)):
    return UtilisateurService(session).createUser(request, ProviderType.APPLE)

# Route pour démarrer le processus d'inscription avec Google
@router.get("/auth/google")
def login_via_google(request: Request):
    return GoogleClient.login_via_google(request)

# Callback après authentification avec Google
@router.get("/auth/google/callback")
def google_callback(request: Request):
    return GoogleClient.google_callback(request)
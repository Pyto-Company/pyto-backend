from fastapi import APIRouter, Depends
from app.dto.ConnexionDTO import ConnexionEmailDTO, ConnexionSocialDTO
from app.service.connexion import ConnexionService
from sqlalchemy.orm import Session
from app.database.database import get_session

router = APIRouter(prefix="/connexion", tags=["connexion"])

@router.post("/email")
def login_email(infoConnexion: ConnexionEmailDTO, session: Session = Depends(get_session)):
    return ConnexionService(session).login(infoConnexion)

@router.post("/google")
def login_google(infoConnexion: ConnexionSocialDTO, session: Session = Depends(get_session)):
    return ConnexionService(session).login_social(infoConnexion)

@router.post("/facebook")
def login_facebook(infoConnexion: ConnexionSocialDTO, session: Session = Depends(get_session)):
    return ConnexionService(session).login_social(infoConnexion)

@router.post("/apple")
def login_apple(infoConnexion: ConnexionSocialDTO, session: Session = Depends(get_session)):
    return ConnexionService(session).login_social(infoConnexion)

@router.post("/refresh-token")
def refresh_access_token(refresh_token: str):
    return ConnexionService.refresh_access_token(refresh_token)
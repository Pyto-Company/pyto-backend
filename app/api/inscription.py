from fastapi import APIRouter, Depends, Request
from app.database.database import get_session
from app.dto.InscriptionDTO import InscriptionDTO
from app.service.utilisateur import UtilisateurService
from sqlalchemy.orm import Session
from app.client.firebase import FirebaseClient

router = APIRouter(prefix="/inscription", tags=["inscription"])

@router.post("/")
def inscription(request: Request, inscription: InscriptionDTO, session: Session = Depends(get_session)):
    user_uid = request.state.user_uid
    return UtilisateurService(session).createUser(user_uid, inscription)

@router.post("/token/{user_uid}")
def inscription(user_uid: str):
    return FirebaseClient().get_token(user_uid)
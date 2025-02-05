from fastapi import APIRouter, Query, Depends, Request
from typing import Annotated
from app.dto.UtilisateurDTO import UtilisateurDTO
from app.model.utilisateur import Utilisateur
from app.database import database  
from sqlalchemy.orm import Session

from app.repository.utilisateur import UtilisateurRepository
from app.service.utilisateur import UtilisateurService

router = APIRouter(prefix="/utilisateur", tags=["utilisateur"])

@router.get("/me")
def getMe(request: Request, session: Session = Depends(database.get_session)) -> UtilisateurDTO:
    firebase_user_uid = request.state.user_uid
    return UtilisateurRepository(session).getMe(firebase_user_uid)

@router.delete("/{user_id}")
def deleteUser(user_id: int):
    return UtilisateurRepository.deleteUser()

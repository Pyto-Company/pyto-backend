from fastapi import APIRouter, Query, Depends, Request
from typing import Annotated
from app.dto.UtilisateurDTO import UtilisateurDTO
from app.model.utilisateur import Utilisateur
from app.database import database  
from sqlalchemy.orm import Session

from app.repository.utilisateur import UtilisateurRepository
from app.service.utilisateur import UtilisateurService

router = APIRouter(prefix="/utilisateur", tags=["utilisateur"])

@router.post("/")
def inscription(user: Utilisateur) -> Utilisateur:
    return UtilisateurService.CreateUser(user)

@router.get("/")
def readUsers(offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Utilisateur]:
    return UtilisateurRepository.getUsers(offset, limit)

@router.get("/me")
def getMe(request: Request, session: Session = Depends(database.get_session)) -> UtilisateurDTO:
    user_id = request.state.user_id
    return UtilisateurRepository(session).getMe(user_id)

@router.get("/{user_id}")
def readUser(user_id: int) -> Utilisateur:
    return UtilisateurRepository.getUserByUserId(user_id)

@router.delete("/{user_id}")
def deleteUser(user_id: int):
    return UtilisateurRepository.deleteUser()

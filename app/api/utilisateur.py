from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Annotated
from model.utilisateur import Utilisateur
from database import database  
from sqlmodel import select, Session

from repository.utilisateur import UtilisateurRepository
from service.utilisateur import UtilisateurService

router = APIRouter(prefix="/utilisateur", tags=["utilisateur"])

@router.post("/")
def inscription(user: Utilisateur) -> Utilisateur:
    return UtilisateurService.CreateUser(user)

@router.get("/")
def readUsers(offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Utilisateur]:
    return UtilisateurRepository.getUsers(offset, limit)

@router.get("/{user_id}")
def readUser(user_id: int) -> Utilisateur:
    return UtilisateurRepository.getUserByUserId(user_id)

@router.delete("/{user_id}")
def deleteUser(user_id: int):
    return UtilisateurRepository.deleteUser()

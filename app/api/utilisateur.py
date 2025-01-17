from fastapi import APIRouter, Query, Depends, Request
from typing import Annotated
from model.utilisateur import Utilisateur
from database import database  
from sqlalchemy.ext.asyncio import AsyncSession

from repository.utilisateur import UtilisateurRepository
from service.utilisateur import UtilisateurService

router = APIRouter(prefix="/utilisateur", tags=["utilisateur"])

@router.post("/")
def inscription(user: Utilisateur) -> Utilisateur:
    return UtilisateurService.CreateUser(user)

@router.get("/")
def readUsers(offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Utilisateur]:
    return UtilisateurRepository.getUsers(offset, limit)

@router.get("/me")
async def getMe(request: Request, session: AsyncSession = Depends(database.get_session)) -> Utilisateur:
    user_id = request.state.user_id
    return await UtilisateurRepository(session).getMe(user_id)

@router.get("/{user_id}")
def readUser(user_id: int) -> Utilisateur:
    return UtilisateurRepository.getUserByUserId(user_id)

@router.delete("/{user_id}")
def deleteUser(user_id: int):
    return UtilisateurRepository.deleteUser()

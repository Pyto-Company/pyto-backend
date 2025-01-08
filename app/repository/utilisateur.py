from typing import Annotated
from fastapi import Query, HTTPException
from sqlmodel import select
from model.utilisateur import Utilisateur
from repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class UtilisateurRepository(BaseRepository[Utilisateur]):
    def __init__(self, session: AsyncSession):
        super().__init__(Utilisateur, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Utilisateur]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, user_id: int) -> Utilisateur:
        return await super().get_by_id(user_id)

    async def create(self, user: Utilisateur) -> Utilisateur:
        return await super().create(user)

    async def delete(self, user_id: int) -> dict:
        return await super().delete(user_id)
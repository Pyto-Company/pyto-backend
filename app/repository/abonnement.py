from typing import Annotated
from fastapi import Query
from sqlmodel import select
from model.abonnement import Abonnement
from repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class AbonnementRepository(BaseRepository[Abonnement]):
    def __init__(self, session: AsyncSession):
        super().__init__(Abonnement, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Abonnement]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, abonnement_id: int) -> Abonnement:
        return await super().get_by_id(abonnement_id)

    async def create(self, abonnement: Abonnement) -> Abonnement:
        return await super().create(abonnement)

    async def delete(self, abonnement_id: int) -> dict:
        return await super().delete(abonnement_id)
    
    async def update(self, abonnement_id: int, updated_data: dict) -> Abonnement:
        return await super().update(abonnement_id, updated_data)
    
    async def get_abonnement_by_utilisateur_id(self, utilisateur_id: int) -> list[Abonnement]:
        query = select(Abonnement).where(Abonnement.utilisateur_id == utilisateur_id)
        result = await self.session.execute(query)
        return result.scalars().all()
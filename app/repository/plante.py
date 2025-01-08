from typing import Annotated
from model.plante import Plante
from repository.base import BaseRepository
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

class PlanteRepository(BaseRepository[Plante]):
    def __init__(self, session: AsyncSession):
        super().__init__(Plante, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Plante]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, plante_id: int) -> Plante:
        return await super().get_by_id(plante_id)

    async def create(self, plante: Plante) -> Plante:
        return await super().create(plante)

    async def delete(self, plante_id: int) -> dict:
        return await super().delete(plante_id)
    
    async def update(self, plante_id: int, updated_data: dict) -> Plante:
        return await super().update(plante_id, updated_data)
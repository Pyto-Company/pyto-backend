from typing import Annotated
from fastapi import Query
from model.rappel import Rappel
from repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class RappelRepository(BaseRepository[Rappel]):
    def __init__(self, session: AsyncSession):
        super().__init__(Rappel, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Rappel]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, rappel_id: int) -> Rappel:
        return await super().get_by_id(rappel_id)

    async def create(self, rappel: Rappel) -> Rappel:
        return await super().create(rappel)

    async def delete(self, rappel_id: int) -> dict:
        return await super().delete(rappel_id)
    
    async def update(self, rappel_id: int, updated_data: dict) -> Rappel:
        return await super().update(rappel_id, updated_data)
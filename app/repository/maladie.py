from typing import Annotated
from fastapi import Query
from sqlmodel import select
from model.maladie import Maladie
from repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class MaladieRepository(BaseRepository[Maladie]):
    def __init__(self, session: AsyncSession):
        super().__init__(Maladie, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Maladie]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, maladie_id: int) -> Maladie:
        return await super().get_by_id(maladie_id)

    async def create(self, maladie: Maladie) -> Maladie:
        return await super().create(maladie)

    async def delete(self, maladie_id: int) -> dict:
        return await super().delete(maladie_id)
    
    async def update(self, maladie_id: int, updated_data: dict) -> Maladie:
        return await super().update(maladie_id, updated_data)
    
    async def get_all_classe_ia(self) -> list[str]:
        query = select(getattr(Maladie, "classe_ia"))
        result = await self.session.execute(query)
        return [item[0] for item in result.all()]
    
    async def get_maladies_by_espece_id(self, espece_id: int) -> list[Maladie]:
        query = select(Maladie).where(Maladie.espece_id == espece_id)
        result = await self.session.execute(query)
        return result.scalars().all()
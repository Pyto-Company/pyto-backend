from typing import Annotated
from fastapi import Query
from sqlmodel import select
from model.espece import Espece
from repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class EspeceRepository(BaseRepository[Espece]):
    def __init__(self, session: AsyncSession):
        super().__init__(Espece, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Espece]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, espece_id: int) -> Espece:
        return await super().get_by_id(espece_id)

    async def create(self, espece: Espece) -> Espece:
        return await super().create(espece)

    async def delete(self, espece_id: int) -> dict:
        return await super().delete(espece_id)
    
    async def update(self, espece_id: int, updated_data: dict) -> Espece:
        return await super().update(espece_id, updated_data)
    
    async def get_all_classe_ia(self) -> list[str]:
        query = select(getattr(Espece, "classe_ia"))
        result = await self.session.execute(query)
        return [item[0] for item in result.all()]
    
    async def get_by_class_ia(self, classe_ia: str) -> list[Espece]:
        query = select(Espece).where(Espece.classe_ia == classe_ia)
        result = await self.session.execute(query)
        return result.scalars().all()
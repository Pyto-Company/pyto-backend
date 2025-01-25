from typing import Annotated
from fastapi import Query
from sqlmodel import select
from app.model.entretien import Entretien
from app.repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class EntretienRepository(BaseRepository[Entretien]):
    def __init__(self, session: AsyncSession):
        super().__init__(Entretien, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Entretien]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, entretien_id: int) -> Entretien:
        return await super().get_by_id(entretien_id)

    async def create(self, entretien: Entretien) -> Entretien:
        return await super().create(entretien)

    async def delete(self, entretien_id: int) -> dict:
        return await super().delete(entretien_id)
    
    async def update(self, entretien_id: int, updated_data: dict) -> Entretien:
        return await super().update(entretien_id, updated_data)
    
    async def get_entretiens_by_espece_id(self, espece_id: int) -> list[Entretien]:
        query = select(Entretien).where(Entretien.espece_id == espece_id)
        result = await self.session.execute(query)
        return result.scalars().all()
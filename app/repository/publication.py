from typing import Annotated
from fastapi import Query
from app.model.publication import Publication
from app.repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

class PublicationRepository(BaseRepository[Publication]):
    def __init__(self, session: AsyncSession):
        super().__init__(Publication, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Publication]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, publication_id: int) -> Publication:
        return await super().get_by_id(publication_id)

    async def create(self, publication: Publication) -> Publication:
        return await super().create(publication)

    async def delete(self, publication_id: int) -> dict:
        return await super().delete(publication_id)
    
    async def update(self, publication_id: int, updated_data: dict) -> Publication:
        return await super().update(publication_id, updated_data)

    async def get_publications_by_user_id(self, user_id: int) -> list[Publication]:
        query = select(Publication).where(Publication.utilisateur_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()
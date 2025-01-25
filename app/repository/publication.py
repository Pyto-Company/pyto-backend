from typing import Annotated
from fastapi import Query
from app.model.publication import Publication
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session
from sqlmodel import select

class PublicationRepository(BaseRepository[Publication]):
    def __init__(self, session: Session):
        super().__init__(Publication, session)

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Publication]:
        return super().get_all(offset, limit)

    def get_by_id(self, publication_id: int) -> Publication:
        return super().get_by_id(publication_id)

    def create(self, publication: Publication) -> Publication:
        return super().create(publication)

    def delete(self, publication_id: int) -> dict:
        return super().delete(publication_id)
    
    def update(self, publication_id: int, updated_data: dict) -> Publication:
        return super().update(publication_id, updated_data)

    def get_publications_by_user_id(self, user_id: int) -> list[Publication]:
        query = select(Publication).where(Publication.utilisateur_id == user_id)
        result = self.session.execute(query)
        return result.scalars().all()
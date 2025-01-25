from typing import Annotated
from fastapi import Query
from sqlmodel import select
from app.model.entretien import Entretien
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session

class EntretienRepository(BaseRepository[Entretien]):
    def __init__(self, session: Session):
        super().__init__(Entretien, session)

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Entretien]:
        return super().get_all(offset, limit)

    def get_by_id(self, entretien_id: int) -> Entretien:
        return super().get_by_id(entretien_id)

    def create(self, entretien: Entretien) -> Entretien:
        return super().create(entretien)

    def delete(self, entretien_id: int) -> dict:
        return super().delete(entretien_id)
    
    def update(self, entretien_id: int, updated_data: dict) -> Entretien:
        return super().update(entretien_id, updated_data)
    
    def get_entretiens_by_espece_id(self, espece_id: int) -> list[Entretien]:
        query = select(Entretien).where(Entretien.espece_id == espece_id)
        result = self.session.execute(query)
        return result.scalars().all()
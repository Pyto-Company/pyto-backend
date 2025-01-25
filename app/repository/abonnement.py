from typing import Annotated
from fastapi import Query
from sqlmodel import select
from app.model.abonnement import Abonnement
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session

class AbonnementRepository(BaseRepository[Abonnement]):
    def __init__(self, session: Session):
        super().__init__(Abonnement, session)

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Abonnement]:
        return super().get_all(offset, limit)

    def get_by_id(self, abonnement_id: int) -> Abonnement:
        return super().get_by_id(abonnement_id)

    def create(self, abonnement: Abonnement) -> Abonnement:
        return super().create(abonnement)

    def delete(self, abonnement_id: int) -> dict:
        return super().delete(abonnement_id)
    
    def update(self, abonnement_id: int, updated_data: dict) -> Abonnement:
        return super().update(abonnement_id, updated_data)
    
    def get_abonnement_by_utilisateur_id(self, utilisateur_id: int) -> list[Abonnement]:
        query = select(Abonnement).where(Abonnement.utilisateur_id == utilisateur_id)
        result = self.session.execute(query)
        return result.scalars().all()
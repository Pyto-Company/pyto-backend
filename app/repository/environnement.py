from typing import Annotated
from fastapi import Query
from sqlmodel import select
from app.model.environnement import Environnement
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session

class EnvironnementRepository(BaseRepository[Environnement]):
    def __init__(self, session: Session):
        super().__init__(Environnement, session)

    def get_environnements_by_espece_id(self, espece_id: int) -> list[Environnement]:
        query = select(Environnement).where(Environnement.espece_id == espece_id)
        result = self.session.execute(query)
        return result.scalars().all() 
from typing import Annotated
from fastapi import Query
from sqlmodel import select
from app.model.traitement import Traitement
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session

class TraitementRepository(BaseRepository[Traitement]):
    def __init__(self, session: Session):
        super().__init__(Traitement, session)

    def get_traitements_by_maladie_id(self, maladie_id: int) -> list[Traitement]:
        query = select(Traitement).where(Traitement.maladie_id == maladie_id)
        result = self.session.execute(query)
        return result.scalars().all() 
from typing import Annotated
from fastapi import Query
from sqlmodel import select
from app.model.symptome import Symptome
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session

class SymptomeRepository(BaseRepository[Symptome]):
    def __init__(self, session: Session):
        super().__init__(Symptome, session)

    def get_symptomes_by_maladie_id(self, maladie_id: int) -> list[Symptome]:
        query = select(Symptome).where(Symptome.maladie_id == maladie_id)
        result = self.session.execute(query)
        return result.scalars().all() 
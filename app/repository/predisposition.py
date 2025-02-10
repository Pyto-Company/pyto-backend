from typing import Annotated
from fastapi import Query
from sqlmodel import select
from app.model.predisposition import Predisposition
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session

class PredispositionRepository(BaseRepository[Predisposition]):
    def __init__(self, session: Session):
        super().__init__(Predisposition, session)

    def get_predispositions_by_maladie_id(self, maladie_id: int) -> list[Predisposition]:
        query = select(Predisposition).where(Predisposition.maladie_id == maladie_id)
        result = self.session.execute(query)
        return result.scalars().all() 
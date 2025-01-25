from typing import Annotated
from fastapi import Query
from sqlmodel import select
from app.model.maladie import Maladie
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session

class MaladieRepository(BaseRepository[Maladie]):
    def __init__(self, session: Session):
        super().__init__(Maladie, session)

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Maladie]:
        return super().get_all(offset, limit)

    def get_by_id(self, maladie_id: int) -> Maladie:
        return super().get_by_id(maladie_id)

    def create(self, maladie: Maladie) -> Maladie:
        return super().create(maladie)

    def delete(self, maladie_id: int) -> dict:
        return super().delete(maladie_id)
    
    def update(self, maladie_id: int, updated_data: dict) -> Maladie:
        return super().update(maladie_id, updated_data)
    
    def get_all_classe_ia(self) -> list[str]:
        query = select(getattr(Maladie, "classe_ia"))
        result = self.session.execute(query)
        return [item[0] for item in result.all()]
    
    def get_maladies_by_espece_id(self, espece_id: int) -> list[Maladie]:
        query = select(Maladie).where(Maladie.espece_id == espece_id)
        result = self.session.execute(query)
        return result.scalars().all()
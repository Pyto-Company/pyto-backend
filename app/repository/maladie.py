from typing import Annotated, List
from fastapi import Query
from sqlmodel import select
from app.model.maladie import Maladie
from app.repository.base import BaseRepository

class MaladieRepository(BaseRepository[Maladie]):

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Maladie]:
        return self.get_all(Maladie, offset, limit)

    def get_by_id(self, maladie_id: int) -> Maladie:
        return self.get_by_id(Maladie, maladie_id)

    def create(self, maladie: Maladie) -> Maladie:
        return self.create(maladie)

    def delete(self, maladie_id: int) -> dict:
        return self.delete(Maladie, maladie_id)
    
    def update(self, maladie_id: int, updated_data: dict) -> Maladie:
        return self.update(Maladie, maladie_id, updated_data)
    
    def get_all_classe_ia(self) -> list[str]:
        # Use SQLAlchemy's distinct to get all unique values for the specified column
        query = select(getattr(Maladie, "classe_ia"))
        result = self.session.exec(query).all()

        # Extract the values from the result
        return [item[0] for item in result]
    
    async def get_maladies_by_espece_id(self, espece_id):
        query = select(Maladie).where(Maladie.espece_id == espece_id)
        return self.session.exec(query).all()
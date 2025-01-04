from typing import Annotated
from fastapi import Query
from sqlmodel import select
from app.model.espece import Espece
from app.repository.base import BaseRepository

class EspeceRepository(BaseRepository[Espece]):

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Espece]:
        return self.get_all(Espece, offset, limit)

    def get_by_id(self, espece_id: int) -> Espece:
        return self.get_by_id(Espece, espece_id)

    def create(self, espece: Espece) -> Espece:
        return self.create(espece)

    def delete(self, espece_id: int) -> dict:
        return self.delete(Espece, espece_id)
    
    def update(self, espece_id: int, updated_data: dict) -> Espece:
        return self.update(Espece, espece_id, updated_data)
    
    def get_all_classe_ia(self) -> list[str]:
        # Use SQLAlchemy's distinct to get all unique values for the specified column
        query = select(getattr(Espece, "classe_ia"))
        result = self.session.exec(query).all()

        # Extract the values from the result
        return [item[0] for item in result]
    
    def get_by_class_ia(self, classe_ia: str) -> Espece:
        query = query(Espece).filter(Espece.classe_ia == classe_ia)
        return self.session.exec(query).all()
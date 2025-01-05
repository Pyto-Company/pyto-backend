from typing import Annotated
from fastapi import Query
from torch import select
from model.entretien import Entretien
from repository.base import BaseRepository

class EntretienRepository(BaseRepository[Entretien]):

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Entretien]:
        return self.get_all(Entretien, offset, limit)

    def get_by_id(self, entretien_id: int) -> Entretien:
        return self.get_by_id(Entretien, entretien_id)

    def create(self, entretien: Entretien) -> Entretien:
        return self.create(entretien)

    def delete(self, entretien_id: int) -> dict:
        return self.delete(Entretien, entretien_id)
    
    def update(self, entretien_id: int, updated_data: dict) -> Entretien:
        return self.update(Entretien, entretien_id, updated_data)
    
    async def get_entretien_by_espece_id(self, espece_id):
        query = select(Entretien).where(Entretien.espece_id == espece_id)
        return self.session.exec(query).all()
from typing import Annotated
from fastapi import Query
from model.plante import Plante
from repository.base import BaseRepository

class PlanteRepository(BaseRepository[Plante]):

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Plante]:
        return self.get_all(Plante, offset, limit)

    def get_by_id(self, plante_id: int) -> Plante:
        return self.get_by_id(Plante, plante_id)

    def create(self, plante: Plante) -> Plante:
        return self.create(plante)

    def delete(self, plante_id: int) -> dict:
        return self.delete(Plante, plante_id)
    
    def update(self, plante_id: int, updated_data: dict) -> Plante:
        return self.update(Plante, plante_id, updated_data)
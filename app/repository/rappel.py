from typing import Annotated
from fastapi import Query
from model.rappel import Rappel
from repository.base import BaseRepository

class RappelRepository(BaseRepository[Rappel]):

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Rappel]:
        return self.get_all(Rappel, offset, limit)

    def get_by_id(self, rappel_id: int) -> Rappel:
        return self.get_by_id(Rappel, rappel_id)

    def create(self, rappel: Rappel) -> Rappel:
        return self.create(rappel)

    def delete(self, rappel_id: int) -> dict:
        return self.delete(Rappel, rappel_id)
    
    def update(self, rappel_id: int, updated_data: dict) -> Rappel:
        return self.update(Rappel, rappel_id, updated_data)
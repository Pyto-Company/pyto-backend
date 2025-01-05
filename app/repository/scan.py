from typing import Annotated
from fastapi import Query
from model.scan import Scan
from repository.base import BaseRepository

class ScanRepository(BaseRepository[Scan]):

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Scan]:
        return self.get_all(Scan, offset, limit)

    def get_by_id(self, scan_maladie_id: int) -> Scan:
        return self.get_by_id(Scan, scan_maladie_id)

    def create(self, scan_maladie: Scan) -> Scan:
        return self.create(scan_maladie)

    def delete(self, scan_maladie_id: int) -> dict:
        return self.delete(Scan, scan_maladie_id)
    
    def update(self, scan_maladie_id: int, updated_data: dict) -> Scan:
        return self.update(Scan, scan_maladie_id, updated_data)
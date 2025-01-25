from typing import Annotated
from fastapi import Query
from app.model.scan import Scan
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlmodel import select

class ScanRepository(BaseRepository[Scan]):
    def __init__(self, session: Session):
        super().__init__(Scan, session)

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Scan]:
        return super().get_all(offset, limit)

    def get_by_id(self, scan_id: int) -> Scan:
        return super().get_by_id(scan_id)

    def create(self, scan: Scan) -> Scan:
        return super().create(scan)

    def delete(self, scan_id: int) -> dict:
        return super().delete(scan_id)
    
    def update(self, scan_id: int, updated_data: dict) -> Scan:
        return super().update(scan_id, updated_data)

    def get_scans_by_plante_id(self, plante_id: int) -> list[Scan]:
        query = select(Scan).where(Scan.plante_id == plante_id).order_by(Scan.date_creation.desc())
        result = self.session.execute(query)
        return result.scalars().all()
from typing import Annotated
from fastapi import Query
from app.model.scan import Scan
from app.repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlmodel import select

class ScanRepository(BaseRepository[Scan]):
    def __init__(self, session: AsyncSession):
        super().__init__(Scan, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Scan]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, scan_id: int) -> Scan:
        return await super().get_by_id(scan_id)

    async def create(self, scan: Scan) -> Scan:
        return await super().create(scan)

    async def delete(self, scan_id: int) -> dict:
        return await super().delete(scan_id)
    
    async def update(self, scan_id: int, updated_data: dict) -> Scan:
        return await super().update(scan_id, updated_data)

    async def get_scans_by_plante_id(self, plante_id: int) -> list[Scan]:
        query = select(Scan).where(Scan.plante_id == plante_id).order_by(Scan.date_creation.desc())
        result = await self.session.execute(query)
        return result.scalars().all()
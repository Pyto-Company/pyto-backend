from typing import Annotated
from fastapi import Query
from model.scan import Scan
from repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

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
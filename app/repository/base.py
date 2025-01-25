from typing import TypeVar, Generic, Type
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[T]:
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, id: int) -> T:
        result = await self.session.get(self.model, id)
        if not result:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} non trouvé")
        return result

    async def create(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def delete(self, id: int) -> dict:
        try:
            entity = await self.session.get(self.model, id)
            await self.session.delete(entity)
            await self.session.commit()
            return {"ok": True}
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def update(self, id: int, data: dict) -> T:
        entity = await self.session.get(self.model, id)
        for key, value in data.items():
            setattr(entity, key, value)
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
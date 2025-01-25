from typing import TypeVar, Generic, Type
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.orm import Session

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def get_all(self, offset: int = 0, limit: int = 100) -> list[T]:
        result = self.session.execute(select(self.model).offset(offset).limit(limit))
        return result.scalars().all()

    def get_by_id(self, id: int) -> T:
        result = self.session.get(self.model, id)
        if not result:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} non trouvé")
        return result

    def create(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, id: int) -> dict:
        try:
            entity = self.session.get(self.model, id)
            self.session.delete(entity)
            self.session.commit()
            return {"ok": True}
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def update(self, id: int, data: dict) -> T:
        entity = self.session.get(self.model, id)
        for key, value in data.items():
            setattr(entity, key, value)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity
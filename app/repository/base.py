from typing import TypeVar, Generic, Annotated
from fastapi import Depends, Query, HTTPException
from sqlmodel import Session, select
from database.database import get_session

# Define a generic type for your entities
T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_all(
        self,
        model: type[T],
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
    ) -> list[T]:
        return self.session.exec(select(model).offset(offset).limit(limit)).all()

    def get_by_id(self, model: type[T], entity_id: int) -> T:
        entity = self.session.get(model, entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        return entity

    def create(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, model: type[T], entity_id: int) -> dict:
        entity = self.session.get(model, entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        self.session.delete(entity)
        self.session.commit()
        return {"ok": True}
    
    def update(self, model: type[T], entity_id: int, updated_data: dict) -> T:
        # Get the existing entity
        entity = self.session.get(model, entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        
        # Update the entity fields with the provided data
        for key, value in updated_data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        
        # Commit the changes to the database
        self.session.commit()
        self.session.refresh(entity)
        return entity
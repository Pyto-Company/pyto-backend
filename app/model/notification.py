from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, time

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    realisation: bool
    date_creation: datetime = Field(default_factory=datetime.now)
    rappel_id: int = Field(foreign_key="rappel.id")
    
    rappel: "Rappel" = Relationship(back_populates="notifications")
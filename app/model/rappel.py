from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, time

class Rappel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    type_entretien: str
    frequence: str
    heure: time
    date_creation: datetime = Field(default_factory=datetime.now)
    plante_id: int = Field(foreign_key="plante.id")
    
    plante: "Plante" = Relationship(back_populates="rappels")
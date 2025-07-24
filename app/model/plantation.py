from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine
from datetime import date

class Plantation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    date_debut: date = Field(index=True)
    date_fin: date = Field(index=True)
    espece_id: int = Field(foreign_key="espece.id", index=True)

    especes: list["Espece"] = Relationship(back_populates="plantations")   
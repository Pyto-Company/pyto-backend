from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum

class TypeEntretien(str, Enum):
    ARROSAGE = "ARROSAGE"
    LUMINOSITE = "LUMINOSITE"
    TAILLAGE = "TAILLAGE"
    ENGRAIS = "ENGRAIS"
    PROPAGATION = "PROPAGATION"
    REMPOTAGE = "REMPOTAGE"

class Entretien(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    type: TypeEntretien = Field(sa_column_kwargs={"nullable": False})
    condition: str
    frequence: Optional[str] = None
    espece_id: int = Field(foreign_key="espece.id")
    
    espece: "Espece" = Relationship(back_populates="entretiens")
    conseils: list["Conseil"] = Relationship(back_populates="entretien")
    rappels: list["Rappel"] = Relationship(back_populates="entretien")
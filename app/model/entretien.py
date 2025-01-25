from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum

class TypeEntretien(str, Enum):
    ARROSAGE = "Arrosage"
    LUMINOSITE = "Luminosité"
    TAILLAGE = "Taillage"
    ENGRAIS = "Engrais"
    TEMPERATURE = "Température"
    PROPAGATION = "Propagation"
    REMPOTAGE = "Rempotage"
    HUMIDITE = "Humidité"

class Entretien(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    type: TypeEntretien = Field(sa_column_kwargs={"nullable": False})
    description: str
    resume: str
    espece_id: int = Field(foreign_key="espece.id")
    
    espece: "Espece" = Relationship(back_populates="entretiens")
    conseils: list["Conseil"] = Relationship(back_populates="entretien")
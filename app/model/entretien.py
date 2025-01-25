from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum

class TypeEntretien(str, Enum):
    ARROSAGE = "Arrosage"
    LUMINOSITE = "Luminosité"
    TAILLAGE = "Taillage"
    ENGRAIS = "Engrais"
    PROPAGATION = "Propagation"
    REMPOTAGE = "Rempotage"

class Entretien(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    type: TypeEntretien = Field(sa_column_kwargs={"nullable": False})
    info_principale: str
    info_secondaire: Optional[str] = None
    espece_id: int = Field(foreign_key="espece.id")
    
    espece: "Espece" = Relationship(back_populates="entretiens")
    conseils: list["Conseil"] = Relationship(back_populates="entretien")
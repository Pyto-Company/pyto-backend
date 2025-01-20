from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine

class Mois(str, Enum):
    JANVIER = "Janvier"
    FEVRIER = "Février"
    MARS = "Mars"
    AVRIL = "Avril"
    MAI = "Mai"
    JUIN = "Juin"
    JUILLET = "Juillet"
    AOUT = "Août"
    SEPTEMBRE = "Septembre"
    OCTOBRE = "Octobre"
    NOVEMBRE = "Novembre"
    DECEMBRE = "Décembre"

class Plantation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    numero_mois: int = Field(index=True)
    espece_id: int = Field(foreign_key="espece.id", index=True)

    especes: list["Espece"] = Relationship(back_populates="plantations")   
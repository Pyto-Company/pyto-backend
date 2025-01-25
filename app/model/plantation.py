from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine

class Mois(str, Enum):
    JANVIER = "JANVIER"
    FEVRIER = "FEVRIER"
    MARS = "MARS"
    AVRIL = "AVRIL"
    MAI = "MAI"
    JUIN = "JUIN"
    JUILLET = "JUILLET"
    AOUT = "AOUT"
    SEPTEMBRE = "SEPTEMBRE"
    OCTOBRE = "OCTOBRE"
    NOVEMBRE = "NOVEMBRE"
    DECEMBRE = "DECEMBRE"

class Plantation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    numero_mois: int = Field(index=True)
    espece_id: int = Field(foreign_key="espece.id", index=True)

    especes: list["Espece"] = Relationship(back_populates="plantations")   
from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine

class NomMois(str, Enum):
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

class Mois(SQLModel, table=True):
    numero: int = Field(default=None, primary_key=True, index=True)
    nom: NomMois = Field(default=None, unique=True)

    especes: list["Espece"] = Relationship(back_populates="mois", link_model="EspeceMois")
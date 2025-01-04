from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Habitat(str, Enum):
    INTERIEUR = "Intérieur"
    EXTERIEUR = "Extérieur"

class Espece(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    nom_commun: str = Field(unique=True)
    photo_defaut: str
    habitat: Habitat = Field(sa_column_kwargs={"nullable": False})
    nom_scientifique: str = Field(unique=True)
    description: str
    type: str
    classe_ia: str = Field(unique=True)

    plantes: list["Plante"] = Relationship(back_populates="espece")
    maladies: list["Maladie"] = Relationship(back_populates="espece")
    entretiens: list["Entretien"] = Relationship(back_populates="espece")
    scans: list["Scan"] = Relationship(back_populates="espece")
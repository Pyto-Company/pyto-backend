from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Maladie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    nom: str
    description: str
    classe_ia: str = Field(unique=True)
    espece_id: int = Field(foreign_key="espece.id")

    espece: "Espece" = Relationship(back_populates="maladies")
    scans: list["Scan"] = Relationship(back_populates="maladie")
    traitements: list["Traitement"] = Relationship(back_populates="maladie")
    predispositions: list["Predisposition"] = Relationship(back_populates="maladie")
    symptomes: list["Symptome"] = Relationship(back_populates="maladie")
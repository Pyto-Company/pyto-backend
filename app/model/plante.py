from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Plante(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    nom: str
    date_creation: datetime
    espece_id: int = Field(foreign_key="espece.id")
    utilisateur_id: int = Field(foreign_key="utilisateur.id")

    espece: "Espece" = Relationship(back_populates="plantes")
    utilisateur: "Utilisateur" = Relationship(back_populates="plantes")

    publications: list["Publication"] = Relationship(back_populates="plante")
    photos: list["Photo"] = Relationship(back_populates="plante")
    rappels: list["Rappel"] = Relationship(back_populates="plante")
    scans: list["Scan"] = Relationship(back_populates="plante")
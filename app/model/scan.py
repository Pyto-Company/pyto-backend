from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Scan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    nom_fichier: str
    date_creation: datetime = Field(default_factory=datetime.now)
    espece_id: int = Field(foreign_key="espece.id")
    maladie_id: Optional[int] = Field(foreign_key="maladie.id")
    plante_id: Optional[int] = Field(foreign_key="plante.id")

    maladie: "Maladie" = Relationship(back_populates="scans")
    espece: "Espece" = Relationship(back_populates="scans")
    plante: "Plante" = Relationship(back_populates="scans")
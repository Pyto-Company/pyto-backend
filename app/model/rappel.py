from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, time

from model.entretien import TypeEntretien

class Rappel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    type_entretien: TypeEntretien
    nb_jours_intervalle: int
    heure: time
    actif: bool = Field(default=True)
    date_creation: datetime = Field(default_factory=datetime.now)
    plante_id: int = Field(foreign_key="plante.id")
    
    plante: "Plante" = Relationship(back_populates="rappels")
    notifications: list["Notification"] = Relationship(
        back_populates="rappel",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum

class TypeEnvironnement(str, Enum):
    TEMPERATURE = "TEMPÉRATURE"
    HABITAT = "HABITAT"
    HUMIDITE = "HUMIDITÉ"

class Environnement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    type: TypeEnvironnement = Field(sa_column_kwargs={"nullable": False})
    info_principale: str
    info_secondaire: Optional[str] = None
    espece_id: int = Field(foreign_key="espece.id")

    espece: "Espece" = Relationship(back_populates="environnements")
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Type(str, Enum):
    GRATUIT = "Gratuit"
    ESSAI = "Essai"
    PREMIUM = "Premium"

class Abonnement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    type: Type = Field(sa_column_kwargs={"nullable": False})
    date_debut: datetime = Field(default_factory=datetime.now)
    est_actif: bool
    utilisateur_id: int = Field(foreign_key="utilisateur.id")
    
    utilisateur: "Utilisateur" = Relationship(back_populates="abonnements")
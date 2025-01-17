from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Enum as SQLAlchemyEnum

class TypeAbonnement(str, Enum):
    GRATUIT = "GRATUIT"
    ESSAI = "ESSAI"
    PREMIUM = "PREMIUM"

class Abonnement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    type: TypeAbonnement = Field(sa_column=SQLAlchemyEnum(TypeAbonnement, name="type_abonnement", create_constraint=True, native_enum=True))
    date_debut: datetime = Field(default_factory=datetime.now)
    est_actif: bool
    utilisateur_id: int = Field(foreign_key="utilisateur.id")
    
    utilisateur: "Utilisateur" = Relationship(back_populates="abonnements")
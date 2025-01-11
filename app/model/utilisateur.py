from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr

class Utilisateur(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str
    prenom: str
    nb_scan: int = Field(default=0)
    date_creation: datetime = Field(default_factory=datetime.now)

    commentaires: list["Commentaire"] = Relationship(back_populates="utilisateur")
    plantes: list["Plante"] = Relationship(back_populates="utilisateur")
    messages: list["Message"] = Relationship(back_populates="utilisateur")
    abonnements: list["Abonnement"] = Relationship(back_populates="utilisateur")
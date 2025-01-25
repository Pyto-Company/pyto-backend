from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
from enum import Enum

class ProviderType(str, Enum):
    EMAIL = "EMAIL"
    GOOGLE = "GOOGLE"
    FACEBOOK = "FACEBOOK"
    APPLE = "APPLE"

class Utilisateur(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: EmailStr = Field(index=True, unique=True)
    password: Optional[str] = None  # Optionnel car pas nécessaire pour auth sociale
    prenom: str
    nb_scan: int = Field(default=0)
    date_creation: datetime = Field(default_factory=datetime.now)
    
    # champs pour l'auth sociale
    provider: ProviderType = Field(default=ProviderType.EMAIL)
    provider_id: Optional[str] = Field(default=None, index=True)  # ID unique fourni par le provider
    photo_url: Optional[str] = None  # URL de la photo de profil
    
    commentaires: list["Commentaire"] = Relationship(back_populates="utilisateur")
    plantes: list["Plante"] = Relationship(back_populates="utilisateur")
    messages: list["Message"] = Relationship(back_populates="utilisateur")
    abonnements: list["Abonnement"] = Relationship(back_populates="utilisateur")
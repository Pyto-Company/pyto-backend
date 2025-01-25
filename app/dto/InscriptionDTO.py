from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.model.utilisateur import ProviderType

class InscriptionDTO(BaseModel):
    email: EmailStr = Field(
        description="Adresse email de l'utilisateur",
        example="user@example.com"
    )
    prenom: str = Field(
        min_length=2,
        description="Prénom de l'utilisateur",
        example="Jean"
    )
    premium_started: bool = Field(
        default=False,
        description="Indique si l'utilisateur commence avec un abonnement premium",
        example=False
    )

class InscriptionEmailDTO(InscriptionDTO):
    password: str = Field(
        min_length=8,
        description="Mot de passe de l'utilisateur",
        example="password123"
    )

class InscriptionSocialDTO(InscriptionDTO):
    provider_id: str = Field(
        description="ID unique fourni par le provider",
        example="1234567890"
    )
    photo_url: str = Field(
        description="URL de la photo de profil",
        example="https://example.com/photo.jpg"
    )
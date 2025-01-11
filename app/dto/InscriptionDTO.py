from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class InscriptionDTO(BaseModel):
    email: EmailStr = Field(
        description="Adresse email de l'utilisateur",
        example="user@example.com"
    )
    password: str = Field(
        min_length=8,
        description="Mot de passe de l'utilisateur",
        example="password123"
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
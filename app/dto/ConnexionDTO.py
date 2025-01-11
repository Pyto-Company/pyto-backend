from pydantic import BaseModel, EmailStr, Field

class ConnexionDTO(BaseModel):
    email: EmailStr = Field(
        description="Adresse email de l'utilisateur",
        example="user@example.com"
    )
    password: str = Field(
        min_length=8,
        description="Mot de passe de l'utilisateur",
        example="password123"
    )
from pydantic import BaseModel, EmailStr, Field

class ConnexionSocialDTO(BaseModel):
    provider_id: str = Field(
        description="ID unique fourni par le provider",
        example="1234567890"
    )

class ConnexionEmailDTO(BaseModel):
    password: str = Field(
        min_length=8,
        description="Mot de passe de l'utilisateur",
        example="password123"
    )
    email: EmailStr = Field(
        description="Adresse email de l'utilisateur",
        example="user@example.com"
    )
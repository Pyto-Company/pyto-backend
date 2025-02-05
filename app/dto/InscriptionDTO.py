from pydantic import BaseModel, Field

class InscriptionDTO(BaseModel):
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
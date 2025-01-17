from sqlmodel import SQLModel, Field
from typing import Optional

class EspeceMois(SQLModel, table=True):
    espece_id: Optional[int] = Field(
        default=None, 
        foreign_key="espece.id", 
        primary_key=True
    )
    mois_nom: Optional[str] = Field(
        default=None, 
        foreign_key="mois.nom", 
        primary_key=True
    ) 
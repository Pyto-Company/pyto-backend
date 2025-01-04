from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Conseil(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    titre: str
    description: str
    ordre: int
    entretien_id: int = Field(foreign_key="entretien.id")
    
    entretien: "Entretien" = Relationship(back_populates="conseils")
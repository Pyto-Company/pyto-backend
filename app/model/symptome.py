from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Symptome(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    nom: str
    icone: str
    description: str
    ordre: int
    maladie_id: int = Field(foreign_key="maladie.id")
    
    maladie: "Maladie" = Relationship(back_populates="symptomes")
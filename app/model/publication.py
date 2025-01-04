from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Publication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    message: str
    date_creation: datetime = Field(default_factory=datetime.now)
    date_modification: datetime = Field(default_factory=datetime.now)
    plante_id: int = Field(foreign_key="plante.id")

    plante: "Plante" = Relationship(back_populates="publications")
    commentaires: list["Commentaire"] = Relationship(back_populates="publication")
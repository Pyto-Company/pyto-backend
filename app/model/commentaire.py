from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Commentaire(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    message: str
    ordre: int
    date_creation: datetime = Field(default_factory=datetime.now)
    date_modification: datetime = Field(default_factory=datetime.now)
    utilisateur_id: int = Field(foreign_key="utilisateur.id")
    publication_id: int = Field(foreign_key="publication.id")

    utilisateur: "Utilisateur" = Relationship(back_populates="commentaires")
    publication: "Publication" = Relationship(back_populates="commentaires")
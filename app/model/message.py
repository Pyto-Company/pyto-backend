from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    contenu: str
    date_creation: datetime = Field(default_factory=datetime.now)
    utilisateur_id: int = Field(foreign_key="utilisateur.id")
    
    utilisateur: "Utilisateur" = Relationship(back_populates="messages")
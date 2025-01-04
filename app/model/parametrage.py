from sqlmodel import Field, Relationship, SQLModel

class Parametrage(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    max_scan_gratuit: int
    max_plante_gratuit: int
from datetime import datetime
from pydantic import BaseModel

from app.model.entretien import TypeEntretien

class RappelPrevuDTO(BaseModel):
    id_rappel: int
    id_plante: int
    type_entretien: TypeEntretien
    planter_nom: str
    espece_image: str
    date_prochain_rappel: datetime

from typing import List, Optional
from datetime import datetime, time
from pydantic import BaseModel

class RappelDTO(BaseModel):
    id: int
    type_entretien: str
    frequence: str
    heure: time
    date_creation: datetime

class PlanteJardinDTO(BaseModel):
    id_plante: int
    nom_plante: str
    nom_commun_espece: str
    nom_fichier: str
    rappels_retard: Optional[List[RappelDTO]] = []
    rappels_proche: Optional[List[RappelDTO]] = []
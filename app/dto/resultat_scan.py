from typing import List, Optional
from pydantic import BaseModel

from model.entretien import Entretien
from model.espece import Espece
from model.maladie import Maladie

class ResultatScanDTO(BaseModel):
    espece: Optional[Espece]
    maladie: Optional[Maladie]
    entretiens: Optional[List[Entretien]] = []
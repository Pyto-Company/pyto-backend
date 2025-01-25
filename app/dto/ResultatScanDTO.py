from typing import List, Optional
from pydantic import BaseModel

from app.model.entretien import Entretien
from app.model.espece import Espece
from app.model.maladie import Maladie

class ResultatScanDTO(BaseModel):
    espece: Optional[Espece]
    maladie: Optional[Maladie]
    entretiens: Optional[List[Entretien]] = []
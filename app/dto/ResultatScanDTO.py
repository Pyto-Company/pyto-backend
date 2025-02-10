from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class ConseilDTO(BaseModel):
    id: int
    description: str
    ordre: int
    titre: str
    model_config = ConfigDict(from_attributes=True)

class EntretienDTO(BaseModel):
    id: int
    type: str
    info_principale: str
    info_secondaire: Optional[str]
    conseils: List[ConseilDTO]
    model_config = ConfigDict(from_attributes=True)

class EspeceDTO(BaseModel):
    id: int
    nom_commun: str
    photo_defaut: str
    nom_scientifique: str
    description: str
    type: str
    classe_ia: str
    model_config = ConfigDict(from_attributes=True)

class MaladieDTO(BaseModel):
    id: int
    nom: str
    description: str
    classe_ia: str
    model_config = ConfigDict(from_attributes=True)

class EnvironnementDTO(BaseModel):
    id: int
    type: str
    info_principale: str
    info_secondaire: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class TraitementDTO(BaseModel):
    id: int
    description: str
    model_config = ConfigDict(from_attributes=True)

class PredispositionDTO(BaseModel):
    id: int
    description: str
    model_config = ConfigDict(from_attributes=True)

class SymptomeDTO(BaseModel):
    id: int
    description: str
    model_config = ConfigDict(from_attributes=True)

class ResultatScanDTO(BaseModel):
    espece: Optional[EspeceDTO]
    maladie: Optional[MaladieDTO]
    entretiens: Optional[List[EntretienDTO]] = []
    environnements: Optional[List[EnvironnementDTO]] = []
    traitements: Optional[List[TraitementDTO]] = []
    predispositions: Optional[List[PredispositionDTO]] = []
    symptomes: Optional[List[SymptomeDTO]] = []
    model_config = ConfigDict(from_attributes=True)

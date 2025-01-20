from pydantic import BaseModel

class PlanteMomentDTO(BaseModel):
    espece_id: int
    espece_nom: str
    mois_nom: str
    image_url: str
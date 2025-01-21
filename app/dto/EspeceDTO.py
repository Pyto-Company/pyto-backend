from pydantic import BaseModel

class EspeceDTO(BaseModel):
    espece_id: int
    espece_nom: str
    image_url: str
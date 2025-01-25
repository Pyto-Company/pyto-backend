from pydantic import BaseModel
from datetime import date

class PrevisionMeteoDTO(BaseModel):
    date: date
    temperature: float
    meteo: str
from typing import List
from fastapi import APIRouter, HTTPException
from dto.plante_jardin import PlanteJardinDTO
from service.jardin import JardinService
from service.meteo import MeteoService

router = APIRouter(prefix="/jardin", tags=["jardin"])

@router.get("/{user_id}", response_model=List[PlanteJardinDTO])
async def getMonJardin(user_id: int):
    return JardinService.get(user_id)
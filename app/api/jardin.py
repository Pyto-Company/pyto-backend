from typing import List
from fastapi import APIRouter, HTTPException
from app.dto.plante_jardin import PlanteJardinDTO
from app.service.jardin import JardinService
from app.service.meteo import MeteoService

router = APIRouter(prefix="/jardin", tags=["jardin"])

@router.get("/{user_id}", response_model=List[PlanteJardinDTO])
async def getMonJardin(user_id: int):
    return JardinService.get(user_id)
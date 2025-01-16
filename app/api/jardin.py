from typing import List
from fastapi import APIRouter, Request, Depends
from dto.plante_jardin import PlanteJardinDTO
from service.jardin import JardinService
from database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/jardin", tags=["jardin"])

@router.get("/", response_model=List[PlanteJardinDTO])
async def getMonJardin(request: Request, session: AsyncSession = Depends(get_session)):
    user_id = request.state.user_id
    return await JardinService(session).get(user_id)
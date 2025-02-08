
from fastapi import APIRouter, Depends
from app.repository.plante import PlanteRepository
from app.database.database import get_session
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Request, Depends
from app.dto.PlanteJardinDTO import PlanteJardinDTO
from app.database.database import get_session
from sqlalchemy.orm import Session
from app.dto.EspeceDTO import EspeceDTO
from app.database.database import get_session
from sqlalchemy.orm import Session
from app.repository.espece import EspeceRepository

router = APIRouter(prefix="/jardin", tags=["jardin"])

@router.get("/", response_model=List[PlanteJardinDTO])
def getMonJardin(request: Request, session: Session = Depends(get_session)):
    user_uid = request.state.user_uid
    return PlanteRepository(session).get_jardin(user_uid)

@router.get("/moment", response_model=List[EspeceDTO])
def getPlantesMoment(session: Session = Depends(get_session)):
    return EspeceRepository(session).getPlantesMoment()
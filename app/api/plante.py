from fastapi import APIRouter, Query
from typing import Annotated
from app.model.plante import Plante
from app.repository.plante import PlanteRepository

router = APIRouter(prefix="/plante", tags=["plante"])

@router.post("/")
def create(plante: Plante) -> Plante:
    return PlanteRepository.create(plante)

@router.get("/")
def get_all(offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Plante]:
    return PlanteRepository.get_all(offset, limit)

@router.get("/{plante_id}")
def get_by_id(plante_id: int) -> Plante:
    return PlanteRepository.get_by_id(plante_id)

@router.put("/{plante_id}")
def update(plante_id: int, updated_data: dict) -> Plante:
    return PlanteRepository.update(plante_id, updated_data)

@router.delete("/{plante_id}")
def delete(plante_id: int):
    return PlanteRepository.delete(plante_id)
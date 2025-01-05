from fastapi import APIRouter, Query
from typing import Annotated
from model.rappel import Rappel
from repository.rappel import RappelRepository

router = APIRouter(prefix="/rappel", tags=["rappel"])

@router.post("/")
def create(rappel: Rappel) -> Rappel:
    return RappelRepository.create(rappel)

@router.get("/")
def get_all(offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Rappel]:
    return RappelRepository.get_all(offset, limit)

@router.get("/{rappel_id}")
def get_by_id(rappel_id: int) -> Rappel:
    return RappelRepository.get_by_id(rappel_id)

@router.put("/{rappel_id}")
def update(rappel_id: int, updated_data: dict) -> Rappel:
    return RappelRepository.update(rappel_id, updated_data)

@router.delete("/{rappel_id}")
def delete(rappel_id: int):
    return RappelRepository.delete(rappel_id)
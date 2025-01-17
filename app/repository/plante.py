from typing import Annotated
from app.dto.plante_mois import PlanteMoisDTO
from model.plante import Plante
from repository.base import BaseRepository
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlmodel import select
from model.espece import Espece
from model.espece_mois import EspeceMois
from model.mois import NomMois

class PlanteRepository(BaseRepository[Plante]):
    def __init__(self, session: AsyncSession):
        super().__init__(Plante, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Plante]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, plante_id: int) -> Plante:
        return await super().get_by_id(plante_id)

    async def create(self, plante: Plante) -> Plante:
        return await super().create(plante)

    async def delete(self, plante_id: int) -> dict:
        return await super().delete(plante_id)
    
    async def update(self, plante_id: int, updated_data: dict) -> Plante:
        return await super().update(plante_id, updated_data)
    
    async def getPlantesMoment(self) -> list[Espece]:
        mois_actuel = datetime.now().month

        # Construire la requête pour récupérer les espèces du mois actuel
        query = (
            select(Espece)
            .join(EspeceMois, Espece.id == EspeceMois.espece_id)
            .where(EspeceMois.mois_nom == mois_actuel)
        )

        result = await self.session.execute(query)
        return result.scalars().all()
        

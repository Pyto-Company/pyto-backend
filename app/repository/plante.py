from typing import Annotated
from model.plante import Plante
from repository.base import BaseRepository
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlmodel import select
from model.espece import Espece
from model.plantation import Plantation
from dto.plante_mois import PlanteMomentDTO
from model.plantation import Mois

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
    
    async def getPlantesMoment(self) -> list[PlanteMomentDTO]:
        mois_actuel = datetime.now().month

        # Construire la requête pour récupérer les espèces du mois actuel
        query = (
            select(
                Espece.id.label("espece_id"),
                Espece.nom_commun.label("espece_nom"),
                Espece.photo_defaut.label("image_url"),
                Plantation.numero_mois
            )
            .join(Plantation, Espece.id == Plantation.espece_id)
            .where(Plantation.numero_mois == mois_actuel)
        )

        result = await self.session.execute(query)
        rows = result.all()
        
        # Convertir les résultats en PlanteMomentDTO
        plantes_moment = []
        for row in rows:
            mois_nom = Mois(row.numero_mois).value if row.numero_mois else ""
            plante_dto = PlanteMomentDTO(
                espece_id=row.espece_id,
                espece_nom=row.espece_nom,
                mois_nom=mois_nom,
                image_url=row.image_url
            )
            plantes_moment.append(plante_dto)

        return plantes_moment
        

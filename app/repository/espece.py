from datetime import datetime
from typing import Annotated
from fastapi import Query
from sqlmodel import select
from app.dto.EspeceDTO import EspeceDTO
from app.model.plantation import Plantation
from app.model.espece import Espece
from app.repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class EspeceRepository(BaseRepository[Espece]):
    def __init__(self, session: AsyncSession):
        super().__init__(Espece, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Espece]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, espece_id: int) -> Espece:
        return await super().get_by_id(espece_id)

    async def create(self, espece: Espece) -> Espece:
        return await super().create(espece)

    async def delete(self, espece_id: int) -> dict:
        return await super().delete(espece_id)
    
    async def update(self, espece_id: int, updated_data: dict) -> Espece:
        return await super().update(espece_id, updated_data)
    
    async def get_all_classe_ia(self) -> list[str]:
        query = select(getattr(Espece, "classe_ia"))
        result = await self.session.execute(query)
        return [item[0] for item in result.all()]
    
    async def get_by_class_ia(self, classe_ia: str) -> list[Espece]:
        query = select(Espece).where(Espece.classe_ia == classe_ia)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def search_by_nom_commun(self, search_term: str):
        query = (
            select(
                Espece.id.label("espece_id"),
                Espece.nom_commun.label("espece_nom"),
                Espece.photo_defaut.label("image_url")
            )
            .where(Espece.nom_commun.ilike(f"{search_term}%"))
        )

        result = await self.session.execute(query)
        rows = result.all()
        
        # Convertir les résultats en EspeceDTO
        especes = []
        for row in rows:
            espece = EspeceDTO(
                espece_id=row.espece_id,
                espece_nom=row.espece_nom,
                image_url=row.image_url
            )
            especes.append(espece)

        return especes
        
    
    async def getPlantesMoment(self) -> list[EspeceDTO]:
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
        
        # Convertir les résultats en EspeceDTO
        plantes_moment = []
        for row in rows:
            plante_dto = EspeceDTO(
                espece_id=row.espece_id,
                espece_nom=row.espece_nom,
                image_url=row.image_url
            )
            plantes_moment.append(plante_dto)

        return plantes_moment
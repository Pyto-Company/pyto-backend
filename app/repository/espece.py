from datetime import datetime
from typing import Annotated
from fastapi import Query
from sqlmodel import select
from app.dto.EspeceDTO import EspeceDTO
from app.model.plantation import Plantation
from app.model.espece import Espece
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session
from sqlalchemy import select

class EspeceRepository(BaseRepository[Espece]):
    def __init__(self, session: Session):
        super().__init__(Espece, session)

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Espece]:
        return super().get_all(offset, limit)

    def get_by_id(self, espece_id: int) -> Espece:
        return super().get_by_id(espece_id)

    def create(self, espece: Espece) -> Espece:
        return super().create(espece)

    def delete(self, espece_id: int) -> dict:
        return super().delete(espece_id)
    
    def update(self, espece_id: int, updated_data: dict) -> Espece:
        return super().update(espece_id, updated_data)
    
    def get_all_classe_ia(self) -> list[str]:
        query = select(getattr(Espece, "classe_ia"))
        result = self.session.execute(query)
        return [item[0] for item in result.all()]
    
    def get_by_class_ia(self, classe_ia: str) -> Espece:
        query = select(Espece).where(Espece.classe_ia == classe_ia)
        result = self.session.execute(query)
        espece = result.scalar_one_or_none()
        
        if espece is None:
            raise ValueError(f"Aucune espèce trouvée avec la classe_ia: {classe_ia}")
            
        return espece

    def search_by_nom_commun(self, search_term: str):
        query = (
            select(
                Espece.id.label("espece_id"),
                Espece.nom_commun.label("espece_nom"),
                Espece.photo_defaut.label("image_url")
            )
            .where(Espece.nom_commun.ilike(f"{search_term}%"))
        )

        result = self.session.execute(query)
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
        
    
    def getPlantesMoment(self) -> list[EspeceDTO]:
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

        result = self.session.execute(query)
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
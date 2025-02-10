from typing import Annotated, Dict
from fastapi import Query
from sqlmodel import select
from app.model.entretien import Entretien
from app.model.conseil import Conseil
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session

class EntretienRepository(BaseRepository[Entretien]):
    def __init__(self, session: Session):
        super().__init__(Entretien, session)

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Entretien]:
        return super().get_all(offset, limit)

    def get_by_id(self, entretien_id: int) -> Entretien:
        return super().get_by_id(entretien_id)

    def create(self, entretien: Entretien) -> Entretien:
        return super().create(entretien)

    def delete(self, entretien_id: int) -> dict:
        return super().delete(entretien_id)
    
    def update(self, entretien_id: int, updated_data: dict) -> Entretien:
        return super().update(entretien_id, updated_data)
    
    def get_entretiens_by_espece_id(self, espece_id: int) -> list[Dict]:
        # Sélectionner les entretiens avec leurs conseils associés
        query = (
            select(Entretien, Conseil)
            .join(Conseil, Entretien.id == Conseil.entretien_id)
            .where(Entretien.espece_id == espece_id)
        )
        result = self.session.execute(query)
        
        # Organiser les résultats par entretien
        entretiens_dict = {}
        for entretien, conseil in result:
            if entretien.id not in entretiens_dict:
                entretiens_dict[entretien.id] = {
                    "id": entretien.id,
                    "type": entretien.type,
                    "info_principale": entretien.info_principale,
                    "info_secondaire": entretien.info_secondaire,
                    "espece_id": entretien.espece_id,
                    "conseils": []
                }
            entretiens_dict[entretien.id]["conseils"].append({
                "id": conseil.id,
                "description": conseil.description,
                "ordre": conseil.ordre,
                "titre": conseil.titre
            })
            
        return list(entretiens_dict.values())
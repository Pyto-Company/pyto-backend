from typing import Annotated
from model.plante import Plante
from repository.base import BaseRepository
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from dto.plante_jardin import PlanteJardinDTO, RappelDTO
from typing import List
from repository.base import BaseRepository
from datetime import datetime, timedelta

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
    
    async def get_jardin(self, user_id: int) -> List[PlanteJardinDTO]:
        sql = text("""
            WITH rappels_notifs AS (
                SELECT 
                    p.id as plante_id, 
                    p.nom as plante_nom, 
                    e.nom_commun, 
                    e.photo_defaut,
                    r.id as rappel_id,
                    r.type_entretien,
                    r.nb_jours_intervalle,
                    r.heure,
                    r.date_creation,
                    r.date_creation + (r.nb_jours_intervalle || ' days')::interval as date_prochain_rappel,
                    n.id as notification_id,
                    n.realisation,
                    n.date_creation as notification_date,
                    CASE 
                        WHEN n.realisation = false THEN 1  -- Notifications non réalisées
                        WHEN n.id IS NULL THEN 2           -- Prochains rappels
                    END as priorite
                FROM plante p 
                INNER JOIN espece e ON e.id = p.espece_id 
                LEFT JOIN rappel r ON r.plante_id = p.id
                LEFT JOIN notification n ON n.rappel_id = r.id
                WHERE p.utilisateur_id = :user_id
            ),
            rappels_classes AS (
                SELECT *,
                    ROW_NUMBER() OVER (
                        PARTITION BY plante_id, priorite 
                        ORDER BY 
                            CASE 
                                WHEN priorite = 1 THEN notification_date  -- Plus anciennes notifications non réalisées
                                WHEN priorite = 2 THEN date_prochain_rappel  -- Prochains rappels
                            END ASC
                    ) as rang
                FROM rappels_notifs
                WHERE priorite IS NOT NULL
            )
            SELECT * 
            FROM rappels_classes
            WHERE rang <= 2
            ORDER BY plante_id, priorite, rang
        """)
        
        result = await self.session.execute(sql, {"user_id": user_id})
        rows = result.all()
        
        plantes_dict = {}
        for row in rows:
            if row.plante_id not in plantes_dict:
                plantes_dict[row.plante_id] = {
                    "id_plante": row.plante_id,
                    "nom_plante": row.plante_nom,
                    "nom_commun_espece": row.nom_commun,
                    "nom_fichier": row.photo_defaut,
                    "rappels_retard": [],
                    "rappels_proche": []
                }
            
            if row.rappel_id:
                rappel = RappelDTO(
                    id=row.rappel_id,
                    type_entretien=row.type_entretien,
                    frequence=str(row.nb_jours_intervalle),
                    heure=row.heure,
                    date_creation=row.date_creation
                )
                
                if row.notification_id and not row.realisation:
                    plantes_dict[row.plante_id]["rappels_retard"].append(rappel)
                elif row.date_prochain_rappel > datetime.now():
                    plantes_dict[row.plante_id]["rappels_proche"].append(rappel)
        
        return list(plantes_dict.values())

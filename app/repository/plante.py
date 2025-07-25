from typing import Annotated
from app.model.plante import Plante
from app.repository.base import BaseRepository
from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.dto.PlanteJardinDTO import PlanteJardinDTO, RappelDTO
from typing import List
from app.repository.base import BaseRepository
from datetime import datetime, timedelta

class PlanteRepository(BaseRepository[Plante]):
    def __init__(self, session: Session):
        super().__init__(Plante, session)

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Plante]:
        return super().get_all(offset, limit)

    def get_by_id(self, plante_id: int) -> Plante:
        return super().get_by_id(plante_id)

    def create(self, plante: Plante) -> Plante:
        return super().create(plante)

    def delete(self, plante_id: int) -> dict:
        return super().delete(plante_id)
    
    def update(self, plante_id: int, updated_data: dict) -> Plante:
        return super().update(plante_id, updated_data)
    
    def get_jardin(self, user_id: int) -> List[PlanteJardinDTO]:
        sql = text("""
            WITH rappels_notifs AS (
                SELECT 
                    p.id as plante_id, 
                    p.nom as plante_nom, 
                    e.nom_commun, 
                    e.photo_defaut,
                    r.id as rappel_id,
                    en.type,
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
                FROM utilisateur u
                INNER JOIN plante p ON p.utilisateur_id = u.id
                INNER JOIN espece e ON e.id = p.espece_id 
                LEFT JOIN rappel r ON r.plante_id = p.id
                LEFT JOIN notification n ON n.rappel_id = r.id
                LEFT JOIN entretien en ON r.entretien_id = en.id
                WHERE u.firebase_user_uid = :user_id
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
        
        result = self.session.execute(sql, {"user_id": user_id})
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
                    type_entretien=row.type,
                    frequence=str(row.nb_jours_intervalle),
                    heure=row.heure,
                    date_creation=row.date_creation,
                    date_prochain_rappel=row.date_prochain_rappel

                )

                
                if row.notification_id and not row.realisation:
                    plantes_dict[row.plante_id]["rappels_retard"].append(rappel)
                elif row.date_prochain_rappel > datetime.now():
                    plantes_dict[row.plante_id]["rappels_proche"].append(rappel)
        
        return list(plantes_dict.values())

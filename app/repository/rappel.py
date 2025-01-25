from typing import Annotated
from fastapi import Query
from sqlalchemy import text
from sqlmodel import select
from app.dto.RappelPrevuDTO import RappelPrevuDTO
from app.model.rappel import Rappel
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session

class RappelRepository(BaseRepository[Rappel]):
    def __init__(self, session: Session):
        super().__init__(Rappel, session)

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Rappel]:
        return super().get_all(offset, limit)

    def get_by_id(self, rappel_id: int) -> Rappel:
        return super().get_by_id(rappel_id)

    def create(self, rappel: Rappel) -> Rappel:
        return super().create(rappel)

    def delete(self, rappel_id: int) -> dict:
        return super().delete(rappel_id)
    
    def update(self, rappel_id: int, updated_data: dict) -> Rappel:
        return super().update(rappel_id, updated_data)
    
    def get_rappels_by_plante_id(self, plante_id: int) -> list[Rappel]:
        sql = text("""
            WITH date_prochain_rappel AS (
                SELECT 
                    r.id,
                    r.type_entretien,
                    r.date_creation,
                    r.nb_jours_intervalle,
                    r.heure,
                    r.plante_id,
                    r.date_creation + 
                        (CEIL(
                            EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - r.date_creation)) / 
                            (r.nb_jours_intervalle * 86400)
                        ) * r.nb_jours_intervalle || ' days')::interval 
                        AS prochain_rappel
                FROM rappel r
                WHERE r.plante_id = :plante_id
            )
            SELECT 
                id,
                type_entretien,
                date_creation,
                nb_jours_intervalle,
                heure,
                plante_id
            FROM date_prochain_rappel
            ORDER BY prochain_rappel ASC
        """)

        result = self.session.execute(sql, {"plante_id": plante_id})
        rows = result.all()
        
        rappels = []
        for row in rows:
            rappel = Rappel(
                id=row.id,
                type_entretien=row.type_entretien,
                date_creation=row.date_creation,
                nb_jours_intervalle=row.nb_jours_intervalle,
                heure=row.heure,
                plante_id=row.plante_id
            )
            rappels.append(rappel)
        
        return rappels

    def get_rappels_by_user_id(self, user_id: int) -> list[RappelPrevuDTO]:
        sql = text("""
            WITH date_prochain_rappel AS (
                SELECT 
                    r.id,
                    ent.type,
                    r.plante_id,
                    p.nom,
                    e.photo_defaut,
                    r.date_creation + 
                        (CEIL(
                            EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - r.date_creation)) / 
                            (r.nb_jours_intervalle * 86400)
                        ) * r.nb_jours_intervalle || ' days')::interval 
                        AS prochain_rappel
                FROM rappel r
                INNER JOIN plante p ON r.plante_id = p.id
                INNER JOIN espece e ON p.espece_id = e.id
                INNER JOIN entretien ent ON r.entretien_id = ent.id
                WHERE p.utilisateur_id = :user_id
            )
            SELECT 
                id,
                type,
                plante_id,
                prochain_rappel,
                nom,
                photo_defaut
            FROM date_prochain_rappel
            ORDER BY prochain_rappel ASC
        """)

        result = self.session.execute(sql, {"user_id": user_id})
        rows = result.all()
        
        rappels = []
        for row in rows:
            rappel = RappelPrevuDTO(
                id_rappel=row.id,
                id_plante=row.plante_id,
                type_entretien=row.type,
                planter_nom=row.nom,
                espece_image=row.photo_defaut,
                date_prochain_rappel=row.prochain_rappel
            )
            rappels.append(rappel)
        
        return rappels

    def get_rappels_for_notifications(self) -> list[Rappel]:
        sql = text("""
            SELECT 
                r.id,
                r.type_entretien,
                r.date_creation,
                r.nb_jours_intervalle,
                r.heure,
                r.plante_id,
                (CURRENT_DATE - r.date_creation::date) as jours_ecoules
            FROM rappel r
            WHERE ((CURRENT_DATE - r.date_creation::date)::integer % r.nb_jours_intervalle = 0)
            AND r.heure <= CURRENT_TIME
        """)

        result = self.session.execute(sql)
        rows = result.all()
        
        rappels = []
        for row in rows:
            rappel = Rappel(
                id=row.id,
                type_entretien=row.type_entretien,
                date_creation=row.date_creation,
                nb_jours_intervalle=row.nb_jours_intervalle,
                heure=row.heure,
                plante_id=row.plante_id
            )
            rappels.append(rappel)
        
        return rappels
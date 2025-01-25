from typing import Annotated
from fastapi import Query
from sqlalchemy import text
from sqlmodel import select
from model.rappel import Rappel
from repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class RappelRepository(BaseRepository[Rappel]):
    def __init__(self, session: AsyncSession):
        super().__init__(Rappel, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Rappel]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, rappel_id: int) -> Rappel:
        return await super().get_by_id(rappel_id)

    async def create(self, rappel: Rappel) -> Rappel:
        return await super().create(rappel)

    async def delete(self, rappel_id: int) -> dict:
        return await super().delete(rappel_id)
    
    async def update(self, rappel_id: int, updated_data: dict) -> Rappel:
        return await super().update(rappel_id, updated_data)
    
    async def get_rappels_by_plante_id(self, plante_id: int) -> list[Rappel]:
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

        result = await self.session.execute(sql, {"plante_id": plante_id})
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

    async def get_rappels_by_user_id(self, user_id: int) -> list[Rappel]:
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
                INNER JOIN plante p ON r.plante_id = p.id
                WHERE p.utilisateur_id = :user_id
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

        result = await self.session.execute(sql, {"user_id": user_id})
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

    async def get_rappels_for_notifications(self) -> list[Rappel]:
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

        result = await self.session.execute(sql)
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
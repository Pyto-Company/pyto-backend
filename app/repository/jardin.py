from fastapi import Query
from sqlalchemy import text
from dto.plante_jardin import PlanteJardinDTO
from typing import List
from repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class JardinRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(None, session)

    async def get_jardin(self, user_id: int) -> List[PlanteJardinDTO]:
        sql = text("""
            SELECT p.id, p.nom, e.nom_commun, e.photo_defaut 
            FROM plante p 
            INNER JOIN espece e on e.id = p.espece_id 
            WHERE p.utilisateur_id = :param1
        """)
        result = await self.session.execute(sql, {"param1": user_id})
        rows = result.all()
        return [{"id_plante": row[0], "nom_plante": row[1], "nom_commun_espece": row[2], "nom_fichier": row[3]} for row in rows]

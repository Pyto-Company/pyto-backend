from typing import Annotated
from fastapi import Query, HTTPException
from sqlmodel import select
from app.dto import MeDTO
from model.utilisateur import Utilisateur
from repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class UtilisateurRepository(BaseRepository[Utilisateur]):
    def __init__(self, session: AsyncSession):
        super().__init__(Utilisateur, session)

    async def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Utilisateur]:
        return await super().get_all(offset, limit)

    async def get_by_id(self, user_id: int) -> Utilisateur:
        return await super().get_by_id(user_id)

    async def create(self, user: Utilisateur) -> Utilisateur:
        return await super().create(user)

    async def delete(self, user_id: int) -> dict:
        return await super().delete(user_id)
    
    async def get_by_email_and_password(self, email: str, password: str) -> Utilisateur:
        query = select(self.model).where(self.model.email == email, self.model.password == password)
        result = await self.session.execute(query)
        utilisateur = result.scalar_one_or_none()
        return utilisateur

    async def getMe(self, user_id: int) -> MeDTO:
        sql = text("""
            SELECT 
                u.id,
                u.email,
                u.prenom,
                u.nb_scan,
                u.date_creation,
                COUNT(p.id) as nb_plantes,
                a.id as abonnement_id,
                a.type,
                a.date_debut,
                a.est_actif,
                a.utilisateur_id
            FROM utilisateur u
            INNER JOIN plante p ON p.utilisateur_id = u.id
            INNER JOIN abonnement a ON a.utilisateur_id = u.id
            WHERE u.id = :user_id
            AND a.est_actif = true
        """)
        
        result = await self.session.execute(sql, {"user_id": user_id})
        rows = result.all()
        if not rows:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
            
        row = rows[0]
        
        meDto: MeDTO = {
            "user_id": row.id,
            "user_email": row.email,
            "user_prenom": row.prenom,
            "user_nb_scan": row.nb_scan,
            "user_date_creation": row.date_creation,
            
            "abonnement_id": row.abonnement_id,
            "abonnement_type": row.type,
            "abonnement_date_debut": row.date_debut,
            "abonnement_est_actif": row.est_actif,
            "abonnement_utilisateur_id": row.utilisateur_id,
            
            "user_nb_plantes": row.nb_plantes
        }

        return meDto

from typing import Annotated, Optional
from fastapi import Query, HTTPException
from sqlmodel import select
from app.dto.UtilisateurDTO import UtilisateurDTO
from app.model.utilisateur import Utilisateur
from app.repository.base import BaseRepository
from sqlalchemy.orm import Session
from sqlalchemy import text

class UtilisateurRepository(BaseRepository[Utilisateur]):
    def __init__(self, session: Session):
        super().__init__(Utilisateur, session)

    def get_all(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Utilisateur]:
        return super().get_all(offset, limit)

    def get_by_id(self, user_id: int) -> Utilisateur:
        return super().get_by_id(user_id)

    def create(self, user: Utilisateur) -> Utilisateur:
        return super().create(user)

    def delete(self, user_id: int) -> dict:
        return super().delete(user_id)
    
    def get_by_email_and_password(self, email: str, password: str) -> Utilisateur:
        query = select(self.model).where(self.model.email == email, self.model.password == password)
        result = self.session.execute(query)
        utilisateur = result.scalar_one_or_none()
        return utilisateur

    def getMe(self, user_id: int) -> UtilisateurDTO:
        sql = text("""
            SELECT 
                u.id,
                u.email,
                u.prenom,
                u.nb_scan,
                u.date_creation,
                (SELECT COUNT(id) FROM plante WHERE utilisateur_id = u.id) as nb_plantes,
                a.id as abonnement_id,
                a.type,
                a.date_debut,
                a.est_actif,
                a.utilisateur_id
            FROM utilisateur u
            INNER JOIN abonnement a ON a.utilisateur_id = u.id
            WHERE u.id = :user_id
            AND a.est_actif = true
        """)
        
        result = self.session.execute(sql, {"user_id": user_id})
        rows = result.all()
        if not rows:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
            
        row = rows[0]
        
        meDto: UtilisateurDTO = {
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

    def get_by_email(self, email: str) -> Optional[Utilisateur]:
        query = select(Utilisateur).where(Utilisateur.email == email)
        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_by_provider_id(self, provider_id: str) -> Optional[Utilisateur]:
        query = select(Utilisateur).where(Utilisateur.provider_id == provider_id)
        result = self.session.execute(query)
        return result.scalar_one_or_none()

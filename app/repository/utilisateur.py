from typing import Annotated
from fastapi import Depends, Query, HTTPException
from sqlmodel import Session, select
from app.database.database import get_session
from app.model.utilisateur import Utilisateur
from app.repository.base import BaseRepository

class UtilisateurRepository(BaseRepository[Utilisateur]):

    def get_users(
        self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
    ) -> list[Utilisateur]:
        return self.get_all(Utilisateur, offset, limit)

    def get_user_by_id(self, user_id: int) -> Utilisateur:
        return self.get_by_id(Utilisateur, user_id)

    def create_user(self, user: Utilisateur) -> Utilisateur:
        return self.create(user)

    def delete_user(self, user_id: int) -> dict:
        return self.delete(Utilisateur, user_id)

    def validate_user(self, token: str):
        query = select(Utilisateur).where(Utilisateur.validation_token == token)
        user = self.session.exec(query).first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid token")
        user.is_active = True
        user.validation_token = None  # Remove token after use
        self.session.add(user)
        self.session.commit()
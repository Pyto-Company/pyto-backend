from fastapi import APIRouter, Depends
from app.database import database
from app.model.publication import Publication
from app.model.utilisateur import Utilisateur
from app.repository.publication import PublicationRepository

router = APIRouter(prefix="/publication", tags=["publication"])

@router.post("/")
def create_post(post: Publication, user_id: int, current_user: Utilisateur = Depends(database)):
    post.user_id = current_user.id
    PublicationRepository.createPost(post)
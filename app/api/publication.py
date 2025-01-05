from fastapi import APIRouter, Depends
from database import database
from model.publication import Publication
from model.utilisateur import Utilisateur
from repository.publication import PublicationRepository

router = APIRouter(prefix="/publication", tags=["publication"])

@router.post("/")
def create_post(post: Publication, user_id: int, current_user: Utilisateur = Depends(database)):
    post.user_id = current_user.id
    PublicationRepository.createPost(post)
import uuid
from sqlmodel import Session
from app.model.utilisateur import Utilisateur
from app.repository.utilisateur import UtilisateurRepository
from app.service.email import EmailService

class UtilisateurService():

    def CreateUser(user: Utilisateur) -> None:
        token = str(uuid.uuid4())  # Generate a unique token
        user.validation_token = token
        user = UtilisateurRepository.createUser(user)
        EmailService.SendValidationEmailToUser(user.email, token)
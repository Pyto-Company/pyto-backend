import uuid
from sqlmodel import Session
from model.utilisateur import Utilisateur
from repository.utilisateur import UtilisateurRepository
from service.email import EmailService

class UtilisateurService():

    def CreateUser(user: Utilisateur) -> None:
        token = str(uuid.uuid4())  # Generate a unique token
        user.validation_token = token
        user = UtilisateurRepository.createUser(user)
        EmailService.SendValidationEmailToUser(user.email, token)
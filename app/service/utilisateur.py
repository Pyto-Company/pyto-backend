from app.repository.utilisateur import UtilisateurRepository
from app.repository.abonnement import AbonnementRepository
from app.dto.InscriptionDTO import InscriptionDTO
from app.model.utilisateur import Utilisateur
from app.model.abonnement import Abonnement, TypeAbonnement
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.client.firebase import FirebaseClient

class UtilisateurService:

    def __init__(self, session: Session):
        self.session = session

    
    def createUser(self, user_uid: str, inscription: InscriptionDTO):
        try:

            user_info = FirebaseClient.get_user_info(user_uid)
            if user_info is None:
                raise HTTPException(status_code=400, detail="Utilisateur introuvable dans Firebase")

            # Vérifier si l'utilisateur existe déjà avec cet email
            existing_user = UtilisateurRepository(self.session).get_by_firebase_user_id(user_uid)
            if existing_user:
                raise HTTPException(status_code=400, detail=f"Un utilisateur existe déjà avec cet User UID")

            # Création d'un nouvel utilisateur sans spécifier l'ID
            new_user = Utilisateur(
                firebase_user_uid=user_uid,
                prenom=inscription.prenom,
                nb_scan=0,
                date_creation=datetime.now()
            )
            
            # Création de l'utilisateur
            created_user = UtilisateurRepository(self.session).create(new_user)
            
            # Création de l'abonnement si premium_started est True
            if inscription.premium_started:
                abonnement_type = TypeAbonnement.ESSAI
            else:
                abonnement_type = TypeAbonnement.GRATUIT

            new_abonnement = Abonnement(
                utilisateur_id=created_user.id,
                date_debut=datetime.now(),
                est_actif=True,
                type=abonnement_type
            )
            AbonnementRepository(self.session).create(new_abonnement)
            
            self.session.commit()
            
            return {"message": "Inscription réussie"}
        
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
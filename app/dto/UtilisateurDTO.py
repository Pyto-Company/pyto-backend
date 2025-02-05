from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.model.abonnement import TypeAbonnement

class UtilisateurDTO(BaseModel):
    user_id: int
    user_firebase_user_uid: str
    user_prenom: str
    user_nb_scan: int
    user_date_creation: datetime

    abonnement_id: int
    abonnement_type: TypeAbonnement
    abonnement_date_debut: datetime
    abonnement_est_actif: bool
    abonnement_utilisateur_id: int

    user_nb_plantes: int

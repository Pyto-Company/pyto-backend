from repository.utilisateur import UtilisateurRepository
from repository.abonnement import AbonnementRepository
from config.password import PasswordConfig
from dto.InscriptionDTO import InscriptionDTO, InscriptionEmailDTO
from model.utilisateur import ProviderType, Utilisateur
from model.abonnement import Abonnement, TypeAbonnement
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

class UtilisateurService:

    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def createUser(self, request: InscriptionEmailDTO, provider: ProviderType):
        try:
            # Vérifier si l'utilisateur existe déjà avec cet email
            existing_user = await UtilisateurRepository(self.session).get_by_email(request.email)
            
            if existing_user:
                if existing_user.provider == provider:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Un compte existe déjà avec cet email via {provider.value}"
                    )
                else:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Un compte existe déjà avec cet email via {existing_user.provider.value}"
                    )

            # Création d'un nouvel utilisateur sans spécifier l'ID
            new_user = Utilisateur(
                email=request.email,
                password=PasswordConfig.hash(request.password),
                prenom=request.prenom,
                date_creation=datetime.now(),
                nb_scan=0,
                provider=provider
            )
            
            # Création de l'utilisateur
            created_user = await UtilisateurRepository(self.session).create(new_user)
            
            # Création de l'abonnement si premium_started est True
            if request.premium_started:
                abonnement_type = TypeAbonnement.ESSAI
            else:
                abonnement_type = TypeAbonnement.GRATUIT

            new_abonnement = Abonnement(
                utilisateur_id=created_user.id,
                date_debut=datetime.now(),
                est_actif=True,
                type=abonnement_type
            )
            await AbonnementRepository(self.session).create(new_abonnement)
            
            await self.session.commit()
            
            return {
                "message": "Inscription réussie",
                "user": {
                    "id": created_user.id,
                    "email": created_user.email,
                    "prenom": created_user.prenom,
                    "premium_started": request.premium_started
                }
            }
        except HTTPException:
            await self.session.rollback()
            raise
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
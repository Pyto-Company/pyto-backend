from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.config.token import TokenConfig
from app.config.password import PasswordConfig
from app.dto.ConnexionDTO import ConnexionEmailDTO, ConnexionSocialDTO
from app.repository.utilisateur import UtilisateurRepository

class ConnexionService():

    def __init__(self, session: Session):
        self.session = session

    def login(self, infoConnexion: ConnexionEmailDTO):
        utilisateur = UtilisateurRepository(self.session).get_by_email_and_password(
            infoConnexion.email, 
            PasswordConfig.hash(infoConnexion.password)
        )
        if not utilisateur:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = TokenConfig.create_access_token(data={"sub": str(utilisateur.id)})
        return {"access_token": access_token, "token_type": "bearer"}
    
    def login_social(self, infoConnexion: ConnexionSocialDTO):
        utilisateur = UtilisateurRepository(self.session).get_by_provider_id(infoConnexion.provider_id)
        if not utilisateur:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = TokenConfig.create_access_token(data={"sub": str(utilisateur.id)})
        return {"access_token": access_token, "token_type": "bearer"}

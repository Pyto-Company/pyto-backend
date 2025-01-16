from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.token import TokenConfig
from config.password import PasswordConfig
from dto.ConnexionDTO import ConnexionDTO
from repository.utilisateur import UtilisateurRepository

class ConnexionService():

    def __init__(self, session: AsyncSession):
        self.session = session

    async def login(self, infoConnexion: ConnexionDTO):
        utilisateur = await UtilisateurRepository(self.session).get_by_email_and_password(
            infoConnexion.email, 
            PasswordConfig.hash(infoConnexion.password)
        )
        if not utilisateur:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = TokenConfig.create_access_token(data={"sub": str(utilisateur.id)})
        return {"access_token": access_token, "token_type": "bearer"}
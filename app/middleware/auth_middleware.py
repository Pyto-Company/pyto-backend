from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import jwt
from jwt.exceptions import PyJWTError, ExpiredSignatureError
from config.token import SECRET_KEY, ALGORITHM
from repository.utilisateur import UtilisateurRepository
from database.database import async_session
from logger.logger import logger

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware d'authentification pour FastAPI.
    Vérifie la présence et la validité du token JWT pour toutes les routes,
    sauf celles explicitement exclues.
    """
    
    def __init__(self, app):
        """
        Initialise le middleware avec les chemins à exclure de l'authentification.
        
        Args:
            app (FastAPI): L'application FastAPI
            exclude_paths (list[str], optional): Liste des chemins à exclure
        """
        super().__init__(app)
        self.exclude_paths = [
            "/docs",
            "/openapi.json",
            "/connexion",
            "/inscription",
            "/health",
            "/docs",              # Documentation Swagger
            "/openapi.json",      # Schéma OpenAPI
            "/redoc",             # Documentation ReDoc
            "/utilisateur",       # Création de compte
            "/connexion/token",   # Obtention du token
            "/inscription"        # Inscription avec Google
        ]

    async def dispatch(self, request, call_next):
        """
        Traite chaque requête entrante.
        
        Args:
            request: La requête HTTP entrante
            call_next: La fonction à appeler pour continuer le traitement
            
        Returns:
            La réponse HTTP
        """
        path = request.url.path
        
        # Vérifie si le chemin est exclu de l'authentification
        if any(path.startswith(excluded) for excluded in self.exclude_paths):
            return await call_next(request)
        
        # Vérifie le token pour tous les autres chemins
        try:    
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Token manquant ou invalide"}
                )
            
            token = auth_header.split(' ')[1]
            
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = int(payload.get("sub"))
                logger.info(f"L'identifiant de l'utilisateur du token est {user_id}")

                # Vérifier l'existence de l'utilisateur
                async with async_session() as session:
                    repository = UtilisateurRepository(session)
                    user = await repository.get_by_id(user_id)
                    logger.info(f"L'utilisateur est {user}")

                    if not user:
                        message = "L'identifiant n'a pas été trouvé"
                        logger.error(message)
                        return JSONResponse(
                            status_code=401,
                            content={"detail": message}
                        )
                    
                request.state.user_id = user_id
                
            except (ExpiredSignatureError, ValueError) as e:
                message = "Token expiré ou invalide"
                logger.error(message + " : " + str(e))
                return JSONResponse(
                    status_code=401,
                    content={"detail": message}
                )
            except PyJWTError as e:
                message = "Token invalide"
                logger.error(message + " : " + str(e))
                return JSONResponse(
                    status_code=401,
                    content={"detail": message}
                )
                
        except Exception as e:
            message = "Erreur inconnue"
            logger.error(message + " : " + str(e))
            return JSONResponse(
                status_code=401,
                content={"detail": message}
            )
            
        return await call_next(request) 
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.logger.logger import logger
from firebase_admin import auth

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
            "/docs/oauth2-redirect",
            "/openapi.json",
            "/health",
            "/redoc",
            "/inscription/token",
            "/swagger-ui.css",
            "/swagger-ui-bundle.js",
            "/swagger-ui-standalone-preset.js"
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
                # Verify the token locally
                decoded_token = auth.verify_id_token(token)
                request.state.user_uid = decoded_token['uid']
                return await call_next(request)

            except auth.InvalidIdTokenError as e:
                message = "Token expiré ou invalide"
                logger.error(message + " : " + str(e))
                return JSONResponse(
                    status_code=401,
                    content={"detail": message}
                )
            
        except Exception as e:
            message = "Erreur lors de la vérification du token"
            logger.error(message + " : " + str(e))
            return JSONResponse(
                status_code=500,
                content={"detail": message}
            )
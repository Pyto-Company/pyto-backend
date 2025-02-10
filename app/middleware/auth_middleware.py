from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.logger.logger import logger
from firebase_admin import auth

from app.config.constants import Constants

class AuthMiddleware(BaseHTTPMiddleware):
    
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        path = request.url.path
        
        # Vérifie si le chemin est exclu de l'authentification
        if any(path.startswith(excluded) for excluded in Constants.get_excluded_paths()):
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
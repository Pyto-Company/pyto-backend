from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBearer
import jwt
from service.connexion import SECRET_KEY, ALGORITHM

# Configuration du bearer token
security = HTTPBearer()

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware d'authentification pour FastAPI.
    Vérifie la présence et la validité du token JWT pour toutes les routes,
    sauf celles explicitement exclues.
    """
    
    def __init__(self, app: FastAPI, exclude_paths: list[str] = None):
        """
        Initialise le middleware avec les chemins à exclure de l'authentification.
        
        Args:
            app (FastAPI): L'application FastAPI
            exclude_paths (list[str], optional): Liste des chemins à exclure
        """
        super().__init__(app)
        self.exclude_paths = exclude_paths or [
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
                request.state.user_id = payload.get("sub")
                
            except jwt.ExpiredSignatureError:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Token expiré"}
                )
            except jwt.JWTError:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Token invalide"}
                )
                
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": str(e)}
            )
            
        return await call_next(request) 
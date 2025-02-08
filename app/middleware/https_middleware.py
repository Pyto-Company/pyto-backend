from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from app.logger.logger import logger

class HTTPSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Liste des chemins autorisés sans HTTPS
        allowed_paths = [
            "/docs",
            "/docs/oauth2-redirect",
            "/openapi.json",
            "/redoc",
            "/swagger-ui.css",
            "/swagger-ui-bundle.js",
            "/swagger-ui-standalone-preset.js",
            "/.well-known/acme-challenge/",
            "/inscription/token"
        ]

        forwarded_proto = request.headers.get("X-Forwarded-Proto", "http")
        
        if forwarded_proto != "https" and not any(request.url.path.startswith(path) for path in allowed_paths):
            logger.warning(f"[{__class__.__name__}] Requête non-HTTPS bloquée")
            return JSONResponse(
                status_code=403,
                content={"detail": "Les requêtes HTTPS sont obligatoires"}
            )
        
        response = await call_next(request)
        return response
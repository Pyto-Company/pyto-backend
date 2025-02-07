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
            "/.well-known/acme-challenge/"
        ]

        if request.url.scheme != "https" and not any(request.url.path.startswith(path) for path in allowed_paths):
            # Log les détails de la requête non-HTTPS
            logger.warning(
                f"Tentative d'accès non-HTTPS détectée\n"
                f"Path: {request.url.path}\n"
                f"Method: {request.method}\n"
                f"Client: {request.client.host if request.client else 'unknown'}\n"
                f"Scheme: {request.url.scheme}"
            )
            
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "Les requêtes HTTPS sont obligatoires"
                }
            )
        return await call_next(request) 
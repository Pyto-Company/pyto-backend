from app.logger.logger import logger
import time
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S')

        logger.info(
            f"[{__class__.__name__}] Réception d'une nouvelle requête\n"
            f"Heure: {formatted_time}\n"
            f"Full URL: {request.url}\n"
            f"Method: {request.method}\n"
            f"Scheme: {request.url.scheme}\n"
            f"X-Forwarded-Proto: {request.headers.get("X-Forwarded-Proto", "http")}\n"
            f"Client: {request.client.host if request.client else 'unknown'}\n"
            f"Port: {request.client.port if request.client else 'unknown'}"
        )

        response = await call_next(request)
        process_time = time.time() - start_time

        logger.info(
            f"[{__class__.__name__}]Retour de la requête\n"
            f"Durée: {process_time:.2f}s\n"
            f"Code retour: {response.status_code}"
        )

        return response
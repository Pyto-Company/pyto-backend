from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import traceback
from logger.logger import logger

class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # Log l'erreur avec la stack trace
            error_details = {
                "path": request.url.path,
                "method": request.method,
                "client_host": request.client.host if request.client else "unknown",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            
            logger.error(
                f"Error occurred: {error_details['error']}\n"
                f"Path: {error_details['path']}\n"
                f"Method: {error_details['method']}\n"
                f"Client: {error_details['client_host']}\n"
                f"Traceback:\n{error_details['traceback']}"
            )
            
            # Retourner une réponse JSON avec l'erreur
            return JSONResponse(
                status_code=500,
                content={"detail": str(e)}
            ) 
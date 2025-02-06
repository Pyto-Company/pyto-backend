from fastapi.logger import logger as fastapi_logger
import time
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S')
        fastapi_logger.info(
            f'{formatted_time} - {request.client.host}:{request.client.port} '
            f'"{request.method} {request.url.path}" {response.status_code} '
            f'(took {process_time:.2f}s)'
        )
        return response
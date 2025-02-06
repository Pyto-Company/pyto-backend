from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        now = time.time()
        
        # Nettoyer les anciennes requêtes
        self.requests[client_ip] = [req_time for req_time in self.requests[client_ip] 
                                  if now - req_time < self.window_seconds]
        
        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Trop de requêtes"}
            )
            
        self.requests[client_ip].append(now)
        return await call_next(request) 
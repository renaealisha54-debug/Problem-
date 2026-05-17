import time
from collections import defaultdict
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 30, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        self.clients = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        ip = (request.client.host if request.client else None) or "unknown"
        now = time.time()
        self.clients[ip] = [t for t in self.clients[ip] if now - t < self.window]
        if len(self.clients[ip]) >= self.max_requests:
            return JSONResponse({"error": "Rate limit exceeded. Try again shortly."}, status_code=429)
        self.clients[ip].append(now)
        return await call_next(request)

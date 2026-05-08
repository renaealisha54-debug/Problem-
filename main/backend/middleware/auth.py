import os
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/"):
            api_key = request.headers.get("X-API-Key")
            expected = os.getenv("APP_API_KEY")
            if expected and api_key != expected:
                return JSONResponse({"error": "Unauthorized"}, status_code=401)
        return await call_next(request)

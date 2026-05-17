import os
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

PROTECTED_PREFIXES = ("/api/",)
PUBLIC_PREFIXES = ("/downloads/", "/health", "/docs", "/openapi.json")

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        is_protected = any(path.startswith(p) for p in PROTECTED_PREFIXES)
        is_public = any(path.startswith(p) for p in PUBLIC_PREFIXES)
        if is_protected and not is_public:
            api_key = request.headers.get("X-API-Key")
            expected = os.getenv("APP_API_KEY")
            if expected and api_key != expected:
                return JSONResponse({"error": "Unauthorized"}, status_code=401)
        return await call_next(request)

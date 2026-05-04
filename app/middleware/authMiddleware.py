from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security import verify_token


PUBLIC_PATHS = {
    "/",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/docs/oauth2-redirect",
}


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        if request.url.path in PUBLIC_PATHS or request.url.path.startswith("/auth"):
            return await call_next(request)
        

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing authentication token"},
            )

        try:
            scheme, token = auth_header.split(" ", 1)
        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authorization header"},
            )

        if scheme.lower() != "bearer":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication scheme"},
            )

        payload = verify_token(token)
        if payload is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or expired token"},
            )

        request.state.user = payload
        return await call_next(request)

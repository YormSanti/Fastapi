from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.security import verify_token


class AuthenticationMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):

        # ✅ Allow public routes
        if request.url.path.startswith("/auth"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing authentication token"},
            )

        try:
            scheme, token = auth_header.split()

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

        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authorization header"},
            )

        return await call_next(request)
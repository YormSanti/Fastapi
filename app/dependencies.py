from collections.abc import Generator

from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_token
from app.core.roles import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


def require_roles(*allowed_roles: UserRole):
    allowed_values = {role.value for role in allowed_roles}

    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") not in allowed_values:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user

    return role_checker


def has_role(current_user: dict, *allowed_roles: UserRole) -> bool:
    return current_user.get("role") in {role.value for role in allowed_roles}


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

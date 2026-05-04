from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "komislecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    if len(password) > 72:
        raise ValueError("Password too long. Maximum 72 characters allowed.")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    if len(plain_password) > 72:
        return False
    return pwd_context.verify(plain_password, hashed_password)


def _create_token(data: dict, expires_delta: timedelta, token_type: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(data: dict):
    return _create_token(
        data,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "access",
    )


def create_refresh_token(data: dict):
    return _create_token(
        data,
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "refresh",
    )


def verify_token(token: str, expected_type: str = "access"):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != expected_type:
            return None
        return payload
    except JWTError:
        return None

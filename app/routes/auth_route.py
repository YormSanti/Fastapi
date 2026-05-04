from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.core.roles import UserRole
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordWithOtpRequest,
    TokenResponse,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_token,
)
from app.services import email_service, password_reset_service, user_service


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

PASSWORD_RESET_MESSAGE = "If this email exists, a reset code has been sent"


def create_token_response(user: User) -> dict:
    token_data = {"sub": user.email, "user_id": user.id, "role": user.role}
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
        "role": user.role,
    }


@router.post("/register", response_model=TokenResponse)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user_count = db.query(User).count()
    role = UserRole.ADMIN.value if user_count == 0 else UserRole.USER.value

    new_user = User(
        firstName=data.firstName,
        lastName=data.lastName,
        email=data.email,
        password=hash_password(data.password),
        role=role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return create_token_response(new_user)


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return create_token_response(user)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    payload = verify_token(data.refresh_token, expected_type="refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    return create_token_response(user)


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == data.email).first()
    if user is None:
        return {"message": PASSWORD_RESET_MESSAGE}

    reset_otp, otp = password_reset_service.create_password_reset_otp(db, user)
    try:
        email_service.send_password_reset_otp(user.email, otp)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not send password reset code",
        )

    return {"message": PASSWORD_RESET_MESSAGE}


@router.post("/reset-password-with-otp", response_model=MessageResponse)
def reset_password_with_otp(
    data: ResetPasswordWithOtpRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == data.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset code",
        )

    reset_otp = password_reset_service.verify_password_reset_otp(db, user, data.otp)
    if reset_otp is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset code",
        )

    user_service.update_user_password(db, user, data.new_password)
    return {"message": "Password has been reset successfully"}

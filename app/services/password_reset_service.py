import secrets
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password, verify_password
from app.models.password_reset_otp import PasswordResetOtp
from app.models.user import User


def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def create_password_reset_otp(db: Session, user: User) -> tuple[PasswordResetOtp, str]:
    otp = generate_otp()
    db.query(PasswordResetOtp).filter(
        PasswordResetOtp.user_id == user.id,
        PasswordResetOtp.is_used.is_(False),
    ).update({"is_used": True})

    reset_otp = PasswordResetOtp(
        user_id=user.id,
        otp_hash=hash_password(otp),
        expires_at=datetime.utcnow()
        + timedelta(minutes=settings.password_reset_otp_expire_minutes),
    )
    db.add(reset_otp)
    db.commit()
    db.refresh(reset_otp)
    return reset_otp, otp


def verify_password_reset_otp(db: Session, user: User, otp: str) -> PasswordResetOtp | None:
    reset_otp = (
        db.query(PasswordResetOtp)
        .filter(
            PasswordResetOtp.user_id == user.id,
            PasswordResetOtp.is_used.is_(False),
        )
        .order_by(PasswordResetOtp.created_at.desc())
        .first()
    )
    if reset_otp is None:
        return None

    if reset_otp.expires_at < datetime.utcnow():
        reset_otp.is_used = True
        db.commit()
        return None

    if reset_otp.attempts >= settings.password_reset_otp_max_attempts:
        reset_otp.is_used = True
        db.commit()
        return None

    if not verify_password(otp, reset_otp.otp_hash):
        reset_otp.attempts += 1
        db.commit()
        return None

    reset_otp.is_used = True
    db.commit()
    db.refresh(reset_otp)
    return reset_otp

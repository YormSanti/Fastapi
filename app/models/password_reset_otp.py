from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PasswordResetOtp(Base):
    __tablename__ = "password_reset_otps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    otp_hash = Column(String(255), nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User")

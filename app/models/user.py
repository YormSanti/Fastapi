from sqlalchemy import Column, DateTime, Integer, String, func, Boolean

from app.core.database import Base
from app.core.roles import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(20), nullable=False, default=UserRole.USER.value, server_default=UserRole.USER.value)
    is_Active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

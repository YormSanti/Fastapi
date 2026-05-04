from sqlalchemy import DateTime, Integer, String, Boolean, Column, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phoneNumber = Column(String(20),unique=True, index=True,nullable=True)
    is_Active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    orders = relationship("Order", back_populates="customer")
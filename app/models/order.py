from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    order_number = Column(String(50), unique=True, index=True)
    order_date = Column(String(50))
    status = Column(String(50))
    discount_amount = Column(Float, default=0.0)
    total_amount = Column(Float)
    payment_method = Column(String(50))
    shipping_address = Column(String(255))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    
    customer = relationship("Customer", back_populates="orders")
    user = relationship("User")
    order_details = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")
    
    
    
    

from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime, func, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class OrderDetail(Base):
    __tablename__ = "orderDetails"
    OrderDetail_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product_name = Column(String(100), nullable=False)
    qty = Column(Integer)
    price = Column(Float)
    discount_amount = Column(Float, default=0.0)
    subtotal = Column(Float)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")

from datetime import datetime

from pydantic import BaseModel, ConfigDict

class OrderBase(BaseModel):
    customer_id: int
    order_number: str
    order_date: str
    status: str
    discount_amount: float | None = None
    total_amount: float
    payment_method: str
    shipping_address: str
    
class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    order_id: int
    user_id: int | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
    
class OrderUpdate(OrderBase):
    pass

class OrderDelete(BaseModel):
    order_id: int
    model_config = ConfigDict(from_attributes=True)
    

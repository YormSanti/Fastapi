from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderDetailBase(BaseModel):
    product_id: int
    qty: int
    price: float
    discount_amount: float = 0.0
    


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailUpdate(OrderDetailBase):
    pass


class OrderDetailRead(OrderDetailBase):
    OrderDetail_id: int
    order_id: int
    product_name: str
    created_at: datetime
    updated_at: datetime
    subtotal: float
    model_config = ConfigDict(from_attributes=True)


class OrderDetailDelete(BaseModel):
    OrderDetail_id: int

    model_config = ConfigDict(from_attributes=True)

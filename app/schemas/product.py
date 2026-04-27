from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.category import CategoryRead

class ProductBase(BaseModel):
    productName: str
    price: float
    description: str | None = None
    qty: int
    category_id: int | None = None
    is_Active: bool = True
   
class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: CategoryRead | None = None

    model_config = ConfigDict(from_attributes=True)
    
class ProductUpdate(ProductBase):
    pass

class ProductDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)

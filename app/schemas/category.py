from datetime import datetime

from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    name: str
    is_Active: bool = True
    
class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
    
class CategoryUpdate(CategoryBase):
    pass

class CategoryDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
    

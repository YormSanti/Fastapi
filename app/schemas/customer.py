from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CustomerBase(BaseModel):
    firstName: str
    lastName: str
    email: str
    phoneNumber: str | None = None
    is_Active: bool = True
    
class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class CustomerUpdate(CustomerBase):
    pass

class CustomerDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.roles import UserRole


class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class UserUpdate(UserCreate):
    pass


class RoleUpdate(BaseModel):
    role: UserRole


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class AdminPasswordChange(BaseModel):
    new_password: str

class UserDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)

        

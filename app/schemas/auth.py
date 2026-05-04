from pydantic import BaseModel, EmailStr

from app.core.roles import UserRole


class RegisterRequest(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    role: UserRole


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordWithOtpRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str


class MessageResponse(BaseModel):
    message: str

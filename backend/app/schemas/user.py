"""Pydantic schemas for user-related request / response payloads."""
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str = ""
    contact_number: str = ""
    user_type: str = "citizen"


class LoginRequest(BaseModel):
    username: str
    password: str


class VerifyEmailRequest(BaseModel):
    token: str


class ResendVerificationRequest(BaseModel):
    email: str


class RequestPasswordResetRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    password: str


class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: Optional[str] = ""
    contact_number: Optional[str] = ""
    user_type: str
    created_at: Optional[str] = None
    email_verified: Optional[bool] = False
    verified: Optional[bool] = False

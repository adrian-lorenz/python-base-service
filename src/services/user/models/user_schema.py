from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# Base User Schema mit gemeinsamen Attributen
class UserBase(BaseModel):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True


# Schema für User-Erstellung (Request)
class UserCreate(UserBase):
    password: str


# Schema für Update eines Users (Request)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


# Schema für die Rückgabe an den Client (Response)
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

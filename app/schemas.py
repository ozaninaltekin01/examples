from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title:str
    content:str
    published: bool = Field(default=True, description="Indicates if the post is published")

class PostRequest(PostBase):
    """Schema for creating a post"""
    pass

class PostResponse(PostBase):
    """Schema for returning a post"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, description="User's password")

class UserRequest(UserBase):
    """Schema for creating a user"""
    pass

class UserResponse(BaseModel):
    """Schema for returning a user"""
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models
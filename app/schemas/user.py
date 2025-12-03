"""
User schemas
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.models.user import UserRole
from app.schemas.base import get_list_from_json

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")
    role: UserRole = UserRole.ANALYST

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    practice: Optional[str] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    industries: Optional[List[str]] = None
    experience_years: Optional[int] = None
    certifications: Optional[List[str]] = None

class UserProfile(UserBase):
    bio: Optional[str] = None
    practice: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    industries: List[str] = Field(default_factory=list)
    experience_years: Optional[int] = None
    certifications: List[str] = Field(default_factory=list)

class UserResponse(UserProfile):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    @field_validator('skills', 'interests', 'industries', 'certifications', mode='before')
    @classmethod
    def parse_json_fields(cls, v):
        """Convert JSON string to list"""
        return get_list_from_json(v)
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

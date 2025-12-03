"""
Initiative schemas
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.models.initiative import InitiativeStatus, InitiativeDuration
from app.schemas.base import get_list_from_json

class InitiativeBase(BaseModel):
    title: str
    description: str
    practice_area: Optional[str] = None
    skills_needed: List[str] = Field(default_factory=list)
    industries: List[str] = Field(default_factory=list)
    time_commitment: Optional[str] = None
    duration: InitiativeDuration = InitiativeDuration.ONGOING
    duration_details: Optional[str] = None
    role_type: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None

class InitiativeCreate(InitiativeBase):
    pass

class InitiativeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    practice_area: Optional[str] = None
    skills_needed: Optional[List[str]] = None
    industries: Optional[List[str]] = None
    time_commitment: Optional[str] = None
    duration: Optional[InitiativeDuration] = None
    duration_details: Optional[str] = None
    role_type: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    status: Optional[InitiativeStatus] = None
    tags: Optional[List[str]] = None

class InitiativeResponse(InitiativeBase):
    id: int
    status: InitiativeStatus
    tags: List[str] = Field(default_factory=list)
    owner_id: int
    created_at: datetime
    updated_at: datetime
    view_count: int = 0
    save_count: int = 0
    application_count: int = 0
    
    @field_validator('skills_needed', 'industries', 'tags', mode='before')
    @classmethod
    def parse_json_fields(cls, v):
        """Convert JSON string to list"""
        return get_list_from_json(v)
    
    class Config:
        from_attributes = True

class InitiativeList(BaseModel):
    total: int
    items: List[InitiativeResponse]
    page: int
    page_size: int

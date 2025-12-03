"""
Engagement schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SaveInitiativeRequest(BaseModel):
    initiative_id: int

class ApplicationRequest(BaseModel):
    initiative_id: int
    message: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    initiative_id: int
    message: Optional[str]
    applied_at: datetime
    status: str
    
    class Config:
        from_attributes = True

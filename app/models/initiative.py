"""
Initiative model
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import json
from app.core.database import Base

class InitiativeStatus(str, enum.Enum):
    OPEN = "open"
    ACTIVE = "active"
    FULL = "full"
    CLOSED = "closed"

class InitiativeDuration(str, enum.Enum):
    SHORT_TERM = "short_term"
    ONGOING = "ongoing"
    FIXED_DURATION = "fixed_duration"

class Initiative(Base):
    __tablename__ = "initiatives"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # Categorization
    practice_area = Column(String, nullable=True)
    skills_needed = Column(Text, nullable=True)  # JSON array stored as text for SQLite
    industries = Column(Text, nullable=True)  # JSON array stored as text for SQLite
    tags = Column(Text, nullable=True)  # JSON array stored as text for SQLite
    
    @property
    def skills_needed_list(self):
        """Get skills_needed as list"""
        return json.loads(self.skills_needed) if self.skills_needed else []
    
    @skills_needed_list.setter
    def skills_needed_list(self, value):
        """Set skills_needed from list"""
        self.skills_needed = json.dumps(value) if value else None
    
    @property
    def industries_list(self):
        """Get industries as list"""
        return json.loads(self.industries) if self.industries else []
    
    @industries_list.setter
    def industries_list(self, value):
        """Set industries from list"""
        self.industries = json.dumps(value) if value else None
    
    @property
    def tags_list(self):
        """Get tags as list"""
        return json.loads(self.tags) if self.tags else []
    
    @tags_list.setter
    def tags_list(self, value):
        """Set tags from list"""
        self.tags = json.dumps(value) if value else None
    
    # Details
    time_commitment = Column(String, nullable=True)  # e.g., "5 hours/week"
    duration = Column(SQLEnum(InitiativeDuration), default=InitiativeDuration.ONGOING)
    duration_details = Column(String, nullable=True)  # e.g., "3 months"
    role_type = Column(String, nullable=True)  # e.g., "Researcher", "Developer"
    
    # Contact & Status
    contact_person = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    status = Column(SQLEnum(InitiativeStatus), default=InitiativeStatus.OPEN, nullable=False)
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Analytics
    view_count = Column(Integer, default=0)
    save_count = Column(Integer, default=0)
    application_count = Column(Integer, default=0)
    
    # Relationships
    owner = relationship("User", back_populates="initiatives")
    saved_by = relationship("SavedInitiative", back_populates="initiative", cascade="all, delete-orphan")
    applications = relationship("InitiativeApplication", back_populates="initiative", cascade="all, delete-orphan")
    views = relationship("InitiativeView", back_populates="initiative", cascade="all, delete-orphan")

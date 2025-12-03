"""
User model
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import json
from app.core.database import Base

class UserRole(str, enum.Enum):
    ANALYST = "analyst"
    LEADER = "leader"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    azure_id = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.ANALYST, nullable=False)
    
    # Profile fields
    bio = Column(Text, nullable=True)
    practice = Column(String, nullable=True)  # Strategy, Technology, Risk, etc.
    skills = Column(Text, nullable=True)  # JSON array stored as text for SQLite
    interests = Column(Text, nullable=True)  # JSON array stored as text for SQLite
    industries = Column(Text, nullable=True)  # JSON array stored as text for SQLite
    experience_years = Column(Integer, nullable=True)
    certifications = Column(Text, nullable=True)  # JSON array stored as text for SQLite
    
    @property
    def skills_list(self):
        """Get skills as list"""
        return json.loads(self.skills) if self.skills else []
    
    @skills_list.setter
    def skills_list(self, value):
        """Set skills from list"""
        self.skills = json.dumps(value) if value else None
    
    @property
    def interests_list(self):
        """Get interests as list"""
        return json.loads(self.interests) if self.interests else []
    
    @interests_list.setter
    def interests_list(self, value):
        """Set interests from list"""
        self.interests = json.dumps(value) if value else None
    
    @property
    def industries_list(self):
        """Get industries as list"""
        return json.loads(self.industries) if self.industries else []
    
    @industries_list.setter
    def industries_list(self, value):
        """Set industries from list"""
        self.industries = json.dumps(value) if value else None
    
    @property
    def certifications_list(self):
        """Get certifications as list"""
        return json.loads(self.certifications) if self.certifications else []
    
    @certifications_list.setter
    def certifications_list(self, value):
        """Set certifications from list"""
        self.certifications = json.dumps(value) if value else None
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    initiatives = relationship("Initiative", back_populates="owner", cascade="all, delete-orphan")
    saved_initiatives = relationship("SavedInitiative", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("InitiativeApplication", back_populates="user", cascade="all, delete-orphan")
    views = relationship("InitiativeView", back_populates="user", cascade="all, delete-orphan")

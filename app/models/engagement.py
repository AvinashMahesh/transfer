"""
User engagement models
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class SavedInitiative(Base):
    __tablename__ = "saved_initiatives"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    initiative_id = Column(Integer, ForeignKey("initiatives.id"), nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="saved_initiatives")
    initiative = relationship("Initiative", back_populates="saved_by")
    
    __table_args__ = (UniqueConstraint('user_id', 'initiative_id', name='unique_user_saved_initiative'),)

class InitiativeApplication(Base):
    __tablename__ = "initiative_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    initiative_id = Column(Integer, ForeignKey("initiatives.id"), nullable=False)
    message = Column(Text, nullable=True)
    applied_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, accepted, rejected
    
    # Relationships
    user = relationship("User", back_populates="applications")
    initiative = relationship("Initiative", back_populates="applications")
    
    __table_args__ = (UniqueConstraint('user_id', 'initiative_id', name='unique_user_initiative_application'),)

class InitiativeView(Base):
    __tablename__ = "initiative_views"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    initiative_id = Column(Integer, ForeignKey("initiatives.id"), nullable=False)
    viewed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="views")
    initiative = relationship("Initiative", back_populates="views")

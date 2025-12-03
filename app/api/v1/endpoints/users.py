"""
User management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserResponse, summary="Get current user profile")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current authenticated user's profile.
    """
    return UserResponse.model_validate(current_user)

@router.put("/me", response_model=UserResponse, summary="Update current user profile")
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the current authenticated user's profile.
    
    Allows updating:
    - Basic info (name, bio)
    - Practice area
    - Skills and interests
    - Industry preferences
    - Experience and certifications
    """
    import json
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Convert list fields to JSON strings for SQLite
    json_fields = ['skills', 'interests', 'industries', 'certifications']
    for field, value in update_data.items():
        if field in json_fields and isinstance(value, list):
            setattr(current_user, field, json.dumps(value))
        else:
            setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse.model_validate(current_user)

@router.get("/{user_id}", response_model=UserResponse, summary="Get user by ID")
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a user's profile by ID.
    
    Requires authentication.
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(user)

@router.get("/", response_model=List[UserResponse], summary="List all users")
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all users (paginated).
    
    Requires authentication.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserResponse.model_validate(user) for user in users]

"""
Initiative management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_leader
from app.models.user import User
from app.models.initiative import Initiative, InitiativeStatus
from app.schemas.initiative import InitiativeCreate, InitiativeUpdate, InitiativeResponse, InitiativeList

router = APIRouter()

@router.post("/", response_model=InitiativeResponse, status_code=status.HTTP_201_CREATED, summary="Create initiative")
async def create_initiative(
    initiative_data: InitiativeCreate,
    current_user: User = Depends(get_current_leader),
    db: Session = Depends(get_db)
):
    """
    Create a new initiative.
    
    Requires leader role.
    
    The initiative will automatically:
    - Generate AI tags based on description (future enhancement)
    - Create vector embeddings for semantic search (future enhancement)
    """
    import json
    
    # Convert initiative data and handle JSON fields
    data = initiative_data.model_dump()
    json_fields = ['skills_needed', 'industries', 'tags']
    for field in json_fields:
        if field in data and isinstance(data[field], list):
            data[field] = json.dumps(data[field])
    
    # Create initiative
    initiative = Initiative(
        **data,
        owner_id=current_user.id
    )
    
    # TODO: Generate AI tags from description
    # TODO: Create vector embeddings for semantic search
    
    db.add(initiative)
    db.commit()
    db.refresh(initiative)
    
    return InitiativeResponse.model_validate(initiative)

@router.get("/", response_model=InitiativeList, summary="List initiatives")
async def list_initiatives(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[InitiativeStatus] = None,
    practice_area: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List initiatives with optional filtering.
    
    Supports filtering by:
    - Status (open, active, full, closed)
    - Practice area
    
    Pagination via skip and limit parameters.
    """
    query = db.query(Initiative)
    
    # Apply filters
    if status:
        query = query.filter(Initiative.status == status)
    if practice_area:
        query = query.filter(Initiative.practice_area == practice_area)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    initiatives = query.offset(skip).limit(limit).all()
    
    return InitiativeList(
        total=total,
        items=[InitiativeResponse.model_validate(i) for i in initiatives],
        page=skip // limit + 1,
        page_size=limit
    )

@router.get("/{initiative_id}", response_model=InitiativeResponse, summary="Get initiative by ID")
async def get_initiative(
    initiative_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get a specific initiative by ID.
    
    Increments view count if user is authenticated.
    """
    initiative = db.query(Initiative).filter(Initiative.id == initiative_id).first()
    
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Initiative not found"
        )
    
    # Increment view count
    initiative.view_count += 1
    db.commit()
    db.refresh(initiative)
    
    return InitiativeResponse.model_validate(initiative)

@router.put("/{initiative_id}", response_model=InitiativeResponse, summary="Update initiative")
async def update_initiative(
    initiative_id: int,
    initiative_update: InitiativeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an initiative.
    
    Only the initiative owner or admin can update.
    """
    initiative = db.query(Initiative).filter(Initiative.id == initiative_id).first()
    
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Initiative not found"
        )
    
    # Check ownership
    if initiative.owner_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this initiative"
        )
    
    # Update fields
    import json
    update_data = initiative_update.model_dump(exclude_unset=True)
    
    # Convert list fields to JSON strings for SQLite
    json_fields = ['skills_needed', 'industries', 'tags']
    for field, value in update_data.items():
        if field in json_fields and isinstance(value, list):
            setattr(initiative, field, json.dumps(value))
        else:
            setattr(initiative, field, value)
    
    # TODO: Regenerate embeddings if description changed
    
    db.commit()
    db.refresh(initiative)
    
    return InitiativeResponse.model_validate(initiative)

@router.delete("/{initiative_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete initiative")
async def delete_initiative(
    initiative_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an initiative.
    
    Only the initiative owner or admin can delete.
    """
    initiative = db.query(Initiative).filter(Initiative.id == initiative_id).first()
    
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Initiative not found"
        )
    
    # Check ownership
    if initiative.owner_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this initiative"
        )
    
    db.delete(initiative)
    db.commit()
    
    return None

@router.get("/my/initiatives", response_model=List[InitiativeResponse], summary="Get my initiatives")
async def get_my_initiatives(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all initiatives created by the current user.
    """
    initiatives = db.query(Initiative).filter(Initiative.owner_id == current_user.id).all()
    return [InitiativeResponse.model_validate(i) for i in initiatives]

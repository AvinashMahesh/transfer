"""
User engagement endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.initiative import Initiative
from app.models.engagement import SavedInitiative, InitiativeApplication, InitiativeView
from app.schemas.engagement import SaveInitiativeRequest, ApplicationRequest, ApplicationResponse
from app.schemas.initiative import InitiativeResponse

router = APIRouter()

@router.post("/save", status_code=status.HTTP_201_CREATED, summary="Save/bookmark initiative")
async def save_initiative(
    request: SaveInitiativeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Save/bookmark an initiative for later.
    
    Saved initiatives appear in the user's saved list.
    """
    # Check if initiative exists
    initiative = db.query(Initiative).filter(Initiative.id == request.initiative_id).first()
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Initiative not found"
        )
    
    # Check if already saved
    existing = db.query(SavedInitiative).filter(
        SavedInitiative.user_id == current_user.id,
        SavedInitiative.initiative_id == request.initiative_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Initiative already saved"
        )
    
    # Save initiative
    saved = SavedInitiative(
        user_id=current_user.id,
        initiative_id=request.initiative_id
    )
    
    # Increment save count
    initiative.save_count += 1
    
    db.add(saved)
    db.commit()
    
    return {"message": "Initiative saved successfully"}

@router.delete("/save/{initiative_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove saved initiative")
async def unsave_initiative(
    initiative_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove an initiative from saved/bookmarked list.
    """
    saved = db.query(SavedInitiative).filter(
        SavedInitiative.user_id == current_user.id,
        SavedInitiative.initiative_id == initiative_id
    ).first()
    
    if not saved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved initiative not found"
        )
    
    # Decrement save count
    initiative = db.query(Initiative).filter(Initiative.id == initiative_id).first()
    if initiative:
        initiative.save_count = max(0, initiative.save_count - 1)
    
    db.delete(saved)
    db.commit()
    
    return None

@router.get("/saved", response_model=List[InitiativeResponse], summary="Get saved initiatives")
async def get_saved_initiatives(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all initiatives saved/bookmarked by the current user.
    """
    saved_records = db.query(SavedInitiative).filter(
        SavedInitiative.user_id == current_user.id
    ).all()
    
    initiative_ids = [s.initiative_id for s in saved_records]
    initiatives = db.query(Initiative).filter(Initiative.id.in_(initiative_ids)).all()
    
    return [InitiativeResponse.model_validate(i) for i in initiatives]

@router.post("/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED, summary="Apply to initiative")
async def apply_to_initiative(
    request: ApplicationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Express interest or apply to an initiative.
    
    The application includes an optional message to the initiative owner.
    """
    # Check if initiative exists
    initiative = db.query(Initiative).filter(Initiative.id == request.initiative_id).first()
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Initiative not found"
        )
    
    # Check if already applied
    existing = db.query(InitiativeApplication).filter(
        InitiativeApplication.user_id == current_user.id,
        InitiativeApplication.initiative_id == request.initiative_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already applied to this initiative"
        )
    
    # Create application
    application = InitiativeApplication(
        user_id=current_user.id,
        initiative_id=request.initiative_id,
        message=request.message
    )
    
    # Increment application count
    initiative.application_count += 1
    
    db.add(application)
    db.commit()
    db.refresh(application)
    
    return ApplicationResponse.model_validate(application)

@router.get("/applications", response_model=List[ApplicationResponse], summary="Get my applications")
async def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all applications submitted by the current user.
    """
    applications = db.query(InitiativeApplication).filter(
        InitiativeApplication.user_id == current_user.id
    ).all()
    
    return [ApplicationResponse.model_validate(a) for a in applications]

@router.get("/initiative/{initiative_id}/applications", response_model=List[ApplicationResponse], summary="Get initiative applications")
async def get_initiative_applications(
    initiative_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all applications for a specific initiative.
    
    Only accessible by the initiative owner or admin.
    """
    # Check if initiative exists and user owns it
    initiative = db.query(Initiative).filter(Initiative.id == initiative_id).first()
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Initiative not found"
        )
    
    if initiative.owner_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view applications for this initiative"
        )
    
    applications = db.query(InitiativeApplication).filter(
        InitiativeApplication.initiative_id == initiative_id
    ).all()
    
    return [ApplicationResponse.model_validate(a) for a in applications]

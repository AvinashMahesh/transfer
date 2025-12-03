"""
AI-powered recommendation endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.initiative import Initiative
from app.schemas.initiative import InitiativeResponse
from pydantic import BaseModel

router = APIRouter()

class RecommendationResponse(BaseModel):
    """Recommendation with explanation"""
    initiative: InitiativeResponse
    score: float
    explanation: str

@router.get("/", response_model=List[RecommendationResponse], summary="Get personalized recommendations")
async def get_recommendations(
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered personalized initiative recommendations.
    
    Recommendations are based on:
    - **User profile**: Skills, interests, industry preferences
    - **Past interactions**: Previously viewed and saved initiatives
    - **Semantic matching**: Profile and initiative embeddings
    - **Collaborative filtering**: Similar users' preferences
    
    Each recommendation includes:
    - The initiative details
    - Match score (0-1)
    - Explanation of why it was recommended
    
    **Note**: This is a simplified implementation. Full AI recommendation requires:
    1. User profile embeddings
    2. Initiative embeddings
    3. Interaction history analysis
    4. Hybrid recommendation algorithm (content + collaborative filtering)
    """
    # TODO: Implement full AI recommendation engine
    # For now, use simple matching based on skills and interests
    
    recommendations = []
    
    # Get all open initiatives
    initiatives = db.query(Initiative).filter(
        Initiative.status == "open"
    ).all()
    
    # Simple scoring based on skill overlap
    from app.schemas.base import get_list_from_json
    
    for initiative in initiatives:
        score = 0.0
        explanations = []
        
        # Match skills
        user_skills = set(get_list_from_json(current_user.skills))
        initiative_skills = set(get_list_from_json(initiative.skills_needed))
        skill_overlap = user_skills.intersection(initiative_skills)
        
        if skill_overlap:
            score += len(skill_overlap) * 0.3
            explanations.append(f"Matched skills: {', '.join(skill_overlap)}")
        
        # Match interests
        user_interests = set(get_list_from_json(current_user.interests))
        initiative_tags = set(get_list_from_json(initiative.tags))
        interest_overlap = user_interests.intersection(initiative_tags)
        
        if interest_overlap:
            score += len(interest_overlap) * 0.2
            explanations.append(f"Aligned with interests: {', '.join(interest_overlap)}")
        
        # Match industries
        user_industries = set(get_list_from_json(current_user.industries))
        initiative_industries = set(get_list_from_json(initiative.industries))
        industry_overlap = user_industries.intersection(initiative_industries)
        
        if industry_overlap:
            score += len(industry_overlap) * 0.2
            explanations.append(f"Industry match: {', '.join(industry_overlap)}")
        
        # Match practice area
        if current_user.practice and current_user.practice == initiative.practice_area:
            score += 0.3
            explanations.append(f"Same practice area: {current_user.practice}")
        
        # Only include if there's some match
        if score > 0:
            explanation = "; ".join(explanations) if explanations else "General match based on profile"
            recommendations.append(
                RecommendationResponse(
                    initiative=InitiativeResponse.model_validate(initiative),
                    score=min(score, 1.0),  # Cap at 1.0
                    explanation=explanation
                )
            )
    
    # Sort by score and return top N
    recommendations.sort(key=lambda x: x.score, reverse=True)
    return recommendations[:limit]

@router.get("/user/{user_id}", response_model=List[RecommendationResponse], summary="Get recommendations for user")
async def get_user_recommendations(
    user_id: int,
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get recommendations for a specific user.
    
    This endpoint allows leaders/admins to see what initiatives
    would be recommended for specific analysts.
    """
    # Get target user
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Use same logic as above but for target user
    # (In production, this would call the same recommendation service)
    recommendations = []
    initiatives = db.query(Initiative).filter(Initiative.status == "open").all()
    
    from app.schemas.base import get_list_from_json
    
    for initiative in initiatives:
        score = 0.0
        explanations = []
        
        # Match skills
        user_skills = set(get_list_from_json(target_user.skills))
        initiative_skills = set(get_list_from_json(initiative.skills_needed))
        skill_overlap = user_skills.intersection(initiative_skills)
        
        if skill_overlap:
            score += len(skill_overlap) * 0.3
            explanations.append(f"Matched skills: {', '.join(skill_overlap)}")
        
        # Match practice area
        if target_user.practice and target_user.practice == initiative.practice_area:
            score += 0.3
            explanations.append(f"Same practice area: {target_user.practice}")
        
        if score > 0:
            explanation = "; ".join(explanations) if explanations else "General match"
            recommendations.append(
                RecommendationResponse(
                    initiative=InitiativeResponse.model_validate(initiative),
                    score=min(score, 1.0),
                    explanation=explanation
                )
            )
    
    recommendations.sort(key=lambda x: x.score, reverse=True)
    return recommendations[:limit]

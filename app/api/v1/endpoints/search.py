"""
Search and filtering endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from app.core.database import get_db
from app.models.initiative import Initiative
from app.schemas.initiative import InitiativeResponse, InitiativeList

router = APIRouter()

@router.get("/", response_model=InitiativeList, summary="Search initiatives")
async def search_initiatives(
    q: Optional[str] = Query(None, description="Search query (searches title and description)"),
    skills: Optional[List[str]] = Query(None, description="Filter by required skills"),
    practice_area: Optional[str] = Query(None, description="Filter by practice area"),
    industries: Optional[List[str]] = Query(None, description="Filter by industries"),
    time_commitment: Optional[str] = Query(None, description="Filter by time commitment"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search and filter initiatives.
    
    Supports:
    - **Text search**: Natural language search across title and description
    - **Skills filter**: Match initiatives requiring specific skills
    - **Practice area**: Filter by practice (Strategy, Technology, etc.)
    - **Industries**: Filter by target industries
    - **Time commitment**: Filter by expected time commitment
    
    Examples:
    - `/search?q=AI healthcare` - Search for AI healthcare initiatives
    - `/search?skills=Python&skills=Machine Learning` - Find initiatives needing Python and ML
    - `/search?practice_area=Technology&time_commitment=5 hours/week` - Technology initiatives with specific commitment
    
    Future enhancement: This will use vector embeddings for semantic search.
    """
    query = db.query(Initiative)
    
    # Text search (basic implementation - will be replaced with vector search)
    if q:
        search_filter = or_(
            Initiative.title.ilike(f"%{q}%"),
            Initiative.description.ilike(f"%{q}%")
        )
        query = query.filter(search_filter)
    
    # Skills filter (match any of the requested skills)
    if skills:
        for skill in skills:
            query = query.filter(Initiative.skills_needed.any(skill))
    
    # Practice area filter
    if practice_area:
        query = query.filter(Initiative.practice_area == practice_area)
    
    # Industries filter
    if industries:
        for industry in industries:
            query = query.filter(Initiative.industries.any(industry))
    
    # Time commitment filter
    if time_commitment:
        query = query.filter(Initiative.time_commitment == time_commitment)
    
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

@router.get("/semantic", response_model=InitiativeList, summary="Semantic search (AI-powered)")
async def semantic_search(
    query: str = Query(..., description="Natural language search query"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    AI-powered semantic search using vector embeddings.
    
    Examples:
    - "Find initiatives involving AI and healthcare"
    - "Available short-term volunteering projects"
    - "Innovation opportunities in financial services"
    
    This endpoint uses vector embeddings to understand the semantic meaning
    of your query and find the most relevant initiatives.
    
    **Note**: This is a placeholder. Full implementation requires:
    1. Embedding generation for initiatives
    2. Vector database integration (Qdrant)
    3. Cosine similarity matching
    """
    # TODO: Implement vector search
    # 1. Generate embedding for query
    # 2. Search vector database
    # 3. Retrieve matching initiative IDs
    # 4. Return ranked results
    
    # For now, fall back to basic text search
    search_filter = or_(
        Initiative.title.ilike(f"%{query}%"),
        Initiative.description.ilike(f"%{query}%")
    )
    
    initiatives = db.query(Initiative).filter(search_filter).limit(limit).all()
    
    return InitiativeList(
        total=len(initiatives),
        items=[InitiativeResponse.model_validate(i) for i in initiatives],
        page=1,
        page_size=limit
    )

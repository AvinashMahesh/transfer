"""
API router aggregation
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, initiatives, search, recommendations, engagement

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(initiatives.router, prefix="/initiatives", tags=["Initiatives"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(engagement.router, prefix="/engagement", tags=["Engagement"])

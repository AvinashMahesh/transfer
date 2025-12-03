"""
Main FastAPI application entry point for Deloitte Initiative Discovery Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## Deloitte Initiative Discovery Platform API
    
    A unified platform for Deloitte analysts to discover and engage with firm initiatives.
    
    ### Features:
    * **Authentication**: Azure AD B2C SSO integration
    * **User Profiles**: Manage analyst and leader profiles
    * **Initiative Management**: Create, update, and manage initiatives
    * **Discovery Tools**: Search, filter, and browse initiatives
    * **AI Recommendations**: Personalized initiative matching
    * **Engagement**: Save, bookmark, and track initiatives
    
    ### User Roles:
    * **Analyst**: Browse, search, and receive recommendations
    * **Leader**: Create and manage initiatives
    """,
    openapi_tags=[
        {"name": "Authentication", "description": "User authentication and authorization"},
        {"name": "Users", "description": "User profile management"},
        {"name": "Initiatives", "description": "Initiative CRUD operations"},
        {"name": "Search", "description": "Search and filtering capabilities"},
        {"name": "Recommendations", "description": "AI-powered personalized recommendations"},
        {"name": "Engagement", "description": "User engagement tracking"},
    ]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Deloitte Initiative Discovery Platform API",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Root"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserResponse
from pydantic import BaseModel, EmailStr

router = APIRouter()

class LoginRequest(BaseModel):
    """Login request with email and password"""
    email: EmailStr
    password: str

class AzureADToken(BaseModel):
    """Azure AD token (for future implementation)"""
    access_token: str

@router.post("/login", response_model=Token, summary="Login with email and password")
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint using email and password.
    
    Authenticates user credentials and returns a JWT access token.
    
    **Test Accounts:**
    - analyst@deloitte.com / password123
    - leader@deloitte.com / password123
    - admin@deloitte.com / password123
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    
    return Token(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )

@router.post("/register", response_model=UserResponse, summary="Register new user")
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user with email and password.
    
    Creates a new account in the system.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Hash the password
    password_hash = get_password_hash(user_data.password)
    
    # Create new user
    user = User(
        email=user_data.email,
        password_hash=password_hash,
        full_name=user_data.full_name,
        role=user_data.role
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return UserResponse.model_validate(user)

@router.post("/azure-login", response_model=Token, summary="Azure AD B2C login (future)")
async def azure_login(
    token: AzureADToken,
    db: Session = Depends(get_db)
):
    """
    Azure AD B2C login endpoint (placeholder for production implementation).
    
    This endpoint would:
    1. Validate the Azure AD token using MSAL
    2. Extract user claims (email, name, groups)
    3. Map Azure AD groups to user roles
    4. Create/update user in database
    5. Return JWT for API access
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Azure AD integration not yet implemented. Use /auth/login for testing."
    )

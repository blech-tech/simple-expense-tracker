"""
FastAPI application for Simple Expense Tracker
Main application file with authentication and expense management endpoints
"""

# Standard library imports
from datetime import datetime, timedelta
from typing import List
from uuid import UUID

# Third-party imports
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.security.http import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Local imports
from database import SessionLocal
import models
import schemas
import os

# =============================================================================
# FastAPI Application Setup
# =============================================================================

app = FastAPI(
    title="Simple Expense Tracker API",
    description="A simple API for tracking personal expenses",
    version="1.0.0",
    root_path="/api"
)

# CORS Configuration
origins_str = os.getenv("CORS_ORIGINS", "http://localhost:5173")
origins = origins_str.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# Configuration Constants
# =============================================================================

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# =============================================================================
# Security Setup
# =============================================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bearer_token_scheme = HTTPBearer()

# =============================================================================
# Database Dependency
# =============================================================================

def get_db() -> Session:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =============================================================================
# Security Helper Functions
# =============================================================================

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(
    token: str = Depends(bearer_token_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user

# =============================================================================
# Application Lifecycle Events
# =============================================================================

@app.on_event("startup")
def on_startup():
    """Application startup event handler"""
    # Database migrations are handled by Alembic
    pass

# =============================================================================
# Health Check Endpoint
# =============================================================================

@app.get("/")
def read_root() -> dict[str, str]:
    """Health check endpoint"""
    return {"message": "Simple Expense Tracker API is running"}

# =============================================================================
# Authentication Endpoints
# =============================================================================

@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> dict[str, str]:
    """Authenticate user and return access token"""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# =============================================================================
# User Management Endpoints
# =============================================================================

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
) -> models.User:
    """Create a new user account"""
    # Check if username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Hash password and create new user
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# =============================================================================
# Expense Management Endpoints
# =============================================================================

@app.post("/expenses/", response_model=schemas.ExpenseResponse)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> models.Expense:
    """Create a new expense for the authenticated user"""
    db_expense = models.Expense(
        description=expense.description,
        amount=expense.amount,
        user_id=current_user.id
    )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    return db_expense

@app.get("/expenses/", response_model=List[schemas.ExpenseResponse])
def get_expenses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> List[models.Expense]:
    """Get all expenses for the authenticated user"""
    expenses = db.query(models.Expense).filter(
        models.Expense.user_id == current_user.id
    ).all()
    
    return expenses

@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: UUID, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Найти расход по ID и проверить его владельца
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found or you don't have permission to delete it")
    
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}

@app.put("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(
    expense_id: UUID,
    expense_update: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Найти расход по ID и проверить его владельца
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found or you don't have permission to update it")
    
    # Обновить поля расхода
    expense.description = expense_update.description
    expense.amount = expense_update.amount
    
    db.commit()
    db.refresh(expense)
    return expense

# =============================================================================
# Application Entry Point
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
# backend/schemas.py

from pydantic import BaseModel, Field
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str

    class Config:
        from_attributes = True

class ExpenseCreate(BaseModel):
    description: str
    amount: float

class ExpenseResponse(BaseModel):
    id: UUID
    description: str
    amount: float

    class Config:
        from_attributes = True
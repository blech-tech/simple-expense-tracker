from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

# Import your SQLAlchemy models
from .database import SessionLocal
from . import models

app = FastAPI()

# Your CORS settings...
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic model for creating a new expense
class ExpenseCreate(BaseModel):
    description: str
    amount: float


# Pydantic model for a full expense, with the UUID type
class Expense(BaseModel):
    id: UUID
    description: str
    amount: float


@app.on_event("startup")
def on_startup():
    # We will use Alembic for migrations, so we can remove init_db()
    pass


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.post("/expenses/", response_model=Expense)
def create_expense(expense: ExpenseCreate):  # Use ExpenseCreate here
    db = SessionLocal()
    # Create the SQLAlchemy model instance
    db_expense = models.Expense(description=expense.description, amount=expense.amount)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    db.close()
    return db_expense


@app.get("/expenses/", response_model=List[Expense])
def get_expenses():
    db = SessionLocal()
    expenses = db.query(models.Expense).all()
    db.close()
    return expenses


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: UUID):
    db = SessionLocal()
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    db.close()
    return {"message": "Expense deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
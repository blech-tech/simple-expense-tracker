from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from uuid import uuid4

app = FastAPI()

class Expense(BaseModel):
    id: str
    description: str
    amount: float

# Временное хранилище в памяти
expenses_db: Dict[str, Expense] = {}

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.post("/expenses/")
async def create_expense(expense: Expense):
    expense.id = str(uuid4()) # Генерируем уникальный ID
    expenses_db[expense.id] = expense
    return expense

@app.get("/expenses/", response_model=List[Expense])
async def get_expenses():
    return list(expenses_db.values())

@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: str):
    if expense_id not in expenses_db:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses_db[expense_id]
    return {"message": "Expense deleted successfully"}
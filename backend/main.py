from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from uuid import uuid4

app = FastAPI()

# Список разрешенных адресов (доменов/портов)
origins = [
    "http://localhost:5173",  # Адрес твоего фронтенда
    "http://127.0.0.1:5173", # Ещё один вариант localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP-методы (GET, POST, DELETE и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

class ExpenseCreate(BaseModel):
    description: str
    amount: float

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
async def create_expense(expense: ExpenseCreate):
    # Генерируем ID внутри бэкенда
    expense_with_id = Expense(id=str(uuid4()), description=expense.description, amount=expense.amount)
    expenses_db[expense_with_id.id] = expense_with_id
    return expense_with_id

@app.get("/expenses/", response_model=List[Expense])
async def get_expenses():
    return list(expenses_db.values())

@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: str):
    if expense_id not in expenses_db:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses_db[expense_id]
    return {"message": "Expense deleted successfully"}
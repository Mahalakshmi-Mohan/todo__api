# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, crud
from app.database import SessionLocal, engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos/", response_model=schemas.ToDoItem)
def create_todo_item(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    return crud.create_todo_item(db=db, todo=todo)

@app.get("/todos/", response_model=List[schemas.ToDoItem])
def read_todo_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_todo_items(db=db, skip=skip, limit=limit)

@app.get("/todos/{todo_id}", response_model=schemas.ToDoItem)
def read_todo_item(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo_item(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return db_todo

@app.put("/todos/{todo_id}", response_model=schemas.ToDoItem)
def update_todo_item(todo_id: int, todo: schemas.ToDoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo_item(db=db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo_item(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo_item(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return {"detail": "ToDo item deleted"}

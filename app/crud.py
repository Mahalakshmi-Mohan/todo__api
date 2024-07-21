# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def create_todo_item(db: Session, todo: schemas.ToDoCreate):
    db_todo = models.ToDoItem(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ToDoItem).offset(skip).limit(limit).all()

def get_todo_item(db: Session, todo_id: int):
    return db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).first()

def update_todo_item(db: Session, todo_id: int, todo: schemas.ToDoUpdate):
    db_todo = db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).first()
    if db_todo is None:
        return None
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo_item(db: Session, todo_id: int):
    db_todo = db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).first()
    if db_todo is None:
        return None
    db.delete(db_todo)
    db.commit()
    return db_todo


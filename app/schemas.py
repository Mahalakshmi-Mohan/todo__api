# app/schemas.py

from pydantic import BaseModel

class ToDoBase(BaseModel):
    title: str
    description: str
    completed: bool = False

class ToDoCreate(ToDoBase):
    pass

class ToDoUpdate(ToDoBase):
    pass

class ToDoItem(ToDoBase):
    id: int

    class Config:
        orm_mode = True

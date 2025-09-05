from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class Task(TaskBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True

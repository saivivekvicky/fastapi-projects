from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="To-Do App")

# Create a new task
@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task(db, task)

# Get all tasks
@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(db: Session = Depends(database.get_db)):
    return crud.get_tasks(db)

# Update a task (mark complete or change title)
@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    db_task = crud.update_task(db, task_id, task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

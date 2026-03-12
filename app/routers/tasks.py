from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
def add_task(data: TaskCreate, db: Session = Depends(get_db)) :
    task = Task(
        title = data.title,
        description = data.description,
        status = data.status,
        user_id = data.user_id,
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.deleted_at.is_(None)).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)) :
    task = db.query(Task).filter(Task.id == task_id, Task.deleted_at.is_(None)).first()
    if not task :
        raise HTTPException(status_code=404, detail="Task introuvable")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)) :
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task :
        raise HTTPException(status_code=404, detail="Task introuvable")
    
    update_fields = data.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(task, key, value)
        
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)) :
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task :
        raise HTTPException(status_code=404, detail="Task introuvable")
    
    if task.deleted_at is not None:
        raise HTTPException(status_code=400, detail="Task déjà supprimée")
    
    task.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return {"details" : "La tâche à bien été supprimer !"}
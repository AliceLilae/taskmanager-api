from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from app.models.task import Status


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Status = Status.PENDING
    user_id: int


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Status
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
        
class TaskUpdate(BaseModel) :
    title : Optional[str] = None
    description : Optional[str] = None
    status : Optional[Status] = None
    user_id : Optional[int] = None
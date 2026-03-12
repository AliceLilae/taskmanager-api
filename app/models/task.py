import enum

from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func

class Status(enum.Enum) :
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class User(Base) :
    __tablename__ = "users"
    
    id : int = Column(Integer, primary_key=True, index=True)
    name : str = Column(String, nullable=False)
    username : str = Column(String, nullable=True)
    email : str = Column(String, nullable=False)
    password_hash : str = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    deleted_at = Column(DateTime, nullable=True)
    
    
class Task(Base) :
    __tablename__ = "tasks"
    
    id : int = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title : str = Column(String, nullable=False)
    description : str = Column(String, nullable=True)
    status = Column(Enum(Status), default=Status.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    deleted_at = Column(DateTime, nullable=True)

from sqlalchemy import Column, String, JSON, DateTime, func
from app.database import Base
from uuid import uuid4

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    file_name = Column(String, nullable=False)
    status = Column(String, default="pending")
    extracted_data = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

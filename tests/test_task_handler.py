import pytest
from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.task_handler import TaskHandler
from app.models import Task

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture
def handler(db_session):
    return TaskHandler(session=lambda: db_session)

def test_create_new_task(handler, db_session):
    mock_file = Mock()
    mock_file.filename = "test.zip"
    mock_background_tasks = Mock()
    
    result = handler.create_new_task(mock_file, mock_background_tasks)
    
    assert "task_id" in result
    assert result["status"] == "pending"
    
    task = db_session.query(Task).filter(Task.id == result["task_id"]).first()
    assert task is not None
    assert task.file_name == "test.zip"

def test_get_task_from_db(handler, db_session):
    task = Task(id="123", file_name="test.zip")
    db_session.add(task)
    db_session.commit()
    
    result = handler.get_task_from_db("123")
    
    assert result["id"] == "123"
    assert result["file_name"] == "test.zip"
    assert result["status"] == "pending"

def test_get_task_not_found(handler):
    with pytest.raises(Exception) as exc:
        handler.get_task_from_db("nonexistent")
    assert exc.value.status_code == 404


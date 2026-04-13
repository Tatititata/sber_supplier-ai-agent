from app.database import SessionLocal
from app.models import Task
from fastapi import HTTPException, BackgroundTasks
from time import sleep
from random import randint, sample
from string import ascii_lowercase



class TaskHandler:

    def __init__(self, session=None):
        self._session = SessionLocal if session is None else session

    
    def create_new_task(self, file, background_tasks: BackgroundTasks):
        db = self._session()
        try:
            task = Task(file_name=file.filename)
            db.add(task)
            db.commit()
            background_tasks.add_task(self._process_file, task.id, file)
            return {"task_id": task.id, "status": 'pending'}
        finally:
            db.close()
    
    def get_task_from_db(self, task_id):
        db = self._session()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                raise HTTPException(404, "Task not found")
            return {
                "id": task.id,
                "file_name": task.file_name,
                "status": task.status,
                "extracted_data": task.extracted_data,
                "error": task.error,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            }
        finally:
            db.close()

    def _process_file(self, task_id: str, file):

        sleep(1)
        db = self._session()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            task.status = "processing"
            db.commit()
            sleep(3)  
            
            if randint(0, 3) > 2:
                task.status = "failed"
                task.error = 'Can not load data from file'
            else:
                suppliers = []
                for i in range(randint(1, 3)):
                    name = ''.join(sample(ascii_lowercase, randint(5, 10))).capitalize()
                    items = []
                    for j in range(randint(1, 3)):
                        items.append({
                            'product': ''.join(sample(ascii_lowercase, randint(10, 15))).capitalize(),
                            'price': randint(10000, 100000)
                        })
                    suppliers.append({
                        'name': name,
                        'items': items
                    })
                task.status = "completed"
                task.extracted_data = {'suppliers': suppliers}
            db.commit()

        except Exception as e:
            db.rollback()
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = "failed"
                task.error = str(e)
                db.commit()
        finally:
            db.close()

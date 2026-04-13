from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import AuthHandler
from app.task_handler import TaskHandler



app = FastAPI(title="Supplier AI Agent")
auth = AuthHandler()
worker = TaskHandler()

@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    user = auth.authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/cp/tasks")
def create_task(request: Request, background_task : BackgroundTasks, file: UploadFile = File(...)):
    username = auth.validate_user(request.headers)
    if not username:
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    return worker.create_new_task(file, background_task)
    
@app.get("/cp/tasks/{task_id}")
def task_from_db(request: Request, task_id: str):
    username = auth.validate_user(request.headers)
    if not username:
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    return worker.get_task_from_db(task_id)
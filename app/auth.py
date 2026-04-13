from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from fastapi.security import HTTPBearer

class AuthHandler:
    def __init__(self):
        self.secret_key = "my-very-long-secret-key-for-supplier-ai-test-task"
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.security = HTTPBearer()
        
        self.fake_users_db = {
            "user": {
                "username": "user",
                "hashed_password": self.pwd_context.hash("userpassword"),
                "role": "user"
            },
            "admin": {
                "username": "admin",
                "hashed_password": self.pwd_context.hash("adminpassword"),
                "role": "admin"
            }
        }
    
    def authenticate_user(self, username: str, password:str):

        user = self.fake_users_db.get(username)
        if not user or not self.pwd_context.verify(password, user["hashed_password"]):
            return False
        return {'sub': user['username'], 'role': user['role']}
    

    def create_access_token(self, data: dict):
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        data["exp"]  = expire
        return jwt.encode(data, self.secret_key, algorithm=self.algorithm)
    

    def validate_user(self, headers):
        auth_header: str = headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username = payload.get("sub")
            role = payload.get("role")
            user = self.fake_users_db.get(username)
            if not username or not role or not user:
                return None
            if username != user['username'] or role != user['role']:
                return None
            return username
        except jwt.JWTError:
            return None
        
    #just in case
    def require_admin(self, current_user):
        if current_user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Admin rights required")
        return current_user
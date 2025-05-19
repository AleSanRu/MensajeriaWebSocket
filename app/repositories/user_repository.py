from app.utils.database import get_database
from app.models.user import UserCreate, User
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self):
        self.db = get_database()
        self.users = self.db["users"]
    
    def create_user(self, user: UserCreate):
        hashed_password = pwd_context.hash(user.password)
        user_data = {
            "username": user.username,
            "email": user.email,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow()
        }
        result = self.users.insert_one(user_data)
        return str(result.inserted_id)
    
    def get_user_by_username(self, username: str):
        return self.users.find_one({"username": username})
    
    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
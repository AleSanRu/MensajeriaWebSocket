from app.repositories.user_repository import UserRepository
from app.models.user import UserCreate, User

class UserService:
    def __init__(self):
        self.repository = UserRepository()
    
    def create_user(self, user: UserCreate):
        if self.repository.get_user_by_username(user.username):
            return None  # Usuario ya existe
        return self.repository.create_user(user)
    
    def authenticate_user(self, username: str, password: str):
        user = self.repository.get_user_by_username(username)
        if not user:
            return None
        if not self.repository.verify_password(password, user["hashed_password"]):
            return None
        return user
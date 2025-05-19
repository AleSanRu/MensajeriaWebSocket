from app.repositories.message_repository import MessageRepository
from app.models.message import MessageCreate, Message

class MessageService:
    def __init__(self):
        self.repository = MessageRepository()
    
    def send_message(self, message: MessageCreate):
        return self.repository.create_message(message)
    
    def get_conversation(self, user1: str, user2: str):
        return self.repository.get_messages_between_users(user1, user2)
    
    def get_user_messages(self, username: str):
        return self.repository.get_user_messages(username)
from app.utils.database import get_database
from app.models.message import MessageCreate, Message
from datetime import datetime

class MessageRepository:
    def __init__(self):
        self.db = get_database()
        self.messages = self.db["messages"]
    
    def create_message(self, message: MessageCreate):
        message_data = {
            "content": message.content,
            "sender_username": message.sender_username,
            "receiver_username": message.receiver_username,
            "created_at": datetime.utcnow()
        }
        result = self.messages.insert_one(message_data)
        return str(result.inserted_id)
    
    def get_messages_between_users(self, user1: str, user2: str):
        query = {
            "$or": [
                {"sender_username": user1, "receiver_username": user2},
                {"sender_username": user2, "receiver_username": user1}
            ]
        }
        return list(self.messages.find(query).sort("created_at", 1))
    
    def get_user_messages(self, username: str):
        query = {
            "$or": [
                {"sender_username": username},
                {"receiver_username": username}
            ]
        }
        return list(self.messages.find(query).sort("created_at", 1))
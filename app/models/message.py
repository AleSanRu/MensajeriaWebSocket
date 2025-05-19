from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class MessageBase(BaseModel):
    content: str
    sender_username: str
    receiver_username: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
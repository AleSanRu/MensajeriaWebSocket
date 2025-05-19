from fastapi import WebSocket, WebSocketDisconnect
from app.services.message_service import MessageService
from app.services.user_service import UserService
from app.models.message import MessageCreate
import json
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.message_service = MessageService()
        self.user_service = UserService()

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, sender: str, receiver: str):
        message_data = {
            "content": message,
            "sender": sender,
            "receiver": receiver,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Guardar el mensaje en la base de datos
        self.message_service.send_message(MessageCreate(
            content=message,
            sender_username=sender,
            receiver_username=receiver
        ))
        
        # Enviar el mensaje a los usuarios involucrados si están conectados
        for username, websocket in self.active_connections.items():
            if username == sender or username == receiver:
                await websocket.send_text(json.dumps(message_data))

manager = ConnectionManager()
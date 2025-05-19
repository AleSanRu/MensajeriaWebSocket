from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import UserCreate, User
from app.models.message import MessageCreate, Message
from app.services.user_service import UserService
from app.services.message_service import MessageService
from datetime import datetime
from typing import List
import json

router = APIRouter()
user_service = UserService()
message_service = MessageService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/users/", response_model=str)
async def create_user(user: UserCreate):
    user_id = user_service.create_user(user)
    if not user_id:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_id

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user["username"], "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = user_service.repository.get_user_by_username(token)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/messages/", response_model=str)
async def send_message(message: MessageCreate, token: str = Depends(oauth2_scheme)):
    if token != message.sender_username:
        raise HTTPException(status_code=403, detail="Cannot send message as another user")
    return message_service.send_message(message)

@router.get("/messages/{username}", response_model=List[Message])
async def get_messages(username: str, token: str = Depends(oauth2_scheme)):
    if token != username:
        raise HTTPException(status_code=403, detail="Cannot access another user's messages")
    return message_service.get_user_messages(username)

@router.get("/messages/{user1}/{user2}", response_model=List[Message])
async def get_conversation(user1: str, user2: str, token: str = Depends(oauth2_scheme)):
    if token != user1 and token != user2:
        raise HTTPException(status_code=403, detail="Cannot access this conversation")
    return message_service.get_conversation(user1, user2)
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from main import Event


router = APIRouter()

users = []

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@router.post('/register')
async def register_user(username: str, email: str, password: str):
    new_user = User(username, email, password)
    users.append(new_user)
    return {"message": "User registered successfully"}

#@router.post('/login')
#async def login_user(username: str, password: str):
    #for user in users:
        #if user.username == username and user.password == password:
            #return {"message": "User logged in successfully"}
    #return {"message": "Login failed"}

@router.get('/users')
async def get_users():
    user_data = [{"username": user.username, "email": user.email} for user in users]
    return user_data
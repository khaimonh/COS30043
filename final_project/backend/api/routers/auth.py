from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status
from dotenv import load_dotenv

import os
from datetime import datetime, timedelta, timezone
from jose import jwt

from deps import db_dependency, bcrypt_context

from models import User
load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

def authenticate_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(user: User, expires_delta: timedelta = ACCESS_TOKEN_EXPIRE_MINUTES):
    payload = {
        "sub": str(user.user_id),
        "name": str(user.first_name),
        "role": user.role.role_name,
    }
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({'exp': expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
from sqlalchemy.orm import Session
from sqlalchemy import select, UUID
from api.database import SessionLocal
import bcrypt
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import uuid

from api.models import User

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

def hash_password(plain: str) -> str:
      return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")
oauth2_pwform = Annotated[OAuth2PasswordRequestForm, Depends()]

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: UUID = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

    user = db.scalar(select(User).where(User.user_id == user_id))

    if user is None:
        raise credentials_exception

    return user
user_dependency = Annotated[User, Depends(get_current_user)]


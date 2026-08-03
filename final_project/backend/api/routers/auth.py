from sqlalchemy import select
from fastapi import APIRouter, HTTPException, status
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr

import os
from datetime import datetime, timedelta, timezone
from jose import jwt

from api.deps import db_dependency, hash_password, verify_password, user_dependency, oauth2_pwform

from api.models import User, Role
load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str
    
def authenticate_user(email: str, password: str, db) -> User | None:
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(user: User, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    payload = {
        "sub": str(user.user_id),
        "name": str(user.first_name),
        "role": user.role.role_name,
    }
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({'exp': expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def _create_user(create_user_request: UserCreateRequest, role_name: str, db):
    existing_user = db.scalar(select(User).where(User.email == create_user_request.email))

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user_role = db.scalar(select(Role).where(Role.role_name == role_name))
    if not user_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{role_name} role not found")
    create_user_model = User(
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        email=create_user_request.email,
        password_hash=hash_password(create_user_request.password),
        role_id=user_role.role_id
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: UserCreateRequest, db: db_dependency):
    _create_user(create_user_request, "User", db)


@router.post('/admin_create', status_code=status.HTTP_201_CREATED)
async def create_admin(create_user_request: UserCreateRequest, db: db_dependency):
    _create_user(create_user_request, "Admin", db)


@router.post('/token', response_model=Token)
async def login_for_access_token(login_request: oauth2_pwform, db: db_dependency):
    user = authenticate_user(login_request.username, login_request.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user, timedelta(hours=10))
    
    return {"access_token": token, "token_type": "bearer"}


@router.get('/me')
async def get_current_user_info(
    current_user: user_dependency,
):
    return {
        "user_id": str(current_user.user_id),
        "email": current_user.email,
        "full_name": current_user.first_name + ' ' + current_user.last_name,
        "role": current_user.role.role_name,
    }

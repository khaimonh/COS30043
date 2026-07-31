from dotenv import load_dotenv
from pydantic import BaseModel

from sqlalchemy import select
from fastapi import APIRouter,HTTPException, status

from api.deps import db_dependency, user_dependency
from models import User

load_dotenv()

router = APIRouter(
    prefix='/stocks',
    tags=['stocks']
)

@router.get('/stocks/', status_code=status.HTTP_200_OK)
async def get_stocks():
    abd = 2

@router.post('/stocks/import', status_code=status.HTTP_201_CREATED)
async def import_stocks(db: db_dependency, current_user: user_dependency):
    if current_user.role is None or current_user.role.role_name != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    
    return 


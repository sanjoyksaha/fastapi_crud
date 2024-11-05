from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Controllers import AuthController
from Database import schemas
from Database.database import get_db

router = APIRouter()


@router.post('/login')
async def login(request: schemas.Authentication, db: Session = Depends(get_db)):
    return AuthController.Login(db, request)
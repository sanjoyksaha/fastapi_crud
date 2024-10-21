from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Controllers import UserController
from Database import schemas
from Database.database import get_db

# from Controllers.UserController import getUsers

router = APIRouter()


@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return UserController.getUsers(db)


@router.post("/users")
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return UserController.insertUser(request, db)


@router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserController.getUser(user_id, db)


@router.put('/users/{user_id}')
async def update_user(request: schemas.User, user_id: int, db: Session = Depends(get_db)):
    return UserController.updateUser(request, user_id, db)


@router.delete('/users/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UserController.deleteUser(user_id, db)

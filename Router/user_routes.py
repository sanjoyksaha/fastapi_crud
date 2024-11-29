from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from Controllers import UserController
from Database import schemas
from Database.database import get_db

# from Controllers.UserController import getUsers

router = APIRouter()


@router.get("/users")
async def get_users(request: Request, db: Session = Depends(get_db)):
    return UserController.getUsers(request, db)


@router.post("/users")
async def create_user(request: Request, payload:schemas.User, db: Session = Depends(get_db)):
    return UserController.insertUser(request, payload, db)


@router.get("/users/{user_id}")
async def get_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    return UserController.getUser(request, user_id, db)


@router.put('/users/{user_id}')
async def update_user(request: Request, payload: schemas.User, user_id: int, db: Session = Depends(get_db)):
    return UserController.updateUser(request, payload, user_id, db)


@router.delete('/users/{user_id}')
async def delete_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    return UserController.deleteUser(request, user_id, db)


@router.get('/authuser')
async def get_user(request: Request, db: Session = Depends(get_db)):
    return UserController.AuthUser(request, db)

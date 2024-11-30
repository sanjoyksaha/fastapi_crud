from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from Controllers import DashboardController
from Database.database import get_db

router = APIRouter()


@router.get('/dashboard')
async def dashboard(request: Request, db: Session = Depends(get_db)):
    return DashboardController.Dashboard(request, db)
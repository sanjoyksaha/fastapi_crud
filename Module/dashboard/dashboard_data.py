import json

from sqlalchemy.orm import Session, joinedload
from Database import models, schemas
from sqlalchemy import select, desc
from sqlalchemy import or_


def AdminDashboardData(db: Session):
    total_user = db.query(models.User).count()
    total_completed = db.query(models.Jobs).filter(models.Jobs.status == 1).count()
    total_pending = db.query(models.Jobs).filter(models.Jobs.status == 0).count()

    data = {
        'total_user': total_user,
        'total_completed': total_completed,
        'total_pending': total_pending
    }

    return data


def UserDashboardData(db: Session, user_id: int):
    total_user = db.query(models.User).count()
    total_completed = db.query(models.Jobs).filter(models.Jobs.user_id == user_id and models.Jobs.status == 1).count()
    total_pending = db.query(models.Jobs).filter(models.Jobs.user_id == user_id and models.Jobs.status == 0).count()

    data = {
        'total_user': total_user,
        'total_completed': total_completed,
        'total_pending': total_pending
    }

    return data
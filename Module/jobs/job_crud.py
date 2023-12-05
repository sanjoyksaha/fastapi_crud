from sqlalchemy.orm import Session
from Database import models, schemas
from sqlalchemy import select
from sqlalchemy import or_


def AllJob(db: Session):
    return db.query(models.User).all()


def InsertJob(db: Session, user_id: int):
    get_user = db.query(models.User).filter(models.User.id == user_id).first()
    get_job = db.query(models.Jobs).order_by(models.Jobs.id).first()

    # user = models.Jobs(unq_id=request.unq_id, position=request.position, status=request.status)
    # db.add(user)
    # db.commit()
    # db.refresh(user)
    # # print("user", user.id)
    # return user


def GetUser(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()




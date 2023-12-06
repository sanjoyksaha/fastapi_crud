from sqlalchemy.orm import Session
from Database import models, schemas
from sqlalchemy import or_


def AllUser(db: Session):
    return db.query(models.User).all()


def InsertUser(db: Session, request: schemas.User):
    user = models.User(name=request.name, unq_id=request.unq_id, position_x=request.position_x, position_y=request.position_y, status=request.status)
    db.add(user)
    db.commit()
    db.refresh(user)
    # print("user", user.id)
    return user


def GetUser(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def GetUserByNameAndUnqID(db: Session, name: str, unq_id: int):
    return db.query(models.User).filter(or_(models.User.name == name, models.User.unq_id == unq_id)).first()


def GetUserByUnqID(db: Session, unq_id: int):
    return db.query(models.User).filter(models.User.unq_id == unq_id).first()


def UpdateUser(db: Session, request: schemas.User, user_id: int):
    data = {
        models.User.name: request.name,
        models.User.unq_id: request.unq_id,
        models.User.position_x: request.position_x,
        models.User.position_y: request.position_y,
        models.User.status: request.status,
    }
    update = db.query(models.User).filter(models.User.id == user_id).update(data, synchronize_session=False)
    db.commit()
    return update


def DeleteUser(db: Session, user_id: int):
    delete = db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    db.commit()

    return delete

from sqlalchemy.orm import Session
from Database import models, schemas
from sqlalchemy import or_, desc


def AllUser(db: Session, authUser: dict):
    if authUser['is_superadmin'] == 1:
        return db.query(models.User).all()
    else:
        return db.query(models.User).filter(models.User.id == authUser['id']).all()


def InsertUser(db: Session, payload: schemas.User):
    user = models.User(name=payload.name, unq_id=payload.unq_id, position_x=payload.position_x, position_y=payload.position_y, status=payload.status)
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

def GetLastUser(db: Session):
    return db.query(models.User).order_by(desc(models.User.id)).first()



def UpdateUser(db: Session, payload: schemas.User, user_id: int):
    data = {
        models.User.name: payload.name,
        # models.User.unq_id: payload.unq_id,
        models.User.position_x: payload.position_x,
        models.User.position_y: payload.position_y,
        models.User.status: payload.status,
    }
    update = db.query(models.User).filter(models.User.id == user_id).update(data, synchronize_session=False)
    db.commit()
    return update


def DeleteUser(db: Session, user_id: int):
    delete = db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    db.commit()

    return delete

from fastapi import Depends
from sqlalchemy.orm import Session

from Database import schemas
from Database.database import get_db
from Module.user import user_crud


def getUsers(db: Session):
    users = user_crud.AllUser(db=db)
    return {"status": 1, "msg": "User Lists.", "data": users}

def insertUser(request, db: Session):
    check = user_crud.GetUserByNameAndUnqID(db, name=request.name, unq_id=request.unq_id)
    if check:
        return {"status": 0, "msg": "Already exists."}
    insert = user_crud.InsertUser(db, request)
    if insert.id > 0:
        return {"status": 1, "msg": "Successfully Inserted."}

def getUser(user_id: int, db: Session):
    data = user_crud.GetUser(db=db, user_id=user_id)
    return {"status": 1, "msg": "User details.", "data": data}

def updateUser(request, user_id: int, db: Session):
    check = user_crud.GetUser(db=db, user_id=user_id)
    if check is None:
        return {"status": 0, "msg": "Invalid UserID."}
    update = user_crud.UpdateUser(db=db, request=request, user_id=user_id)
    if update == 1:
        return {"status": 1, "msg": "Successfully Updated."}
    else:
        return {"status": 0, "msg": "Failed to update."}

def deleteUser(user_id: int, db: Session):
    check = user_crud.GetUser(db=db, user_id=user_id)
    if check is None:
        return {"status": 0, "msg": "Invalid UserID."}
    delete = user_crud.DeleteUser(db=db, user_id=user_id)
    if delete == 1:
        return {"status": 1, "msg": "Successfully Deleted."}
    else:
        return {"status": 0, "msg": "Failed to delete this data."}
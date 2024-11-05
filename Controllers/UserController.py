from http.client import HTTPException

from fastapi import Depends
from sqlalchemy.orm import Session

from Database import schemas
from Database.database import get_db
from Helpers import Helper
from Module.user import user_crud


def getUsers(request, db: Session):
    auth = Helper.AuthenticateByToken(request, db)

    if len(auth) == 0:
        return {"status": 0, "msg": "Unauthorized"}

    users = user_crud.AllUser(db=db)
    return {"status": 1, "msg": "User Lists.", "data": users}

def insertUser(request, payload, db: Session):
    auth = Helper.AuthenticateByToken(request, db)
    if len(auth) == 0:
        return {"status": 0, "msg": "Unauthorized"}

    if auth['is_superadmin'] != 1:
        return {"status": 0, "msg": "You are not an administrator."}
    check = user_crud.GetUserByNameAndUnqID(db, name=payload.name, unq_id=payload.unq_id)
    if check:
        return {"status": 0, "msg": "Already exists."}
    insert = user_crud.InsertUser(db, payload)
    if insert.id > 0:
        return {"status": 1, "msg": "Successfully Inserted."}

def getUser(request, user_id: int, db: Session):
    auth = Helper.AuthenticateByToken(request, db)
    if len(auth) == 0:
        return {"status": 0, "msg": "Unauthorized"}

    data = user_crud.GetUser(db=db, user_id=user_id)
    return {"status": 1, "msg": "User details.", "data": data}

def updateUser(request, payload, user_id: int, db: Session):
    auth = Helper.AuthenticateByToken(request, db)
    if len(auth) == 0:
        return {"status": 0, "msg": "Unauthorized"}

    check = user_crud.GetUser(db=db, user_id=user_id)
    if check is None:
        return {"status": 0, "msg": "Invalid UserID."}

    if auth['is_superadmin'] != 1 and auth['id'] != check['id']:
        return {"status": 0, "msg": "Invalid request."}

    update = user_crud.UpdateUser(db=db, payload=payload, user_id=user_id)
    if update == 1:
        return {"status": 1, "msg": "Successfully Updated."}
    else:
        return {"status": 0, "msg": "Failed to update."}

def deleteUser(request, user_id: int, db: Session):
    auth = Helper.AuthenticateByToken(request, db)
    if len(auth) == 0:
        return {"status": 0, "msg": "Unauthorized"}

    if auth['is_superadmin'] != 1:
        return {"status": 0, "msg": "You are not an administrator."}

    check = user_crud.GetUser(db=db, user_id=user_id)
    if check is None:
        return {"status": 0, "msg": "Invalid UserID."}
    delete = user_crud.DeleteUser(db=db, user_id=user_id)
    if delete == 1:
        return {"status": 1, "msg": "Successfully Deleted."}
    else:
        return {"status": 0, "msg": "Failed to delete this data."}
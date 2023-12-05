from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from Database import models, schemas
from Database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from Module.user import user_crud

app = FastAPI()

models.Base.metadata.create_all(engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# def getUser(unq_id: float = None, user_id: int = None, position: float = None):
#     return {"status": 1, "data": {"unq_id": unq_id, "user_id": user_id, "position": position}}
@app.get("/users")
def Users(db: Session = Depends(get_db)):
    return {"status": 1, "msg": "User Lists.", "data": user_crud.AllUser(db=db)}


@app.post("/users")
def CreateUser(request: schemas.User, db: Session = Depends(get_db)):
    check = user_crud.GetUserByNameAndUnqID(db, name=request.name, unq_id=request.unq_id)
    if check:
        return {"status": 0, "msg": "Already exists."}
    insert = user_crud.InsertUser(db, request)
    if insert.id > 0:
        return {"status": 1, "msg": "Successfully Inserted."}


@app.get("/users/{user_id}")
def GetUser(user_id: int, db: Session = Depends(get_db)):
    data = user_crud.GetUser(db=db, user_id=user_id)
    return {"status": 1, "msg": "User details.", "data": data}


@app.put('/users/{user_id}')
def UpdateUser(request: schemas.User, user_id: int, db: Session = Depends(get_db)):
    check = user_crud.GetUser(db=db, user_id=user_id)
    if check is None:
        return {"status": 0, "msg": "Invalid UserID."}
    update = user_crud.UpdateUser(db=db, request=request, user_id=user_id)
    if update == 1:
        return {"status": 1, "msg": "Successfully Updated."}
    else:
        return {"status": 0, "msg": "Failed to delete this data."}


@app.delete('/users/{user_id}')
def DeleteUser(user_id: int, db: Session = Depends(get_db)):
    check = user_crud.GetUser(db=db, user_id=user_id)
    if check is None:
        return {"status": 0, "msg": "Invalid UserID."}
    delete = user_crud.DeleteUser(db=db, user_id=user_id)
    if delete == 1:
        return {"status": 1, "msg": "Successfully Deleted."}
    else:
        return {"status": 0, "msg": "Failed to delete this data."}


@app.post('/addjob')
def AddJob(user_id: int, db: Session= Depends(get_db)):
    pass


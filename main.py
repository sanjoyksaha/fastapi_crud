from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from Database import models, schemas
from Database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import and_
from Module.user import user_crud
from Module.jobs import job_crud

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
        return {"status": 0, "msg": "Failed to update."}


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


@app.post('/jobs')
def AddJob(request: schemas.Jobs, db: Session = Depends(get_db)):
    """
    First check user has any pending job
    """
    get_job = db.query(models.Jobs).where(and_(models.Jobs.user_id == request.user_id, models.Jobs.status == 0)).first()
    if get_job:
        return {"status": 0, "msg": "User has already pending job. Please wait.."}

    insert = job_crud.InsertJob(db, request)
    if insert.id > 0:
        return {"status": 1, "msg": "Success."}
    return {"status": 0, "msg": insert}


@app.get('/jobs')
def AllJobs(is_pending: int = None, page: int = None, db: Session = Depends(get_db)):
    data = ""
    page_size = 2  # Number of users per page
    if page is not None:
        page = page
    else:
        page = 1

    # Calculate the offset based on the page number and page size
    offset = (page - 1) * page_size
    if is_pending is None:
        data = job_crud.AllJob(db=db, offset=offset, page_size=page_size)
    elif is_pending == 1:
        data = job_crud.AllPendingJobs(db=db)
    elif is_pending == 0:
        data = job_crud.AllFinishedJobs(db=db)
    return {"status": 1, "msg": "Job Lists.", "data": data}


@app.put('/jobs/{job_id}')
def UpdateJob(job_id: int, db: Session = Depends(get_db)):
    update = job_crud.UpdateJob(db=db, job_id=job_id)
    if update == 1:
        return {"status": 1, "msg": "Job finished."}
    else:
        return {"status": 0, "msg": "Failed to finish the job."}

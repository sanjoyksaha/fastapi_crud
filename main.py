from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from Database import models, schemas
from Database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import and_
from Module.user import user_crud
from Module.jobs import job_crud
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import os

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
    page_size = 10 # Number of users per page
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
def UpdateJob(request: schemas.JobStatus, job_id: int, db: Session = Depends(get_db)):
    update = job_crud.UpdateJob(db=db, request=request, job_id=job_id)
    if update == 1:
        if request.status == 1:
            get_job = job_crud.GetJob(db=db, job_id=job_id)
            return {"status": 1, "msg": "Successfully Updated.", "data": get_job}
        return {"status": 1, "msg": "Job finished."}
    else:
        return {"status": 0, "msg": "Failed to finish the job."}


@app.delete('/jobs/{job_id}')
def DeleteUser(job_id: int, db: Session = Depends(get_db)):
    # check = job_crud.GetUser(db=db, user_id=user_id)
    # if check is None:
    #     return {"status": 0, "msg": "Invalid UserID."}
    delete = job_crud.DeleteJob(db=db, job_id=job_id)
    if delete == 1:
        return {"status": 1, "msg": "Successfully Deleted."}
    else:
        return {"status": 0, "msg": "Failed to delete this data."}


@app.get('/map')
def ReadFile():
    pgm_file = os.getcwd() + "/new.pgm"
    # image = Image.open(pgm_file)
    # # Rotate the image by 90 degrees (you can specify a different angle)
    # rotated_image = ImageOps.flip(image)
    #
    # rotated_image.save('new.pgm')
    # rotated_image.show()
    # exit()

    with open(pgm_file, 'rb') as f:  # Open the file in text mode for P2 format
        # Skip comments and metadata lines
        magic_number = f.readline().decode('utf-8').strip()
        if magic_number not in ['P2', 'P5']:
            raise ValueError("Invalid PGM format")

        # Skip comments and metadata lines
        while True:
            line = f.readline().decode('utf-8').strip()
            if not line.startswith('#'):
                break

        # Read PGM header
        width, height = map(int, line.split())
        print(width, height)
        max_val = int(f.readline())
        # print("max", f.read())

        # Read pixel values
        data = f.read()
        # print(data)
        #
        coordinates = []
        # coordinates = []
        X = []
        Y = []
        for w in range(width):
            for h in range(height):
                pixel_value = int(data[h * width + w])
                # # You may want to adjust the condition based on your specific requirements
                if pixel_value < 205:
                    # X.append(x)
                    # Y.append(y)
                    # coordinates.append((x, y))
                    coordinates.append({
                        'x': w,
                        'y': h
                    })

    return {"status": 1, "x": X, 'data': coordinates}


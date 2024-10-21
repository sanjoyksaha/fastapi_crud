from operator import and_

from sqlalchemy.orm import Session

from Database import models
from Module.jobs import job_crud


def getJobs(db: Session, is_pending: int = None, page: int = None):
    data = ""
    page_size = 10  # Number of users per page
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


def createJob(db: Session, request):
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


def updateJob(db: Session, request, job_id):
    update = job_crud.UpdateJob(db=db, request=request, job_id=job_id)
    if update == 1:
        if request.status == 1:
            get_job = job_crud.GetJob(db=db, job_id=job_id)
            return {"status": 1, "msg": "Successfully Updated.", "data": get_job}
        return {"status": 1, "msg": "Job finished."}
    else:
        return {"status": 0, "msg": "Failed to finish the job."}


def deleteJob(db: Session, job_id):
    # check = job_crud.GetUser(db=db, user_id=user_id)
    # if check is None:
    #     return {"status": 0, "msg": "Invalid UserID."}
    delete = job_crud.DeleteJob(db=db, job_id=job_id)
    if delete == 1:
        return {"status": 1, "msg": "Successfully Deleted."}
    else:
        return {"status": 0, "msg": "Failed to delete this data."}


def updateDoorStatus(db: Session, request, job_id):
    update = job_crud.UpdateDoorStatus(db=db, request=request, job_id=job_id)
    if update == 1:
        return {"status": 1, "msg": "Successfully Door Status Updated."}
    else:
        return {"status": 0, "msg": "Failed to update door status."}
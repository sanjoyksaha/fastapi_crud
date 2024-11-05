from operator import and_

from sqlalchemy.orm import Session

from Database import models
from Helpers import Helper
from Module.jobs import job_crud


def getJobs(request, db: Session, is_pending: int = None, page: int = None):
    auth = Helper.AuthenticateByToken(request, db)

    if len(auth) == 0:
        return {"status": 0, "msg": "Unauthorized"}

    filters = {}
    if auth['is_superadmin'] != 1:
        filters['user_id'] = auth['id']

    data = ""
    page_size = 10  # Number of users per page
    if page is not None:
        page = page
    else:
        page = 1

    # Calculate the offset based on the page number and page size
    offset = (page - 1) * page_size
    if is_pending is None:
        data = job_crud.AllJob(db=db, filters=filters, offset=offset, page_size=page_size)
    elif is_pending == 1:
        data = job_crud.AllPendingJobs(db=db, filters=filters)
    elif is_pending == 0:
        data = job_crud.AllFinishedJobs(db=db, filters=filters)
    return {"status": 1, "msg": "Job Lists.", "data": data}


def createJob(request, db: Session, payload):
    auth = Helper.AuthenticateByToken(request, db)

    if len(auth) == 0:
        return {"status": 0, "msg": "Unauthorized"}

    """
    First check user has any pending job
    """
    get_job = db.query(models.Jobs).where(and_(models.Jobs.user_id == payload.user_id, models.Jobs.status == 0)).first()
    if get_job:
        return {"status": 0, "msg": "User has already pending job. Please wait.."}

    insert = job_crud.InsertJob(db, payload)
    if insert.id > 0:
        return {"status": 1, "msg": "Success."}
    return {"status": 0, "msg": insert}


def getJobDetails(request, db: Session, job_id):
    auth = Helper.AuthenticateByToken(request, db)

    if len(auth) == 0:
        return {"status": 0, "msg": "Unauthorized"}

    data = job_crud.GetJob(db, job_id)
    if data is not None:
        return {"status": 1, "msg": "Job Details.", "data": data}
    else:
        return {"status": 0, "msg": "No Data Found."}


def updateJob(request, db: Session, payload, job_id):
    auth = Helper.AuthenticateByToken(request, db)

    if len(auth) == 0:
        return {"status": 0, "msg": "Unauthorized"}

    update = job_crud.UpdateJob(db=db, payload=payload, job_id=job_id)
    if update == 1:
        get_job = job_crud.GetJob(db=db, job_id=job_id)
        msg = 'Successfully updated.'
        if payload.status == 1:
            msg = 'Goal Reached & Successfully Job Status Updated..'
        elif payload.status == 12:
            msg = 'Job Is Finished.'
        return {"status": 1, "msg": f'{msg}', "data": get_job}
    else:
        return {"status": 0, "msg": "Failed to finish the job."}


def deleteJob(request, db: Session, job_id):
    auth = Helper.AuthenticateByToken(request, db)

    if len(auth) == 0:
        return {"status": 0, "msg": "Unauthorized"}

    # check = job_crud.GetUser(db=db, user_id=user_id)
    # if check is None:
    #     return {"status": 0, "msg": "Invalid UserID."}
    delete = job_crud.DeleteJob(db=db, job_id=job_id)
    if delete == 1:
        return {"status": 1, "msg": "Successfully Deleted."}
    else:
        return {"status": 0, "msg": "Failed to delete this data."}


def updateDoorStatus(request, db: Session, payload, job_id):
    update = job_crud.UpdateDoorStatus(db=db, payload=payload, job_id=job_id)
    if update == 1:
        return {"status": 1, "msg": "Successfully Door Status Updated."}
    else:
        return {"status": 0, "msg": "Failed to update door status."}
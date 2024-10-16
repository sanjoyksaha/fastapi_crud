from sqlalchemy.orm import Session, joinedload
from Database import models, schemas
from sqlalchemy import select, desc
from sqlalchemy import or_


def AllJob(db: Session, offset, page_size: int = 10):
    # return db.query(models.Jobs).join(models.User).all()
    return db.query(models.Jobs).options(joinedload(models.Jobs.creator)).offset(offset).limit(page_size).all()


def AllPendingJobs(db: Session):
    # return db.query(models.Jobs).where(models.Jobs.status == 0).all()
    return db.query(models.Jobs).where(models.Jobs.status != 1).all()


def AllFinishedJobs(db: Session):
    return db.query(models.Jobs).where(models.Jobs.status == 1).all()


def InsertJob(db: Session, request: schemas.Jobs):
    get_user = db.query(models.User).filter(models.User.id == request.user_id).first()

    get_job = db.query(models.Jobs).order_by(desc(models.Jobs.id)).first()

    if get_job is None:
        job_id = 1000001
    else:
        job_id = get_job.unq_id + 1

    job = models.Jobs(unq_id=job_id, user_id=request.user_id, position_x=get_user.position_x,
                      position_y=get_user.position_y, status=0)
    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def UpdateJob(db: Session, request: schemas.JobStatus, job_id: int):
    data = {
        models.Jobs.status: request.status,
    }
    update = db.query(models.Jobs).filter(models.Jobs.id == job_id).update(data, synchronize_session=False)
    db.commit()
    return update


def DeleteJob(db: Session, job_id: int):
    delete = db.query(models.Jobs).filter(models.Jobs.id == job_id).delete(synchronize_session=False)
    db.commit()

    return delete

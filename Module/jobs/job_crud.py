import json

from sqlalchemy.orm import Session, joinedload
from Database import models, schemas
from sqlalchemy import select, desc
from sqlalchemy import or_


def AllJob(db: Session, offset, page_size: int = 10):
    # return db.query(models.Jobs).join(models.User).all()
    # return db.query(models.Jobs.id).options(joinedload(models.Jobs.creator)).offset(offset).limit(page_size).all()
    # return db.query(models.Jobs).join(models.Jobs.creator).offset(offset).limit(page_size).all()

    results = (db.query(models.Jobs.id, models.Jobs.unq_id, models.Jobs.status, models.Jobs.door_open, models.Jobs.position_x, models.Jobs.position_y, models.User.name)
               .join(models.User, models.User.id == models.Jobs.user_id).offset(offset).limit(page_size).all())
    formatted_results = [{"id": row[0], "unq_id": row[1], "status": row[2], "door_open": row[3], "position_x": row[4], "position_y": row[5], "user_name": row[6]} for row
                         in results]

    return formatted_results

def AllPendingJobs(db: Session):
    # return db.query(models.Jobs).where(models.Jobs.status == 0).all()
    # return db.query(models.Jobs).where(models.Jobs.status != 12).where(models.Jobs.door_open != 2).all()
    results = (db.query(models.Jobs.id, models.Jobs.unq_id, models.Jobs.status, models.Jobs.door_open, models.Jobs.position_x, models.Jobs.position_y, models.User.name, models.Jobs.user_id)
               .join(models.User, models.User.id == models.Jobs.user_id)
               .where(models.Jobs.status != 12).where(models.Jobs.door_open != 2)
               .all())
    formatted_results = [{"id": row[0], "unq_id": row[1], "status": row[2], "door_open": row[3], "position_x": row[4], "position_y": row[5], "user_name": row[6], "user_id": row[7]} for row
                         in results]

    return formatted_results


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


def GetJob(db: Session, job_id: int):
    data = db.query(models.Jobs, models.User).join(models.User, models.User.id == models.Jobs.user_id).filter(models.Jobs.id == job_id).first()
    if data:
        return {
                'id': data.Jobs.id,
                'user_name': data.User.name,
                'unq_id': data.Jobs.unq_id,
                'status': data.Jobs.status,
                'door_open': data.Jobs.door_open,
                'position_x': data.Jobs.position_x,
                'position_y': data.Jobs.position_y,
            }
    else:
        return None



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

def UpdateDoorStatus(db: Session, request: schemas.DoorStatus, job_id: int):
    data = {
        models.Jobs.door_open: request.door_open,
    }
    update = db.query(models.Jobs).filter(models.Jobs.id == job_id).update(data, synchronize_session=False)
    db.commit()
    return update

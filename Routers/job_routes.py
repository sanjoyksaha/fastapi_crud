from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Controllers import UserController, JobController
from Database import schemas
from Database.database import get_db

router = APIRouter()


@router.get('/jobs')
async def get_jobs(is_pending: int = None, page: int = None, db: Session = Depends(get_db)):
    return JobController.getJobs(db, is_pending, page)


@router.post('/jobs')
async def create_job(request: schemas.Jobs, db: Session = Depends(get_db)):
    return JobController.createJob(db, request)



@router.put('/jobs/{job_id}')
def update_job(request: schemas.JobStatus, job_id: int, db: Session = Depends(get_db)):
    return JobController.updateJob(db, job_id, request)


@router.delete('/jobs/{job_id}')
def delete_job(job_id: int, db: Session = Depends(get_db)):
    return JobController.deleteJob(db, job_id)


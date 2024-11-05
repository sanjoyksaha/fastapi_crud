from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from Controllers import UserController, JobController
from Database import schemas
from Database.database import get_db

router = APIRouter()


@router.get('/jobs')
async def get_jobs(request: Request, is_pending: int = None, page: int = None, db: Session = Depends(get_db)):
    return JobController.getJobs(request, db, is_pending, page)


@router.post('/jobs')
async def create_job(request: Request, payload: schemas.Jobs, db: Session = Depends(get_db)):
    return JobController.createJob(request, db, payload)


@router.get('/jobs/{job_id}')
def job_details(request: Request, job_id: int, db: Session = Depends(get_db)):
    return JobController.getJobDetails(request, db, job_id)


@router.put('/jobs/{job_id}')
def update_job(request: Request, payload: schemas.JobStatus, job_id: int, db: Session = Depends(get_db)):
    return JobController.updateJob(request, db, payload, job_id)


@router.delete('/jobs/{job_id}')
def delete_job(request: Request, job_id: int, db: Session = Depends(get_db)):
    return JobController.deleteJob(request, db, job_id)


@router.put('/jobs/door_status/{job_id}')
def update_job(request: Request, payload: schemas.DoorStatus, job_id: int, db: Session = Depends(get_db)):
    return JobController.updateDoorStatus(request, db, payload, job_id)
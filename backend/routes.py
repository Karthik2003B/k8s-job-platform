from fastapi import APIRouter
from backend.job_service import (create_job,get_job_status,get_job_logs)
from backend.db_manager import DatabaseManager
db=DatabaseManager()
router = APIRouter()

@router.post("/jobs")
def submit_job(job_name:str,image:str,command:str,cpu:str,memory:str,namespace:str):
    return create_job(job_name,image,command,cpu,memory,namespace)

@router.get("/jobs/{job_name}")
def job_status(job_name: str, namespace: str):
    return get_job_status(job_name, namespace)


@router.get("/jobs/{job_name}/logs")
def job_logs(job_name: str, namespace: str):

    return get_job_logs(job_name, namespace)

@router.get("/jobs")
def get_all_jobs():
    return db.get_all_jobs()
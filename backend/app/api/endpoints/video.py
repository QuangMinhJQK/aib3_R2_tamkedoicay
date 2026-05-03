import uuid
import json
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from backend.app.services.video.pipeline import run_video_pipeline
from backend.app.services import job_service
from backend.app.services.appointment_service import get_last_summary
from backend.app.services.job_service import get_job, list_jobs

router = APIRouter()

# In-memory dictionary to store job statuses
jobs_state = {}

class VideoGenerateRequest(BaseModel):
    patient_id: int

@router.post("/generate")
def generate_video(req: VideoGenerateRequest, background_tasks: BackgroundTasks):
    # 1. Fetch medical record for context
    summary = get_last_summary(req.patient_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Medical record not found for patient")
    
    # Format the medical record as text for the LLM
    medical_record_text = json.dumps(summary, ensure_ascii=False, indent=2)
    
    # 2. Generate Job ID and initialize state
    job_id = str(uuid.uuid4())
    jobs_state[job_id] = {"status": "PENDING"}

    # Persist job to DB so it's tracked across restarts
    job_service.create_job(job_id, req.patient_id)

    # 3. Dispatch Background Task
    background_tasks.add_task(run_video_pipeline, req.patient_id, medical_record_text, job_id, jobs_state)
    
    return {"job_id": job_id, "status": "PENDING"}

@router.get("/{job_id}/status")
def get_video_status(job_id: str):
    # Prefer DB-backed job state if available
    db_job = get_job(job_id)
    if db_job:
        return db_job

    # Fallback to in-memory jobs_state for very recent jobs
    if job_id in jobs_state:
        return jobs_state[job_id]

    raise HTTPException(status_code=404, detail="Job ID not found")


@router.get("/", response_model=list)
def list_video_jobs():
    return list_jobs(50)

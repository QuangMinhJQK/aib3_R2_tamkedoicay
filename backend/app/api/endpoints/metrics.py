from fastapi import APIRouter, Query

from backend.app.schemas.common import APIResponse
from backend.app.services import metric_service

router = APIRouter(tags=["Health Metrics & Medications"])


@router.get("/api/v1/metrics/latest", response_model=APIResponse)
async def get_latest(patient_id: int = Query(1)):
    data = metric_service.get_latest_metrics(patient_id)
    return APIResponse(data=data)


@router.get("/api/v1/metrics/trend", response_model=APIResponse)
async def get_trend(
    patient_id: int = Query(1),
    type: str = Query("blood_glucose"),
    days: int = Query(7),
):
    data = metric_service.get_trend(patient_id, type, days)
    return APIResponse(data=data)


@router.get("/api/v1/medications/status", response_model=APIResponse)
async def get_medication_status(patient_id: int = Query(1)):
    data = metric_service.get_medication_status(patient_id)
    return APIResponse(data=data)

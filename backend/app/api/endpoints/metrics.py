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


@router.get("/api/v1/metrics/history", response_model=APIResponse)
async def get_history(
    patient_id: int = Query(1),
    days: int = Query(30),
    max_series: int = Query(4),
    max_points_per_series: int = Query(8),
):
    data = metric_service.get_clinical_history(
        patient_id=patient_id,
        days=days,
        max_series=max_series,
        max_points_per_series=max_points_per_series,
    )
    return APIResponse(data=data)


@router.get("/api/v1/medications/status", response_model=APIResponse)
async def get_medication_status(patient_id: int = Query(1)):
    data = metric_service.get_medication_status(patient_id)
    return APIResponse(data=data)

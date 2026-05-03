from pydantic import BaseModel
from typing import Optional


class MetricValue(BaseModel):
    value: float | str
    unit: str
    status: str
    updated_at: str


class LatestMetricsResponse(BaseModel):
    blood_glucose: Optional[MetricValue] = None
    blood_pressure: Optional[MetricValue] = None


class TrendPoint(BaseModel):
    date: str
    value: float


class MedicationStatusResponse(BaseModel):
    status: str  # "TAKEN" | "MISSED" | "PENDING"
    time: Optional[str] = None

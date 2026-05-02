from pydantic import BaseModel
from typing import List, Optional


class NextAppointmentResponse(BaseModel):
    id: int
    title: str
    location: Optional[str] = None
    date: str
    time: str
    status: str


class RescheduleRequest(BaseModel):
    action: str  # "reschedule" | "cancel"
    new_date: Optional[str] = None
    reason: Optional[str] = None


class LastSummaryResponse(BaseModel):
    date: str
    clinical_summary: str
    metrics: List[str] = []
    doctor_notes: Optional[str] = None
    warning: Optional[str] = None
    next_steps: Optional[str] = None
    next_appointment_date: Optional[str] = None

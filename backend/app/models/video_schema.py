from pydantic import BaseModel, Field
from typing import List, Optional

class HealthMetric(BaseModel):
    label: str
    value: str
    trend: str # 'up' | 'down' | 'stable'
    unit: Optional[str] = None

class DoctorAdvice(BaseModel):
    text: str
    audioDurationInFrames: int


class SectionNarration(BaseModel):
    section: str  # one of: report_status | health_metrics | progress | advice
    text: str
    audioDurationInFrames: int = 0

class MasterProps(BaseModel):
    patientName: str
    overallStatus: str
    metrics: List[HealthMetric]
    advices: List[DoctorAdvice]
    sectionNarrations: List[SectionNarration] = Field(default_factory=list)
    totalDurationInFrames: int

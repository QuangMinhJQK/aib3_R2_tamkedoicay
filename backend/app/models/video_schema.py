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


class SectionDurations(BaseModel):
    report_status: int = 90
    health_metrics: int = 120
    progress: int = 120
    advice: int = 120


class ClinicalMetricPoint(BaseModel):
    date: str
    value: float


class ClinicalMetricSeries(BaseModel):
    name: str
    unit: str = ""
    points: List[ClinicalMetricPoint] = Field(default_factory=list)
    totalPoints: int = 0

class MasterProps(BaseModel):
    patientName: str
    overallStatus: str
    metrics: List[HealthMetric]
    advices: List[DoctorAdvice]
    sectionNarrations: List[SectionNarration] = Field(default_factory=list)
    sectionDurationsInFrames: SectionDurations = Field(default_factory=SectionDurations)
    clinicalHistory: List[ClinicalMetricSeries] = Field(default_factory=list)
    totalDurationInFrames: int

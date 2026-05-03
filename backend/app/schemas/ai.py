from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    message: str
    attachments: List[str] = []


class ChatResponse(BaseModel):
    reply: str
    sources: List[str] = []


class SuggestionItem(BaseModel):
    text: str


class InsightResponse(BaseModel):
    insight: str


class VideoAdviceResponse(BaseModel):
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    title: str
    description: Optional[str] = None


class VideoUrlUpdateRequest(BaseModel):
    patient_id: int
    video_url: str

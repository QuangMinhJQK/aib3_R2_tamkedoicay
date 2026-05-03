from pydantic import BaseModel
from typing import Optional


class NotificationResponse(BaseModel):
    id: int
    type: Optional[str] = None
    title: str
    message: Optional[str] = None
    is_read: bool = False
    created_at: Optional[str] = None


class NotificationDetailResponse(NotificationResponse):
    ai_insight: Optional[str] = None

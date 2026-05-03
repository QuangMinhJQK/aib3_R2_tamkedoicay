from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    id: int
    name: str
    avatar_url: Optional[str] = None
    overall_health_status: Optional[str] = None


class RelativeResponse(BaseModel):
    id: int
    name: str
    relationship: Optional[str] = None
    phone: Optional[str] = None
    is_connected: bool = True
    allow_notifications: bool = True


class RelativeCreateRequest(BaseModel):
    name: str
    phone: str
    relationship: str


class NotificationToggleRequest(BaseModel):
    allow_notifications: bool

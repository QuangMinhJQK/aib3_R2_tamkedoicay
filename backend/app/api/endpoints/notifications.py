from fastapi import APIRouter, HTTPException, Query

from backend.app.schemas.common import APIResponse
from backend.app.services import notification_service

router = APIRouter(prefix="/api/v1/notifications", tags=["Notifications & Alerts"])


@router.get("", response_model=APIResponse)
async def get_all(patient_id: int = Query(1)):
    data = notification_service.get_notifications(patient_id)
    return APIResponse(data=data)


@router.get("/{notification_id}", response_model=APIResponse)
async def get_detail(notification_id: int):
    data = notification_service.get_notification_detail(notification_id)
    if not data:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông báo")
    return APIResponse(data=data)


@router.put("/{notification_id}/dismiss", response_model=APIResponse)
async def dismiss(notification_id: int):
    ok = notification_service.dismiss_notification(notification_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông báo")
    return APIResponse(message="Đã đánh dấu đã đọc")

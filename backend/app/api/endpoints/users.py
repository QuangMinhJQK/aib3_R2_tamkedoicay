from fastapi import APIRouter, HTTPException, Query

from backend.app.schemas.common import APIResponse
from backend.app.schemas.user import RelativeCreateRequest, NotificationToggleRequest
from backend.app.services import user_service

router = APIRouter(prefix="/api/v1/users", tags=["Users & Relatives"])


@router.get("/me", response_model=APIResponse)
async def get_current_user(patient_id: int = Query(1)):
    user = user_service.get_current_user(patient_id)
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy bệnh nhân")
    return APIResponse(data=user)


@router.get("/relatives", response_model=APIResponse)
async def get_relatives(patient_id: int = Query(1)):
    relatives = user_service.get_relatives(patient_id)
    return APIResponse(data=relatives)


@router.post("/relatives", response_model=APIResponse, status_code=201)
async def add_relative(body: RelativeCreateRequest, patient_id: int = Query(1)):
    new_id = user_service.add_relative(patient_id, body.name, body.phone, body.relationship)
    return APIResponse(data={"id": new_id}, message="Đã thêm người thân thành công")


@router.put("/relatives/{relative_id}/notifications", response_model=APIResponse)
async def toggle_notification(relative_id: int, body: NotificationToggleRequest):
    updated = user_service.toggle_notification(relative_id, body.allow_notifications)
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy người thân")
    return APIResponse(message="Cập nhật thành công")

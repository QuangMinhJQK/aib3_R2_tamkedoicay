from fastapi import APIRouter, HTTPException, Query

from backend.app.schemas.common import APIResponse
from backend.app.schemas.appointment import RescheduleRequest
from backend.app.services import appointment_service

router = APIRouter(prefix="/api/v1/appointments", tags=["Appointments"])


@router.get("/next", response_model=APIResponse)
async def get_next(patient_id: int = Query(1)):
    appointment = appointment_service.get_next_appointment(patient_id)
    if not appointment:
        return APIResponse(data=None, message="Không có lịch hẹn sắp tới")
    return APIResponse(data=appointment)


@router.put("/{appointment_id}/confirm", response_model=APIResponse)
async def confirm(appointment_id: int):
    ok = appointment_service.confirm_appointment(appointment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Không tìm thấy hoặc đã xác nhận")
    return APIResponse(message="Đã xác nhận lịch hẹn")


@router.put("/{appointment_id}/reschedule", response_model=APIResponse)
async def reschedule(appointment_id: int, body: RescheduleRequest):
    ok = appointment_service.reschedule_appointment(
        appointment_id, body.action, body.new_date, body.reason
    )
    if not ok:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn")
    return APIResponse(message="Đã cập nhật lịch hẹn")


@router.post("/{appointment_id}/relative-confirm", response_model=APIResponse)
async def relative_confirm(appointment_id: int):
    ok = appointment_service.relative_confirm(appointment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn")
    return APIResponse(message="Người thân đã xác nhận lịch hẹn")


@router.get("/last-summary", response_model=APIResponse)
async def get_last_summary(patient_id: int = Query(1)):
    summary = appointment_service.get_last_summary(patient_id)
    if not summary:
        return APIResponse(data=None, message="Chưa có kết quả khám")
    return APIResponse(data=summary)

from fastapi import APIRouter, HTTPException, Query, UploadFile, File

from backend.app.schemas.common import APIResponse
from backend.app.schemas.ai import ChatRequest
from backend.app.services import ai_service

router = APIRouter(prefix="/api/v1/ai", tags=["AI Advisor & Chatbot"])


@router.post("/chat", response_model=APIResponse)
async def chat(body: ChatRequest, patient_id: int = Query(1)):
    result = ai_service.chat(patient_id, body.message)
    return APIResponse(data=result)


@router.post("/upload-attachment", response_model=APIResponse)
async def upload_attachment(file: UploadFile = File(...), patient_id: int = Query(1)):
    # Stub: nhận file nhưng chưa xử lý AI phân tích
    return APIResponse(
        data={"filename": file.filename, "size": file.size},
        message="Đã nhận file. Tính năng phân tích AI đang phát triển.",
    )


@router.get("/suggestions", response_model=APIResponse)
async def get_suggestions():
    return APIResponse(data=ai_service.get_suggestions())


@router.get("/insights", response_model=APIResponse)
async def get_insights(patient_id: int = Query(1)):
    insight = ai_service.get_insights(patient_id)
    return APIResponse(data={"insight": insight})


@router.get("/video-advice", response_model=APIResponse)
async def get_video_advice(patient_id: int = Query(1)):
    data = ai_service.get_video_advice(patient_id)
    if not data:
        return APIResponse(data=None, message="Chưa có video tư vấn")
    return APIResponse(data=data)

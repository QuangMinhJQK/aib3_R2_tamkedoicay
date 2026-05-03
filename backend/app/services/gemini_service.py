import json
import logging
import os
from datetime import date

import google.generativeai as genai

logger = logging.getLogger(__name__)

_PROMPT_TEMPLATE = """Dựa vào các dữ liệu y tế thô sau, tạo tóm tắt KẾT QUẢ LÂM SÀNG cực kỳ NGẮN GỌN (dưới 15 chữ cho mỗi trường) để hiển thị trên giao diện điện thoại:

--- DỮ LIỆU THÔ ---
- Bệnh nhân: {patient_name}
- Chẩn đoán: {diagnosis}
- Ghi chú: {doctor_notes}
- Xét nghiệm: {metrics}
- Đơn thuốc: {prescriptions}

--- YÊU CẦU ---
Trả về duy nhất JSON object với các trường (KHÔNG markdown):
{{
  "clinical_summary": "Tối đa 5 chữ .",
  "metrics": ["Chỉ giữ tên chỉ số và kết quả đo, KHÔNG GIẢI THÍCH"],
  "doctor_notes": "Tối đa 25 chữ .",
  "warning": "Tối đa 15 chữ, bắt đầu bằng 'Lưu ý:' .",
  "next_steps": "Tối đa 15 chữ."
}}"""



def _init_client() -> genai.GenerativeModel | None:
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        "gemini-2.5-flash-lite",
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.4,
        ),
    )


def generate_clinical_summary(
    patient_name: str,
    diagnosis: str,
    doctor_notes: str,
    prescriptions: str,
    metrics: list[str],
    next_appointment_date: str | None,
) -> dict:
    model = _init_client()

    prompt = _PROMPT_TEMPLATE.format(
        patient_name=patient_name,
        diagnosis=diagnosis,
        doctor_notes=doctor_notes,
        metrics=", ".join(metrics) if metrics else "Không có dữ liệu",
        prescriptions=prescriptions or "Không có",
        next_appointment_date=next_appointment_date or "Chưa xác định",
    )

    try:
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        required_keys = {"clinical_summary", "metrics", "doctor_notes", "warning", "next_steps"}
        if not required_keys.issubset(result.keys()):
            logger.error("Gemini response missing required keys: %s", result.keys())
            raise ValueError("Gemini response missing required keys")
        return result
    except Exception as e:
        logger.error("Gemini API error: %s", e)
        raise e

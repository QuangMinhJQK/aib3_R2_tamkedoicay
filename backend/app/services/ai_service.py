from backend.app.core.database import get_db

# Các endpoint AI hiện tại trả về mock data.
# Khi tích hợp Gemini API, chỉ cần cập nhật file này.

PRESET_SUGGESTIONS = [
    "Cách dùng thuốc Metformin",
    "Chế độ ăn cho người tiểu đường",
    "Khi nào cần gọi bác sĩ?",
    "Tác dụng phụ của thuốc huyết áp",
    "Bài tập vận động nhẹ cho người lớn tuổi",
]


def chat(patient_id: int, message: str) -> dict:
    return {
        "reply": f"Cảm ơn bác đã hỏi về \"{message}\". Hiện tại hệ thống AI đang được nâng cấp, xin vui lòng thử lại sau.",
        "sources": [],
    }


def get_suggestions() -> list[str]:
    return PRESET_SUGGESTIONS


def get_insights(patient_id: int) -> str:
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT metric_value, unit, metric_name
            FROM clinical_metrics
            WHERE patient_id = ?
            ORDER BY recorded_at DESC LIMIT 1
            """,
            (patient_id,),
        ).fetchone()
    if row:
        return f"Chỉ số {row['metric_name']} gần nhất: {row['metric_value']} {row['unit']}. Tiếp tục duy trì chế độ ăn ít tinh bột."
    return "Chưa có đủ dữ liệu để phân tích."


def get_video_advice(patient_id: int) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT ai_video_url, ai_summary
            FROM medical_records
            WHERE patient_id = ? AND ai_video_url IS NOT NULL
            ORDER BY created_at DESC LIMIT 1
            """,
            (patient_id,),
        ).fetchone()
    if not row:
        return None
    return {
        "video_url": row["ai_video_url"],
        "thumbnail_url": None,
        "title": "Video giải thích tóm tắt",
        "description": row["ai_summary"],
    }


def update_latest_video_url(patient_id: int, video_url: str) -> bool:
    with get_db() as conn:
        record = conn.execute(
            """
            SELECT id
            FROM medical_records
            WHERE patient_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT 1
            """,
            (patient_id,),
        ).fetchone()
        if not record:
            return False

        cursor = conn.execute(
            """
            UPDATE medical_records
            SET ai_video_url = ?
            WHERE id = ?
            """,
            (video_url, record["id"]),
        )
        return cursor.rowcount > 0

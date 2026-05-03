import json
import logging

from backend.app.core.database import get_db
from backend.app.services.gemini_service import generate_clinical_summary

logger = logging.getLogger(__name__)


def get_next_appointment(patient_id: int) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT id, doctor_name, department, appointment_datetime, status
            FROM appointments
            WHERE patient_id = ? AND status IN ('Scheduled', 'Confirmed')
            ORDER BY appointment_datetime ASC
            LIMIT 1
            """,
            (patient_id,),
        ).fetchone()
    if not row:
        return None
    dt = row["appointment_datetime"]
    date_part = dt[:10] if dt else ""
    time_part = dt[11:16] if dt and len(dt) > 11 else ""
    return {
        "id": row["id"],
        "title": f"Tái khám {row['department']}",
        "location": None,
        "date": date_part,
        "time": time_part,
        "status": row["status"],
    }


def confirm_appointment(appointment_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE appointments SET status = 'Confirmed' WHERE id = ? AND status = 'Scheduled'",
            (appointment_id,),
        )
        return cursor.rowcount > 0


def reschedule_appointment(appointment_id: int, action: str, new_date: str | None, reason: str | None) -> bool:
    with get_db() as conn:
        if action == "cancel":
            cursor = conn.execute(
                "UPDATE appointments SET status = 'Cancelled' WHERE id = ?",
                (appointment_id,),
            )
        else:
            cursor = conn.execute(
                "UPDATE appointments SET appointment_datetime = ?, status = 'Scheduled' WHERE id = ?",
                (new_date, appointment_id),
            )
        return cursor.rowcount > 0


def relative_confirm(appointment_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE appointments SET status = 'Confirmed' WHERE id = ?",
            (appointment_id,),
        )
        return cursor.rowcount > 0


def _try_parse_cached_summary(ai_summary: str | None) -> dict | None:
    """Attempt to parse ai_summary as JSON. Returns dict if valid, None otherwise."""
    if not ai_summary:
        return None
    try:
        parsed = json.loads(ai_summary)
        required = {"clinical_summary", "metrics", "doctor_notes", "warning", "next_steps"}
        if required.issubset(parsed.keys()):
            return parsed
    except (json.JSONDecodeError, TypeError):
        pass
    return None


def _save_ai_summary(record_id: int, summary_json: str):
    """Cache the generated summary back to DB."""
    with get_db() as conn:
        conn.execute(
            "UPDATE medical_records SET ai_summary = ? WHERE id = ?",
            (summary_json, record_id),
        )


def get_last_summary(patient_id: int) -> dict | None:
    # 1. Query medical_records + patient info
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT mr.diagnosis, mr.doctor_notes, mr.prescriptions,
                   mr.next_appointment_date, mr.ai_summary, mr.created_at,
                   a.appointment_datetime,
                   p.full_name AS patient_full_name,
                   p.risk_group
            FROM medical_records mr
            JOIN appointments a ON mr.appointment_id = a.id
            JOIN patients p ON mr.patient_id = p.id
            WHERE mr.patient_id = ?
            ORDER BY mr.created_at DESC
            LIMIT 1
            """,
            (patient_id,),
        ).fetchone()
    if not row:
        return None
    visit_date = row["appointment_datetime"][:10] if row["appointment_datetime"] else ""

    # Map risk_group to a simple overall status string for downstream consumers.
    risk = (row["risk_group"] or "").lower()
    if risk == "high":
        overall_status = "Needs Attention"
    elif risk == "medium":
        overall_status = "Monitor"
    else:
        overall_status = "Good"

    return {
        "patientName": row["patient_full_name"],
        "overallStatus": overall_status,
        "date": visit_date,
        "clinical_summary": row["ai_summary"] or row["diagnosis"],
        "doctor_notes": row["doctor_notes"],
        "warning": None,
        "next_steps": f"Uống thuốc theo đơn: {row['prescriptions']}" if row["prescriptions"] else None,
        "next_appointment_date": row["next_appointment_date"],
    }

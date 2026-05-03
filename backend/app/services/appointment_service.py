from backend.app.core.database import get_db


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


def get_last_summary(patient_id: int) -> dict | None:
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

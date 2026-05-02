from backend.app.core.database import get_db


def get_current_user(patient_id: int) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, full_name, phone, email, risk_group FROM patients WHERE id = ?",
            (patient_id,),
        ).fetchone()
    if not row:
        return None
    return {
        "id": row["id"],
        "name": row["full_name"],
        "avatar_url": None,
        "overall_health_status": f"Nhóm nguy cơ: {row['risk_group']}",
    }


def get_relatives(patient_id: int) -> list[dict]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, full_name, relationship, phone, is_opt_in FROM caregivers WHERE patient_id = ?",
            (patient_id,),
        ).fetchall()
    return [
        {
            "id": r["id"],
            "name": r["full_name"],
            "relationship": r["relationship"],
            "phone": r["phone"],
            "is_connected": True,
            "allow_notifications": bool(r["is_opt_in"]),
        }
        for r in rows
    ]


def add_relative(patient_id: int, name: str, phone: str, relationship: str) -> int:
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO caregivers (patient_id, full_name, relationship, phone, is_opt_in) VALUES (?, ?, ?, ?, 1)",
            (patient_id, name, relationship, phone),
        )
        return cursor.lastrowid


def toggle_notification(relative_id: int, allow: bool) -> bool:
    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE caregivers SET is_opt_in = ? WHERE id = ?",
            (int(allow), relative_id),
        )
        return cursor.rowcount > 0

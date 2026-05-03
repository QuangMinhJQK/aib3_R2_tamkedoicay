from backend.app.core.database import get_db


def get_notifications(patient_id: int) -> list[dict]:
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT id, channel, message_level, content, sent_at, is_responded
            FROM communication_logs
            WHERE patient_id = ?
            ORDER BY sent_at DESC
            """,
            (patient_id,),
        ).fetchall()
    return [
        {
            "id": r["id"],
            "type": r["channel"],
            "title": f"Thông báo {r['message_level'].replace('_', ' ')}",
            "message": r["content"],
            "is_read": bool(r["is_responded"]),
            "created_at": r["sent_at"],
        }
        for r in rows
    ]


def get_notification_detail(notification_id: int) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT cl.id, cl.channel, cl.message_level, cl.content, cl.sent_at, cl.is_responded,
                   p.full_name, a.appointment_datetime, a.department
            FROM communication_logs cl
            JOIN patients p ON cl.patient_id = p.id
            LEFT JOIN appointments a ON cl.appointment_id = a.id
            WHERE cl.id = ?
            """,
            (notification_id,),
        ).fetchone()
    if not row:
        return None
    return {
        "id": row["id"],
        "type": row["channel"],
        "title": f"Thông báo {row['message_level'].replace('_', ' ')}",
        "message": row["content"],
        "is_read": bool(row["is_responded"]),
        "created_at": row["sent_at"],
        "ai_insight": f"{row['full_name']} có lịch khám {row['department'] or 'N/A'} lúc {row['appointment_datetime'] or 'N/A'}.",
    }


def dismiss_notification(notification_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE communication_logs SET is_responded = 1 WHERE id = ?",
            (notification_id,),
        )
        return cursor.rowcount > 0

from datetime import datetime, timedelta
from collections import defaultdict

from backend.app.core.database import get_db


def _relative_time(recorded_at: str) -> str:
    try:
        dt = datetime.strptime(recorded_at, "%Y-%m-%d %H:%M:%S")
        delta = datetime.now() - dt
        if delta < timedelta(hours=1):
            return f"{max(1, int(delta.total_seconds() // 60))} phút trước"
        if delta < timedelta(days=1):
            return f"{int(delta.total_seconds() // 3600)} giờ trước"
        return f"{delta.days} ngày trước"
    except (ValueError, TypeError):
        return "N/A"


def _glucose_status(value: float) -> str:
    if value < 5.6:
        return "GOOD"
    if value <= 7.0:
        return "STABLE"
    return "HIGH"


def _bp_status(systolic: float) -> str:
    if systolic < 120:
        return "GOOD"
    if systolic <= 140:
        return "STABLE"
    return "HIGH"


def get_latest_metrics(patient_id: int) -> dict:
    result = {"blood_glucose": None, "blood_pressure": None}
    with get_db() as conn:
        # Blood glucose
        bg = conn.execute(
            """
            SELECT metric_value, unit, recorded_at
            FROM clinical_metrics
            WHERE patient_id = ? AND metric_name = 'Blood Glucose'
            ORDER BY recorded_at DESC LIMIT 1
            """,
            (patient_id,),
        ).fetchone()
        if bg:
            result["blood_glucose"] = {
                "value": bg["metric_value"],
                "unit": bg["unit"],
                "status": _glucose_status(bg["metric_value"]),
                "updated_at": _relative_time(bg["recorded_at"]),
            }

        # Blood pressure (Systolic)
        bp = conn.execute(
            """
            SELECT metric_value, unit, recorded_at
            FROM clinical_metrics
            WHERE patient_id = ? AND metric_name = 'Systolic Blood Pressure'
            ORDER BY recorded_at DESC LIMIT 1
            """,
            (patient_id,),
        ).fetchone()
        if bp:
            result["blood_pressure"] = {
                "value": f"{int(bp['metric_value'])}/85",
                "unit": bp["unit"],
                "status": _bp_status(bp["metric_value"]),
                "updated_at": _relative_time(bp["recorded_at"]),
            }
    return result


def get_trend(patient_id: int, metric_type: str, days: int) -> list[dict]:
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    metric_map = {
        "blood_glucose": "Blood Glucose",
        "blood_pressure": "Systolic Blood Pressure",
    }
    metric_name = metric_map.get(metric_type, metric_type)

    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT metric_value, recorded_at
            FROM clinical_metrics
            WHERE patient_id = ? AND metric_name = ? AND recorded_at >= ?
            ORDER BY recorded_at ASC
            """,
            (patient_id, metric_name, cutoff),
        ).fetchall()

    return [
        {
            "date": r["recorded_at"][5:10].replace("-", "/") if r["recorded_at"] else "",
            "value": r["metric_value"],
        }
        for r in rows
    ]


def get_medication_status(patient_id: int) -> dict:
    # Simplified: kiểm tra nếu có medical_record gần đây → giả định đã uống thuốc
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT prescriptions, created_at
            FROM medical_records
            WHERE patient_id = ?
            ORDER BY created_at DESC LIMIT 1
            """,
            (patient_id,),
        ).fetchone()
    if row and row["prescriptions"]:
        return {"status": "TAKEN", "time": "Sáng nay"}
    return {"status": "PENDING", "time": None}


def get_clinical_history(patient_id: int, days: int = 30, max_series: int = 4, max_points_per_series: int = 8) -> list[dict]:
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT metric_name, metric_value, unit, recorded_at
            FROM clinical_metrics
            WHERE patient_id = ? AND recorded_at >= ?
            ORDER BY recorded_at ASC
            """,
            (patient_id, cutoff),
        ).fetchall()

    grouped: dict[str, dict] = {}
    for row in rows:
        metric_name = row["metric_name"]
        series = grouped.setdefault(
            metric_name,
            {
                "name": metric_name,
                "unit": row["unit"] or "",
                "points": [],
                "latestAt": row["recorded_at"],
            },
        )
        series["unit"] = series["unit"] or (row["unit"] or "")
        series["latestAt"] = row["recorded_at"]
        series["points"].append(
            {
                "date": row["recorded_at"][5:10].replace("-", "/") if row["recorded_at"] else "",
                "value": row["metric_value"],
            }
        )

    ordered_series = sorted(grouped.values(), key=lambda item: item.get("latestAt") or "", reverse=True)
    trimmed_series = []
    for series in ordered_series[:max_series]:
        points = series["points"][-max_points_per_series:]
        trimmed_series.append(
            {
                "name": series["name"],
                "unit": series["unit"],
                "points": points,
                "totalPoints": len(series["points"]),
            }
        )

    return trimmed_series

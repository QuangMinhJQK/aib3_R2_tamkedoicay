from backend.app.core.database import get_db


def ensure_jobs_table():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS video_jobs (
                id TEXT PRIMARY KEY,
                patient_id INTEGER,
                status TEXT,
                video_url TEXT,
                error TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME
            )
            """
        )


def create_job(job_id: str, patient_id: int) -> None:
    ensure_jobs_table()
    with get_db() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO video_jobs (id, patient_id, status, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (job_id, patient_id, "PENDING"),
        )


def update_job(job_id: str, status: str, video_url: str | None = None, error: str | None = None) -> bool:
    ensure_jobs_table()
    with get_db() as conn:
        cursor = conn.execute(
            """
            UPDATE video_jobs
            SET status = ?, video_url = COALESCE(?, video_url), error = COALESCE(?, error), updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (status, video_url, error, job_id),
        )
        return cursor.rowcount > 0


def get_job(job_id: str) -> dict | None:
    ensure_jobs_table()
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT id, patient_id, status, video_url, error, created_at, updated_at
            FROM video_jobs
            WHERE id = ?
            """,
            (job_id,),
        ).fetchone()
        return dict(row) if row else None


def list_jobs(limit: int = 50) -> list[dict]:
    ensure_jobs_table()
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT id, patient_id, status, video_url, error, created_at, updated_at
            FROM video_jobs
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

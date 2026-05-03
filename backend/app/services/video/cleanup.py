import shutil
import os

def cleanup_job_files(temp_dir: str) -> None:
    """
    Deletes the temporary job directory and all its contents (json, mp3).
    """
    if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Failed to cleanup {temp_dir}: {e}")

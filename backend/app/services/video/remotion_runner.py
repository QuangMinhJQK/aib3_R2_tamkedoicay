import subprocess
import os
import platform

def render_video(props_path: str, output_path: str) -> None:
    """
    Calls the Node.js Remotion subprocess to render the video.
    """
    # Assuming the remotion project is at video_renderer
    remotion_dir = os.path.abspath("video_renderer")
    props_abs_path = os.path.abspath(props_path)
    output_abs_path = os.path.abspath(output_path)
    
    # Build command as string for Windows compatibility with npx
    command = f'npx remotion render CareLoopVideo "{output_abs_path}" --props="{props_abs_path}"'
    
    result = subprocess.run(
        command,
        cwd=remotion_dir,
        capture_output=True,
        text=True,
        encoding='utf-8',
        shell=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Remotion render failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")

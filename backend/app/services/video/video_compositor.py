import subprocess
import os
import json
from typing import Optional, Dict, Any

class VideoCompositor:
    """
    Composes video, audio, and subtitles using FFmpeg.
    
    Performs:
    - Validation: Check file existence
    - Probing: Get video/audio duration and resolution
    - Filter Graph: Build subtitle filter if needed
    - Execution: Run FFmpeg with retry logic
    - Cleanup: Remove temporary files
    """
    
    def __init__(self, max_retries: int = 3, crf: int = 23):
        self.max_retries = max_retries
        self.crf = crf  # Quality: 0-51 (lower = better), 23 is default
        self.temp_files = []
    
    def validate_inputs(self, video_path: str, audio_path: str, subtitle_path: Optional[str] = None) -> None:
        """Validate that all input files exist."""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        if subtitle_path and not os.path.exists(subtitle_path):
            raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")
    
    def probe_file(self, file_path: str) -> Dict[str, Any]:
        """
        Get file information using ffprobe.
        
        Returns:
            Dict with 'duration' and 'width'/'height' (for video)
        """
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_format",
                "-show_streams",
                "-of", "json",
                file_path
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"ffprobe failed: {result.stderr}")
            
            data = json.loads(result.stdout)
            info = {
                "duration": float(data.get("format", {}).get("duration", 0))
            }
            
            # Get video dimensions if available
            for stream in data.get("streams", []):
                if stream.get("codec_type") == "video":
                    info["width"] = stream.get("width")
                    info["height"] = stream.get("height")
                    break
            
            return info
        except Exception as e:
            raise RuntimeError(f"Failed to probe {file_path}: {e}")
    
    def build_filter_graph(self, subtitle_path: Optional[str] = None, font_size: int = 24) -> str:
        """
        Build FFmpeg video filter graph for subtitle burning.
        
        Args:
            subtitle_path: Path to SRT file (if None, no subtitle filter)
            font_size: Font size for subtitle text
            
        Returns:
            Filter graph string (or empty string if no subtitles)
        """
        if not subtitle_path:
            return ""
        
        # Escape Windows paths for FFmpeg
        escaped_path = os.path.abspath(subtitle_path).replace("\\", "/").replace(":", "\\:")
        
        # FFmpeg subtitle filter with styling
        filter_graph = (
            f"subtitles='{escaped_path}':force_style="
            f"'FontSize={font_size},PrimaryColour=&HFFFFFF,BackColour=&H000000@0.7'"
        )
        return filter_graph
    
    def compose(
        self,
        video_path: str,
        audio_path: str,
        output_path: str,
        subtitle_path: Optional[str] = None,
        font_size: int = 24
    ) -> str:
        """
        Compose video, audio, and optionally subtitles using FFmpeg.
        
        Args:
            video_path: Path to input video (MP4 or similar)
            audio_path: Path to input audio (MP3, WAV, etc)
            output_path: Path to output video file
            subtitle_path: Optional path to SRT subtitle file
            font_size: Font size for burned-in subtitles
            
        Returns:
            Path to the composed video file
        """
        # Step 1: Validate inputs
        self.validate_inputs(video_path, audio_path, subtitle_path)
        
        # Step 2: Probe files to get duration
        video_info = self.probe_file(video_path)
        audio_info = self.probe_file(audio_path)
        
        # Step 3: Build filter graph
        filter_graph = self.build_filter_graph(subtitle_path, font_size)
        
        # Step 4: Create output directory
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        
        # Step 5: Build FFmpeg command
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "libx264",
            "-crf", str(self.crf),
            "-preset", "medium",
            "-c:a", "aac",
            "-b:a", "128k",
            "-af", "apad",
            "-shortest",  # Use shortest input duration
            "-movflags", "+faststart",  # Optimize for web streaming
        ]
        
        # Add filter graph if subtitles exist
        if filter_graph:
            cmd.extend(["-vf", filter_graph])
        
        # Add output path and overwrite flag
        cmd.extend(["-y", output_path])
        
        # Step 6: Execute with retry logic
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minute timeout
                    encoding="utf-8"
                )
                
                if result.returncode == 0:
                    return output_path
                else:
                    last_error = result.stderr
                    if attempt < self.max_retries:
                        print(f"FFmpeg attempt {attempt} failed, retrying... Error: {result.stderr[-200:]}")
                    continue
                    
            except subprocess.TimeoutExpired:
                last_error = "FFmpeg process timed out"
                if attempt < self.max_retries:
                    print(f"Attempt {attempt} timed out, retrying...")
            except Exception as e:
                last_error = str(e)
                if attempt < self.max_retries:
                    print(f"Attempt {attempt} failed with error: {e}")
        
        # All retries exhausted
        raise RuntimeError(
            f"Failed to compose video after {self.max_retries} attempts. "
            f"Last error: {last_error}"
        )
    
    def cleanup_temp_files(self) -> None:
        """Remove all temporary files created during composition."""
        for file_path in self.temp_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to cleanup {file_path}: {e}")

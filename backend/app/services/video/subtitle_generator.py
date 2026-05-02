import os
from typing import List, Tuple

class AdviceWithTiming:
    """Data class for advice text with timing information"""
    def __init__(self, text: str, start_frame: int, end_frame: int, fps: int = 30):
        self.text = text
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.fps = fps
    
    def frame_to_srt_time(self, frame: int) -> str:
        """Convert frame number to SRT time format (HH:MM:SS,mmm)"""
        seconds = frame / self.fps
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_subtitle_srt(advices_with_timing: List[AdviceWithTiming], output_path: str) -> None:
    """
    Generate SRT subtitle file from advice list with timing information.
    
    Args:
        advices_with_timing: List of AdviceWithTiming objects
        output_path: Path to save the SRT file
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    srt_content = []
    for idx, advice in enumerate(advices_with_timing, 1):
        start_time = advice.frame_to_srt_time(advice.start_frame)
        end_time = advice.frame_to_srt_time(advice.end_frame)
        
        # Clean text: remove newlines, limit to 42 chars per line
        text_lines = []
        words = advice.text.split()
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= 42:
                current_line += word + " " if current_line else word
            else:
                if current_line:
                    text_lines.append(current_line)
                current_line = word
        if current_line:
            text_lines.append(current_line)
        
        text = "\n".join(text_lines)
        
        srt_content.append(f"{idx}\n{start_time} --> {end_time}\n{text}\n")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_content))

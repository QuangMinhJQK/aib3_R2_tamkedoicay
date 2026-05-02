import os
import json
import uuid
from backend.app.services.video.llm_agent import extract_video_props
from backend.app.services.video.tts_engine import generate_audio_for_advice, build_synchronized_narration
from backend.app.services.video.remotion_runner import render_video
from backend.app.services.video.cleanup import cleanup_job_files
from backend.app.services.video.video_compositor import VideoCompositor
from backend.app.services.video.subtitle_generator import generate_subtitle_srt, AdviceWithTiming


def _build_section_text_map(props) -> dict:
    section_map = {
        "report_status": "",
        "health_metrics": "",
        "progress": "",
        "advice": "",
    }

    for item in getattr(props, "sectionNarrations", []) or []:
        if item.section in section_map and item.text:
            section_map[item.section] = item.text.strip()

    metric_parts = []
    for m in props.metrics[:4]:
        unit = f" {m.unit}" if m.unit else ""
        metric_parts.append(f"{m.label} is {m.value}{unit}")

    metric_sentence = "; ".join(metric_parts) if metric_parts else "there is not enough metric data yet"
    trend_map = {"up": "increasing", "down": "decreasing", "stable": "stable"}
    trend_summary = ", ".join([f"{m.label} is {trend_map.get(m.trend, 'stable')}" for m in props.metrics[:4]])

    if not section_map["report_status"]:
        section_map["report_status"] = (
            f"Health status report for {props.patientName}. "
            f"Current overall status: {props.overallStatus}."
        )
    if not section_map["health_metrics"]:
        section_map["health_metrics"] = f"Key health metrics include: {metric_sentence}."
    if not section_map["progress"]:
        section_map["progress"] = (
            f"Recent progress shows: {trend_summary}. "
            f"Overall, the condition is being closely monitored."
        )
    if not section_map["advice"]:
        advice_text = " ".join([a.text for a in props.advices[:3]])
        section_map["advice"] = advice_text or "Please continue a healthy routine and attend follow-up visits on schedule."

    return section_map


def run_video_pipeline(medical_record_text: str, job_id: str, jobs_state: dict) -> None:
    temp_dir = os.path.join("output", job_id)
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        jobs_state[job_id] = {"status": "PROCESSING"}
        
        # Step 1: Extract data using LLM
        props = extract_video_props(medical_record_text)
        
        # Step 2: Build section narrations for 4 segments and generate TTS.
        section_frames = {
            "report_status": 90,
            "health_metrics": 120,
            "progress": 120,
        }
        section_texts = _build_section_text_map(props)
        section_order = ["report_status", "health_metrics", "progress", "advice"]

        section_durations = {}
        for idx, section in enumerate(section_order):
            audio_path = os.path.join(temp_dir, f"section_{idx}_{section}.mp3")
            duration_frames = generate_audio_for_advice(section_texts[section], audio_path)
            section_durations[section] = {
                "audio_path": audio_path,
                "duration_frames": duration_frames,
            }

        # First 3 sections are fixed on screen. The advice section expands when needed.
        advice_frames = max(120, section_durations["advice"]["duration_frames"])
        total_frames = 330 + advice_frames

        # Update sectionNarrations with actual durations for traceability.
        for item in getattr(props, "sectionNarrations", []) or []:
            if item.section in section_durations:
                item.audioDurationInFrames = section_durations[item.section]["duration_frames"]

        # Subtitle timeline follows actual section slots in the video.
        timeline = {
            "report_status": (0, section_frames["report_status"]),
            "health_metrics": (90, 210),
            "progress": (210, 330),
            "advice": (330, total_frames),
        }

        advices_with_timing = []
        audio_segments = []

        for section in section_order:
            start_frame, end_frame = timeline[section]
            audio_path = section_durations[section]["audio_path"]
            narration_text = section_texts[section]

            advices_with_timing.append(
                AdviceWithTiming(narration_text, start_frame, end_frame, fps=30)
            )
            audio_segments.append(
                {
                    "audio_path": audio_path,
                    "start_ms": int(start_frame * 1000 / 30),
                    "end_ms": int(end_frame * 1000 / 30),
                }
            )
        
        props.totalDurationInFrames = total_frames
        
        # Step 3: Save MasterProps.json
        props_path = os.path.join(temp_dir, "master_props.json")
        with open(props_path, "w", encoding="utf-8", errors="replace") as f:
            f.write(props.model_dump_json())
        
        # Step 4: Generate SRT subtitles
        subtitle_path = os.path.join(temp_dir, "subtitles.srt")
        generate_subtitle_srt(advices_with_timing, subtitle_path)

        # Step 5: Render Video via Remotion (silent animation)
        video_mp4 = os.path.join(temp_dir, f"silent_video.mp4")
        render_video(props_path, video_mp4)

        # Step 6: Build synchronized narration with silence padding to video duration.
        target_duration_ms = int(total_frames * 1000 / 30)
        combined_audio_path = os.path.join(temp_dir, "combined_audio.mp3")
        build_synchronized_narration(
            segments=audio_segments,
            output_path=combined_audio_path,
            target_duration_ms=target_duration_ms,
        )
        
        # Step 7: Composite video + audio + subtitles
        compositor = VideoCompositor(crf=23)
        output_mp4 = os.path.join("output", f"{job_id}.mp4")
        compositor.compose(
            video_path=video_mp4,
            audio_path=combined_audio_path,
            output_path=output_mp4,
            subtitle_path=subtitle_path,
            font_size=24
        )
        
        jobs_state[job_id] = {
            "status": "COMPLETED",
            "video_url": f"/static/videos/{job_id}.mp4"
        }
        
    except Exception as e:
        print(f"Video Pipeline Error: {e}")
        jobs_state[job_id] = {"status": "FAILED", "error": str(e)}
    finally:
        cleanup_job_files(temp_dir)


import os
import requests
from mutagen.mp3 import MP3
from pydub import AudioSegment
from pydub.effects import speedup


def generate_audio_for_advice(text: str, output_path: str) -> int:
    provider = os.getenv("TTS_PROVIDER", "disabled")

    if provider == "disabled":
        word_count = len(text.split())
        estimated_seconds = word_count / 2.5
        duration_frames = int((estimated_seconds + 1.0) * 30)
        duration_ms = int(duration_frames * 1000 / 30)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        AudioSegment.silent(duration=max(1, duration_ms)).export(output_path, format="mp3")
        return duration_frames

    elif provider == "elevenlabs":
        api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY is not set.")

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }

        voices_resp = requests.get(
            "https://api.elevenlabs.io/v1/voices",
            headers=headers,
            timeout=10
        )

        if voices_resp.status_code != 200:
            raise RuntimeError(f"Fetch voices failed: {voices_resp.text}")

        voices = voices_resp.json().get("voices", [])
        if not voices:
            raise ValueError("No voices found.")

        preferred = os.getenv("ELEVENLABS_VOICE_NAME")
        if preferred:
            match = next((v for v in voices if v["name"] == preferred), None)
            if not match:
                raise ValueError(f"Voice '{preferred}' not found.")
            voice_id = match["voice_id"]
        else:
            voice_id = voices[0]["voice_id"]

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        tts_headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        response = requests.post(
            url,
            json=data,
            headers=tts_headers,
            timeout=30,
            stream=True
        )

        if response.status_code != 200:
            raise RuntimeError(f"TTS failed: {response.text}")

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(1024):
                if chunk:
                    f.write(chunk)

        try:
            audio = MP3(output_path)
            return int(audio.info.length * 30)
        except Exception as e:
            raise RuntimeError(f"MP3 parse failed: {e}")

    else:
        raise ValueError(f"Unknown TTS provider: {provider}")


def build_synchronized_narration(
    segments: list,
    output_path: str,
    target_duration_ms: int,
) -> str:
    """
    Build one narration track aligned to timed subtitle slots.

    Expected segment format:
      {
        "audio_path": str,
        "start_ms": int,
        "end_ms": int,
      }
    """
    if target_duration_ms <= 0:
        raise ValueError("target_duration_ms must be > 0")

    timeline = AudioSegment.silent(duration=target_duration_ms)
    allowed_speed = (1.0, 1.1, 1.25, 1.5)

    for segment in segments:
        audio_path = segment["audio_path"]
        start_ms = max(0, int(segment["start_ms"]))
        end_ms = max(start_ms, int(segment["end_ms"]))
        slot_ms = max(1, end_ms - start_ms)

        if not os.path.exists(audio_path):
            continue

        clip = AudioSegment.from_file(audio_path)

        if len(clip) > slot_ms:
            for factor in allowed_speed[1:]:
                candidate = speedup(clip, playback_speed=factor)
                if len(candidate) <= slot_ms:
                    clip = candidate
                    break
            if len(clip) > slot_ms:
                clip = clip[:slot_ms]

        if len(clip) < slot_ms:
            clip += AudioSegment.silent(duration=slot_ms - len(clip))

        timeline = timeline.overlay(clip, position=start_ms)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    timeline.export(output_path, format="mp3")
    return output_path
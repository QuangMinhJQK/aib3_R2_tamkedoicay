import os
import json
from openai import OpenAI
from backend.app.models.video_schema import MasterProps


def _extract_json_object(content: str) -> dict:
    """
    Extract the first JSON object from a model response.

    This tolerates leading/trailing markdown or commentary by locating the
    first '{' and using JSONDecoder.raw_decode to parse the first object only.
    """
    if not content:
        raise ValueError("Empty model response")

    start_index = content.find("{")
    if start_index == -1:
        raise ValueError("No JSON object found in model response")

    decoder = json.JSONDecoder()
    parsed, _ = decoder.raw_decode(content[start_index:])
    return parsed

def extract_video_props(medical_record_text: str) -> MasterProps:
    """Extract structured data from a medical record using LLM."""
    client = OpenAI(
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        api_key=os.getenv("OPENROUTER_API_KEY", "")
    )
    
    model = os.getenv("REASONING_MODEL", "openai/gpt-oss-120b:free")
    
    prompt = f"""
    You are a medical data extraction AI. Extract the following medical record into a structured JSON format.
    Important requirement: Generate narration text with full context for exactly 4 video segments:
    1) report_status
    2) health_metrics
    3) progress
    4) advice

    All generated text fields MUST be in English only.
    Each narration text should be concise, natural English speech (2-5 sentences) suitable for TTS.
    sectionNarrations must always have exactly 4 items and preserve the above section order.
    The output MUST exactly match this JSON schema (do not include Markdown wrappers like ```json, just output the raw JSON object):
    {{
        "patientName": "string",
        "overallStatus": "string (e.g., Good, Stable, Needs Attention)",
        "metrics": [
            {{ "label": "string", "value": "string", "trend": "up|down|stable", "unit": "string" }}
        ],
        "advices": [
            {{ "text": "string", "audioDurationInFrames": 0 }}
        ],
        "sectionNarrations": [
            {{ "section": "report_status", "text": "string", "audioDurationInFrames": 0 }},
            {{ "section": "health_metrics", "text": "string", "audioDurationInFrames": 0 }},
            {{ "section": "progress", "text": "string", "audioDurationInFrames": 0 }},
            {{ "section": "advice", "text": "string", "audioDurationInFrames": 0 }}
        ],
        "totalDurationInFrames": 0
    }}
    
    Medical Record:
    {medical_record_text}
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    
    content = response.choices[0].message.content or "{}"
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    # Parse and validate against our Pydantic schema
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = _extract_json_object(content)
    # Ensure audioDurationInFrames and totalDurationInFrames are at least 0
    return MasterProps(**data)

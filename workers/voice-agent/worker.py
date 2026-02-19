"""
Voice Agent Worker - Generates voiceover using Kokoro (local) or ElevenLabs (API)
"""

import os
import logging
import time
import requests
from pathlib import Path
from datetime import datetime
from supabase import create_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:8000")
ASSETS_DIR = Path("/assets/renders")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_with_elevenlabs(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
    """Generate voice with ElevenLabs API"""
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY not configured")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    logger.info("Generating voice with ElevenLabs...")
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"ElevenLabs error: {response.text}")
        raise Exception(f"Voice generation failed: {response.status_code}")
    
    return response.content

def poll_and_work():
    """Main worker loop"""
    worker_id = f"voice-agent-{os.getpid()}"
    
    logger.info(f"Voice Agent started: {worker_id}")
    
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    while True:
        try:
            # Poll for voiceover jobs
            response = requests.get(
                f"{ORCHESTRATOR_URL}/jobs/poll",
                params={"worker_type": "voice-agent", "limit": 1}
            )
            
            if response.status_code != 200:
                logger.error(f"Poll failed: {response.status_code}")
                time.sleep(5)
                continue
            
            jobs = response.json()
            
            if not jobs:
                time.sleep(5)
                continue
            
            job = jobs[0]
            job_id = job['id']
            project_id = job['project_id']
            
            logger.info(f"Processing voice job {job_id}")
            
            # Claim
            claim_response = requests.post(
                f"{ORCHESTRATOR_URL}/jobs/{job_id}/claim",
                params={"worker_id": worker_id}
            )
            
            if claim_response.status_code != 200:
                continue
            
            # Get project and script
            project = supabase.table('projects').select('*').eq('id', project_id).single().execute()
            if not project.data:
                raise Exception("Project not found")
            
            script = project.data.get('script_content', {})
            segments = script.get('segments', [])
            
            # Combine all text
            full_text = ' '.join([seg.get('text', '') for seg in segments])
            
            # Generate voice
            audio_data = generate_with_elevenlabs(full_text)
            
            # Save
            output_file = ASSETS_DIR / f"voice_{project_id}.mp3"
            output_file.write_bytes(audio_data)
            
            # Complete
            requests.post(
                f"{ORCHESTRATOR_URL}/jobs/{job_id}/complete",
                json={
                    "output": {
                        "voice_url": str(output_file)
                    }
                }
            )
            
            logger.info(f"Voice generated: {output_file}")
            
        except Exception as e:
            logger.error(f"Error: {e}")
            if 'job_id' in locals():
                try:
                    requests.post(
                        f"{ORCHESTRATOR_URL}/jobs/{job_id}/fail",
                        params={"error": str(e)}
                    )
                except:
                    pass
            time.sleep(5)

if __name__ == "__main__":
    poll_and_work()

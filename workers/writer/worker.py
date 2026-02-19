"""
Writer Worker - Generates scripts using Gemini or Moonshot AI
"""

import os
import logging
import time
import requests
from datetime import datetime
from supabase import create_client
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:8000")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def call_gemini(prompt: str, model: str = "gemini-1.5-pro") -> str:
    """Call Gemini API"""
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not configured")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Gemini error: {response.text}")
        raise Exception(f"Gemini API error: {response.status_code}")
    
    data = response.json()
    
    if "candidates" not in data or not data["candidates"]:
        raise Exception("No response from Gemini")
    
    return data["candidates"][0]["content"]["parts"][0]["text"]

def call_moonshot(prompt: str, model: str = "moonshot-v1-8k") -> str:
    """Call Moonshot API (Kimi)"""
    if not MOONSHOT_API_KEY:
        raise RuntimeError("MOONSHOT_API_KEY not configured")
    
    url = "https://api.moonshot.cn/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {MOONSHOT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Moonshot error: {response.text}")
        raise Exception(f"Moonshot API error: {response.status_code}")
    
    data = response.json()
    return data["choices"][0]["message"]["content"]

def generate_script(project_data: dict, research_data: dict, template: dict) -> dict:
    """
    Generate timed script based on project, research, and template
    """
    brief = project_data.get('creative_brief', {})
    template_id = brief.get('template', 'pre-race-preview')
    
    # Get system prompt from template
    system_prompt = template.get('system_prompt', 'You are a racing content creator.')
    
    # Get target length
    default_brief = template.get('default_brief', {})
    target_length = brief.get('length_seconds', default_brief.get('length_seconds', 60))
    
    # Build prompt
    race_name = research_data.get('race_name', 'the upcoming race')
    
    prompt = f"""{system_prompt}

Create a {target_length}-second TikTok script about {race_name}.

RESEARCH DATA:
{json.dumps(research_data.get('raw_data', {}), indent=2)}

REQUIREMENTS:
- Hook (first 3 seconds): Must grab attention immediately
- Total duration: ~{target_length} seconds
- Format: JSON array with timed segments
- Each segment: start_time, end_time, text, visual_prompt

Example format:
[
  {{"start": 0, "end": 3, "text": "The horse the bookies fear...", "visual_prompt": "close_up_horse_intense"}},
  {{"start": 3, "end": 8, "text": "Midnight Run, barrier 4", "visual_prompt": "barrier_draw_graphic"}}
]

Output ONLY valid JSON. No markdown, no explanation."""

    # Try Gemini first, fallback to Moonshot
    try:
        logger.info("Using Gemini for script generation")
        response = call_gemini(prompt)
    except Exception as e:
        logger.warning(f"Gemini failed: {e}, trying Moonshot")
        response = call_moonshot(prompt)
    
    # Parse JSON response
    try:
        # Clean up response (remove markdown if present)
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        
        segments = json.loads(cleaned.strip())
        
        # Validate structure
        if not isinstance(segments, list):
            raise ValueError("Response is not a JSON array")
        
        for seg in segments:
            if not all(k in seg for k in ['start', 'end', 'text']):
                raise ValueError(f"Segment missing required fields: {seg}")
        
        # Build full script structure
        script = {
            "segments": segments,
            "total_duration": segments[-1]['end'] if segments else target_length,
            "word_count": sum(len(seg['text'].split()) for seg in segments),
            "template_used": template_id,
            "generated_at": datetime.now().isoformat()
        }
        
        return script
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse script JSON: {e}")
        logger.error(f"Raw response: {response}")
        raise Exception(f"Invalid JSON from LLM: {e}")

def poll_and_work():
    """Main worker loop"""
    worker_id = f"writer-{os.getpid()}"
    
    logger.info(f"Writer Worker started: {worker_id}")
    logger.info(f"Gemini: {'Enabled' if GEMINI_API_KEY else 'Disabled'}")
    logger.info(f"Moonshot: {'Enabled' if MOONSHOT_API_KEY else 'Disabled'}")
    
    while True:
        try:
            # Poll for pending write jobs
            response = requests.get(
                f"{ORCHESTRATOR_URL}/jobs/poll",
                params={"worker_type": "writer", "limit": 1}
            )
            
            if response.status_code != 200:
                logger.error(f"Poll failed: {response.status_code}")
                time.sleep(5)
                continue
            
            jobs = response.json()
            
            if not jobs:
                logger.debug("No jobs available, sleeping...")
                time.sleep(5)
                continue
            
            job = jobs[0]
            job_id = job['id']
            project_id = job['project_id']
            
            logger.info(f"Processing job {job_id} for project {project_id}")
            
            # Claim the job
            claim_response = requests.post(
                f"{ORCHESTRATOR_URL}/jobs/{job_id}/claim",
                params={"worker_id": worker_id}
            )
            
            if claim_response.status_code != 200:
                logger.warning(f"Failed to claim job {job_id}: {claim_response.text}")
                continue
            
            # Get project data
            project = supabase.table('projects').select('*').eq('id', project_id).single().execute()
            if not project.data:
                raise Exception(f"Project {project_id} not found")
            
            project_data = project.data
            brief = project_data.get('creative_brief', {})
            template_id = brief.get('template', 'pre-race-preview')
            
            # Get template
            template_result = supabase.table('templates').select('*').eq('id', template_id).single().execute()
            template = template_result.data if template_result.data else {}
            
            # Get research data (latest)
            research = supabase.table('research_data').select('*').eq('project_id', project_id).order('created_at', desc=True).limit(1).execute()
            if not research.data or len(research.data) == 0:
                raise Exception(f"No research data for project {project_id}")
            
            research_data = research.data[0]
            
            # Generate script
            script = generate_script(project_data, research_data, template)
            
            # Mark job complete
            complete_response = requests.post(
                f"{ORCHESTRATOR_URL}/jobs/{job_id}/complete",
                json={
                    "output": {
                        "script_content": script
                    }
                },
                params={"next_status": "approval_script"}
            )
            
            logger.info(f"Job {job_id} completed. Script: {script['word_count']} words, {script['total_duration']}s")
            
        except Exception as e:
            logger.error(f"Error processing job: {e}")
            
            if 'job_id' in locals():
                try:
                    requests.post(
                        f"{ORCHESTRATOR_URL}/jobs/{job_id}/fail",
                        params={"error": str(e), "retry": True}
                    )
                except:
                    pass
            
            time.sleep(5)

if __name__ == "__main__":
    poll_and_work()

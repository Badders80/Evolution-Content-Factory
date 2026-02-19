"""
Researcher Worker - Scrapes racing data from websites
Uses Firecrawl for clean markdown extraction
"""

import os
import time
import logging
from datetime import datetime
from supabase import create_client
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "fc-3b50a4365330469f9660eec86fe5cfc8")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:8000")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Racing site configurations
RACING_SOURCES = {
    "racing.com": {
        "name": "Racing.com",
        "base_url": "https://www.racing.com",
        "selector_map": {
            "race_name": "h1.race-name",
            "date": ".race-date",
            "runners": ".runner-row"
        }
    },
    "tab.co.nz": {
        "name": "TAB NZ",
        "base_url": "https://www.tab.co.nz",
        "selector_map": {}
    },
    "nztr.co.nz": {
        "name": "NZ Thoroughbred Racing",
        "base_url": "https://www.nztr.co.nz",
        "selector_map": {}
    }
}

def scrape_with_firecrawl(url: str) -> dict:
    """
    Scrape URL using Firecrawl API
    Returns clean markdown + metadata
    """
    if not FIRECRAWL_API_KEY:
        raise RuntimeError("FIRECRAWL_API_KEY not configured")
    
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Scrape endpoint
    scrape_url = "https://api.firecrawl.dev/v1/scrape"
    payload = {
        "url": url,
        "formats": ["markdown", "html"],
        "onlyMainContent": True
    }
    
    logger.info(f"Scraping: {url}")
    response = requests.post(scrape_url, json=payload, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Firecrawl error: {response.text}")
        raise Exception(f"Scraping failed: {response.status_code}")
    
    data = response.json()
    
    if not data.get("success"):
        raise Exception(f"Firecrawl error: {data.get('error', 'Unknown')}")
    
    return {
        "markdown": data["data"]["markdown"],
        "html": data["data"].get("html", ""),
        "metadata": data["data"].get("metadata", {}),
        "url": url
    }

def extract_racing_data(markdown: str, source_url: str) -> dict:
    """
    Extract structured racing data from markdown
    This is a simplified parser - can be enhanced with LLM
    """
    data = {
        "source_url": source_url,
        "raw_markdown": markdown,
        "extracted_at": datetime.now().isoformat(),
        "runners": [],
        "race_name": None,
        "race_date": None,
        "venue": None
    }
    
    # Simple regex/pattern extraction (enhance with Gemini later)
    lines = markdown.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Look for race name (usually first h1)
        if line.startswith('# ') and not data["race_name"]:
            data["race_name"] = line.replace('# ', '').strip()
        
        # Look for dates (simple pattern)
        if any(month in line.lower() for month in ['january', 'february', 'march', 'april', 'may', 'june', 
                                                    'july', 'august', 'september', 'october', 'november', 'december']):
            if not data["race_date"]:
                data["race_date"] = line
    
    return data

def poll_and_work():
    """Main worker loop - poll for jobs and process"""
    worker_id = f"researcher-{os.getpid()}"
    
    logger.info(f"Researcher Worker started: {worker_id}")
    logger.info(f"Orchestrator: {ORCHESTRATOR_URL}")
    
    while True:
        try:
            # Poll for pending research jobs
            response = requests.get(
                f"{ORCHESTRATOR_URL}/jobs/poll",
                params={"worker_type": "researcher", "limit": 1}
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
            
            # Get project details
            project = supabase.table('projects').select('*').eq('id', project_id).single().execute()
            if not project.data:
                raise Exception(f"Project {project_id} not found")
            
            project_data = project.data
            race_url = project_data.get('race_url')
            
            if not race_url:
                raise Exception(f"No race_url for project {project_id}")
            
            # Scrape the racing page
            scrape_result = scrape_with_firecrawl(race_url)
            
            # Extract structured data
            racing_data = extract_racing_data(scrape_result['markdown'], race_url)
            
            # Save to research_data table
            research_record = {
                "project_id": project_id,
                "source_url": race_url,
                "source_name": detect_source(race_url),
                "raw_data": racing_data,
                "summary": generate_summary(racing_data)
            }
            
            supabase.table('research_data').insert(research_record).execute()
            
            # Mark job complete
            complete_response = requests.post(
                f"{ORCHESTRATOR_URL}/jobs/{job_id}/complete",
                json={
                    "output": {
                        "research_data_id": research_record.get('id'),
                        "source": research_record['source_name'],
                        "race_name": racing_data.get('race_name')
                    }
                },
                params={"next_status": "scripting"}
            )
            
            logger.info(f"Job {job_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Error processing job: {e}")
            
            # Try to fail the job if we have a job_id
            if 'job_id' in locals():
                try:
                    requests.post(
                        f"{ORCHESTRATOR_URL}/jobs/{job_id}/fail",
                        params={"error": str(e), "retry": True}
                    )
                except:
                    pass
            
            time.sleep(5)

def detect_source(url: str) -> str:
    """Detect which racing site we're scraping"""
    url_lower = url.lower()
    for domain, config in RACING_SOURCES.items():
        if domain in url_lower:
            return config['name']
    return "Unknown"

def generate_summary(data: dict) -> str:
    """Generate AI summary of racing data (placeholder for LLM)"""
    race_name = data.get('race_name', 'Unknown Race')
    return f"Research completed for {race_name}. Raw data extracted."

if __name__ == "__main__":
    poll_and_work()

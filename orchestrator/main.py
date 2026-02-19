from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from supabase import create_client
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Evolution Content Factory API",
    description="State machine orchestrator for AI-powered TikTok content",
    version="3.0.0"
)

# Initialize Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    logger.error("SUPABASE_URL and SUPABASE_KEY must be set")
    raise RuntimeError("Database credentials not configured")

supabase = create_client(supabase_url, supabase_key)

# Valid state transitions (must match database enum)
VALID_TRANSITIONS = {
    'idea': ['researching'],
    'researching': ['scripting', 'failed'],
    'scripting': ['approval_script', 'failed'],
    'approval_script': ['gathering_clips', 'scripting'],  # Approve or reject
    'gathering_clips': ['approval_clips', 'failed'],
    'approval_clips': ['rendering', 'gathering_clips'],  # Approve or reject
    'rendering': ['approval_final', 'failed'],
    'approval_final': ['done', 'rendering'],  # Approve or re-render
    'done': [],  # Terminal state
    'failed': ['researching', 'scripting', 'gathering_clips', 'rendering']  # Retry
}

# Request/Response Models
class ProjectCreate(BaseModel):
    title: str
    race_url: Optional[str] = None
    creative_brief: Dict[str, Any] = Field(default_factory=dict)
    telegram_chat_id: Optional[str] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    creative_brief: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class StatusTransition(BaseModel):
    to_status: str
    reason: Optional[str] = None

class TemplateResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    default_brief: Dict[str, Any]

# Health check
@app.get("/")
def health_check():
    try:
        # Test database connection
        result = supabase.table('projects').select('count', count='exact').execute()
        return {
            "status": "healthy",
            "database": "connected",
            "version": "3.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Database connection failed")

# Projects API
@app.post("/projects", status_code=201)
def create_project(project: ProjectCreate):
    """Create a new content project"""
    try:
        data = {
            "title": project.title,
            "race_url": project.race_url,
            "creative_brief": project.creative_brief,
            "telegram_chat_id": project.telegram_chat_id,
            "status": "idea"
        }
        result = supabase.table('projects').insert(data).execute()
        
        # Create initial research job
        if result.data:
            project_id = result.data[0]['id']
            supabase.table('jobs').insert({
                "project_id": project_id,
                "job_type": "research",
                "status": "pending",
                "input_payload": {"race_url": project.race_url}
            }).execute()
        
        return result.data[0]
    except Exception as e:
        logger.error(f"Failed to create project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projects")
def list_projects(status: Optional[str] = None, limit: int = 50):
    """List projects with optional status filter"""
    try:
        query = supabase.table('projects').select('*').order('created_at', desc=True).limit(limit)
        if status:
            query = query.eq('status', status)
        result = query.execute()
        return result.data
    except Exception as e:
        logger.error(f"Failed to list projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projects/{project_id}")
def get_project(project_id: str):
    """Get project details"""
    try:
        result = supabase.table('projects').select('*').eq('id', project_id).single().execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Project not found")
        return result.data
    except Exception as e:
        logger.error(f"Failed to get project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/projects/{project_id}/transition")
def transition_status(project_id: str, transition: StatusTransition):
    """Transition project to new status (with validation)"""
    try:
        # Get current project
        project = supabase.table('projects').select('status').eq('id', project_id).single().execute()
        if not project.data:
            raise HTTPException(status_code=404, detail="Project not found")
        
        current_status = project.data['status']
        new_status = transition.to_status
        
        # Validate transition
        if new_status not in VALID_TRANSITIONS.get(current_status, []):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid transition: {current_status} -> {new_status}. Valid: {VALID_TRANSITIONS[current_status]}"
            )
        
        # Update status
        update_data = {
            "status": new_status,
            "updated_at": datetime.now().isoformat()
        }
        
        result = supabase.table('projects').update(update_data).eq('id', project_id).execute()
        
        # Trigger background job based on new status
        if new_status == 'researching':
            create_research_job(project_id)
        elif new_status == 'scripting':
            create_script_job(project_id)
        elif new_status == 'gathering_clips':
            create_clip_jobs(project_id)
        elif new_status == 'rendering':
            create_render_job(project_id)
        
        return result.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to transition status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Jobs API (for workers to poll)
@app.get("/jobs/poll")
def poll_jobs(worker_type: str, limit: int = 1):
    """Workers poll for available jobs"""
    try:
        job_type_map = {
            'researcher': 'research',
            'writer': 'write',
            'clip-agent': 'download_clip',
            'editor': 'render',
            'voice-agent': 'voiceover'
        }
        
        job_type = job_type_map.get(worker_type)
        if not job_type:
            raise HTTPException(status_code=400, detail=f"Unknown worker type: {worker_type}")
        
        result = supabase.table('jobs')\
            .select('*')\
            .eq('job_type', job_type)\
            .eq('status', 'pending')\
            .order('created_at')\
            .limit(limit)\
            .execute()
        
        return result.data
    except Exception as e:
        logger.error(f"Failed to poll jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/jobs/{job_id}/claim")
def claim_job(job_id: str, worker_id: str):
    """Worker claims a job (prevents double-processing)"""
    try:
        result = supabase.table('jobs').update({
            "status": "claimed",
            "worker_id": worker_id,
            "claimed_at": datetime.now().isoformat()
        }).eq('id', job_id).eq('status', 'pending').execute()
        
        if not result.data:
            raise HTTPException(status_code=409, detail="Job already claimed or not found")
        
        return result.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to claim job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/jobs/{job_id}/complete")
def complete_job(job_id: str, output: Dict[str, Any], next_status: Optional[str] = None):
    """Worker completes job and optionally triggers status transition"""
    try:
        # Update job
        job_result = supabase.table('jobs').update({
            "status": "complete",
            "output_payload": output,
            "completed_at": datetime.now().isoformat()
        }).eq('id', job_id).execute()
        
        if not job_result.data:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = job_result.data[0]
        
        # Update project with output
        if 'script_content' in output:
            supabase.table('projects').update({
                "script_content": output['script_content']
            }).eq('id', job['project_id']).execute()
        
        if 'video_url' in output:
            supabase.table('projects').update({
                "video_url": output['video_url']
            }).eq('id', job['project_id']).execute()
        
        # Trigger status transition if provided
        if next_status:
            transition = StatusTransition(to_status=next_status, reason="Job completed")
            transition_status(job['project_id'], transition)
        
        return job_result.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to complete job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/jobs/{job_id}/fail")
def fail_job(job_id: str, error: str, retry: bool = True):
    """Worker reports job failure"""
    try:
        job_result = supabase.table('jobs').select('*').eq('id', job_id).single().execute()
        if not job_result.data:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = job_result.data[0]
        retry_count = job.get('retry_count', 0) + 1
        max_retries = job.get('max_retries', 3)
        
        if retry and retry_count < max_retries:
            # Requeue for retry
            result = supabase.table('jobs').update({
                "status": "pending",
                "retry_count": retry_count,
                "error_message": error
            }).eq('id', job_id).execute()
        else:
            # Mark as failed
            result = supabase.table('jobs').update({
                "status": "failed",
                "retry_count": retry_count,
                "error_message": error
            }).eq('id', job_id).execute()
            
            # Also mark project as failed
            supabase.table('projects').update({
                "status": "failed",
                "error_count": retry_count,
                "last_error": error
            }).eq('id', job['project_id']).execute()
        
        return result.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fail job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Templates API
@app.get("/templates")
def list_templates():
    """List available content templates"""
    try:
        result = supabase.table('templates').select('*').execute()
        return result.data
    except Exception as e:
        logger.error(f"Failed to list templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/templates/{template_id}")
def get_template(template_id: str):
    """Get template details"""
    try:
        result = supabase.table('templates').select('*').eq('id', template_id).single().execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Template not found")
        return result.data
    except Exception as e:
        logger.error(f"Failed to get template: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions for job creation
def create_research_job(project_id: str):
    """Create research job for project"""
    supabase.table('jobs').insert({
        "project_id": project_id,
        "job_type": "research",
        "status": "pending",
        "input_payload": {"project_id": project_id}
    }).execute()

def create_script_job(project_id: str):
    """Create script writing job"""
    supabase.table('jobs').insert({
        "project_id": project_id,
        "job_type": "write",
        "status": "pending",
        "input_payload": {"project_id": project_id}
    }).execute()

def create_clip_jobs(project_id: str):
    """Create clip download jobs from creative_brief"""
    project = supabase.table('projects').select('creative_brief').eq('id', project_id).single().execute()
    if project.data:
        brief = project.data.get('creative_brief', {})
        clips = brief.get('youtube_clips', [])
        
        for clip in clips:
            # Insert clip and get ID
            clip_result = supabase.table('clips').insert({
                "project_id": project_id,
                "youtube_url": clip['url'],
                "start_seconds": clip.get('start', 0),
                "end_seconds": clip.get('end', 30),
                "label": clip.get('label', 'clip')
            }).execute()
            
            clip_id = clip_result.data[0]['id'] if clip_result.data else None
            
            # Create job with clip_id
            job_payload = {**clip, 'clip_id': clip_id}
            supabase.table('jobs').insert({
                "project_id": project_id,
                "job_type": "download_clip",
                "status": "pending",
                "input_payload": job_payload
            }).execute()

def create_render_job(project_id: str):
    """Create video render job"""
    supabase.table('jobs').insert({
        "project_id": project_id,
        "job_type": "render",
        "status": "pending",
        "input_payload": {"project_id": project_id}
    }).execute()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

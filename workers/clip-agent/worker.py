"""
Clip Agent Worker - Downloads and extracts YouTube video segments
Uses yt-dlp for downloading, FFmpeg for extraction
"""

import os
import subprocess
import logging
import time
import requests
from pathlib import Path
from datetime import datetime
from supabase import create_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:8000")
ASSETS_DIR = Path("/assets/clips")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def download_youtube_video(url: str, output_dir: Path) -> Path:
    """
    Download best quality video from YouTube using yt-dlp
    """
    logger.info(f"Downloading: {url}")
    
    # yt-dlp command for best quality
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "--output", str(output_dir / "%(id)s.%(ext)s"),
        "--no-playlist",
        "--newline",
        url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"yt-dlp error: {result.stderr}")
        raise Exception(f"Download failed: {result.stderr}")
    
    # Find downloaded file
    video_id = url.split("v=")[-1].split("&")[0]
    downloaded_file = output_dir / f"{video_id}.mp4"
    
    if not downloaded_file.exists():
        # Try to find any mp4 in the directory
        mp4_files = list(output_dir.glob("*.mp4"))
        if mp4_files:
            downloaded_file = mp4_files[0]
        else:
            raise Exception("Downloaded file not found")
    
    logger.info(f"Downloaded to: {downloaded_file}")
    return downloaded_file

def extract_segment(input_file: Path, output_file: Path, start_sec: int, end_sec: int) -> Path:
    """
    Extract segment using FFmpeg with NVENC encoding
    Crops to 9:16 vertical format
    """
    duration = end_sec - start_sec
    
    logger.info(f"Extracting {duration}s segment from {start_sec}s to {end_sec}s")
    logger.info(f"Output: {output_file}")
    
    # FFmpeg command with NVENC hardware encoding
    # Crops to 9:16 vertical (1080x1920) for TikTok
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output
        "-ss", str(start_sec),  # Start time
        "-t", str(duration),  # Duration
        "-i", str(input_file),  # Input
        "-vf", "crop=ih*9/16:ih,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",  # Crop to 9:16
        "-c:v", "h264_nvenc",  # NVENC hardware encoder
        "-preset", "fast",  # Encoding speed
        "-crf", "23",  # Quality
        "-c:a", "aac",  # Audio codec
        "-b:a", "128k",  # Audio bitrate
        "-movflags", "+faststart",  # Web optimization
        str(output_file)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"FFmpeg error: {result.stderr}")
        # Fallback to CPU encoding if NVENC fails
        return extract_segment_cpu(input_file, output_file, start_sec, end_sec)
    
    logger.info(f"Segment extracted: {output_file}")
    return output_file

def extract_segment_cpu(input_file: Path, output_file: Path, start_sec: int, end_sec: int) -> Path:
    """Fallback CPU-based extraction"""
    duration = end_sec - start_sec
    
    logger.info(f"Using CPU fallback for extraction")
    
    cmd = [
        "ffmpeg",
        "-y",
        "-ss", str(start_sec),
        "-t", str(duration),
        "-i", str(input_file),
        "-vf", "crop=ih*9/16:ih,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "28",
        "-c:a", "aac",
        "-b:a", "128k",
        str(output_file)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"FFmpeg CPU fallback failed: {result.stderr}")
    
    return output_file

def poll_and_work():
    """Main worker loop"""
    worker_id = f"clip-agent-{os.getpid()}"
    
    logger.info(f"Clip Agent Worker started: {worker_id}")
    logger.info(f"Assets directory: {ASSETS_DIR}")
    
    # Ensure assets directory exists
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    while True:
        try:
            # Poll for pending clip download jobs
            response = requests.get(
                f"{ORCHESTRATOR_URL}/jobs/poll",
                params={"worker_type": "clip-agent", "limit": 1}
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
            input_payload = job.get('input_payload', {})
            
            youtube_url = input_payload.get('url') or input_payload.get('youtube_url')
            start_sec = input_payload.get('start', 0)
            end_sec = input_payload.get('end', 30)
            
            if not youtube_url:
                raise Exception("No YouTube URL in job payload")
            
            logger.info(f"Processing job {job_id}: {youtube_url} [{start_sec}-{end_sec}]")
            
            # Claim the job
            claim_response = requests.post(
                f"{ORCHESTRATOR_URL}/jobs/{job_id}/claim",
                params={"worker_id": worker_id}
            )
            
            if claim_response.status_code != 200:
                logger.warning(f"Failed to claim job {job_id}: {claim_response.text}")
                continue
            
            # Update clip status to downloading
            clip_id = input_payload.get('clip_id')
            if clip_id:
                supabase.table('clips').update({
                    "status": "downloading"
                }).eq('id', clip_id).execute()
            
            # Download full video
            video_file = download_youtube_video(youtube_url, ASSETS_DIR)
            
            # Extract segment
            segment_filename = f"segment_{job_id}_{start_sec}_{end_sec}.mp4"
            segment_path = ASSETS_DIR / segment_filename
            
            extract_segment(video_file, segment_path, start_sec, end_sec)
            
            # Clean up full video (keep segment)
            try:
                video_file.unlink()
                logger.info(f"Cleaned up full video: {video_file}")
            except Exception as e:
                logger.warning(f"Failed to clean up: {e}")
            
            # Update clip record
            if clip_id:
                supabase.table('clips').update({
                    "status": "extracted",
                    "local_path": str(segment_path)
                }).eq('id', clip_id).execute()
            
            # Mark job complete
            complete_response = requests.post(
                f"{ORCHESTRATOR_URL}/jobs/{job_id}/complete",
                json={
                    "output": {
                        "segment_path": str(segment_path),
                        "duration": end_sec - start_sec,
                        "resolution": "1080x1920"
                    }
                }
            )
            
            logger.info(f"Job {job_id} completed successfully")
            
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

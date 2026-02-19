"""
Editor Worker v3 - Professional Video Rendering
Studio-quality output with cinematic color grading, smooth transitions, and professional graphics
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

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:8000")
ASSETS_DIR = Path("/assets")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_cinematic_ken_burns(image_path: Path, output_path: Path, duration: int):
    """
    Cinematic Ken Burns effect with smooth zoom and pan
    Professional easing for documentary feel
    """
    logger.info(f"Creating cinematic Ken Burns: {image_path.name}")
    
    frames = duration * 25
    
    # Smooth zoom out with subtle pan
    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-vf",
        f"zoompan=z='if(lte(on,1),1.3,max(1.0,zoom-0.001))':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)+sin(on/100)*30':"
        f"d={frames}:s=1080x1920",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",  # High quality
        "-t", str(duration),
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Ken Burns failed: {result.stderr}")
        return None
    
    logger.info(f"Ken Burns created: {output_path}")
    return output_path

def apply_cinematic_color_grade(input_path: Path, output_path: Path):
    """
    Professional color grading
    Increases contrast, saturation, adds cinematic warmth
    """
    logger.info(f"Applying color grade: {input_path.name}")
    
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-vf",
        "eq=contrast=1.15:saturation=1.1:brightness=0.02,"
        "curves=r='0/0 0.5/0.45 1/1':g='0/0 0.5/0.48 1/1':b='0/0 0.5/0.52 1/1'",
        "-c:v", "libx264",
        "-preset", "slow",  # Better compression
        "-crf", "18",  # High quality
        "-c:a", "copy",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Color grade failed: {result.stderr}")
        import shutil
        shutil.copy(input_path, output_path)
        return output_path
    
    logger.info(f"Color graded: {output_path}")
    return output_path

def add_professional_lower_third(input_path: Path, output_path: Path, text: str):
    """
    Professional lower third with animated background bar
    Modern design with subtle shadows and clean typography
    """
    logger.info(f"Adding lower third: {text[:40]}...")
    
    # Write text to temp file
    text_file = ASSETS_DIR / "renders" / f"lt_text_{datetime.now().strftime('%s')}.txt"
    
    # Smart text wrapping
    words = text.split()
    if len(text) > 80:
        mid = len(words) // 2
        line1 = ' '.join(words[:mid])
        line2 = ' '.join(words[mid:])
        text_file.write_text(f"{line1}\n{line2}")
        two_lines = True
    else:
        text_file.write_text(text)
        two_lines = False
    
    if two_lines:
        # Two-line professional lower third
        vf = (
            "format=yuv420p,"
            "drawbox=y=ih-h+60:color=black@0.75:width=iw:height=140:t=fill,"
            f"drawtext=textfile='{text_file}':fontcolor=white:fontsize=38:"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
            "x=(w-text_w)/2:y=h-180:shadowcolor=black@0.9:shadowx=3:shadowy=3:"
            "line_spacing=15:boxborderw=10"
        )
    else:
        # Single line
        vf = (
            "format=yuv420p,"
            "drawbox=y=ih-h+80:color=black@0.75:width=iw:height=100:t=fill,"
            f"drawtext=textfile='{text_file}':fontcolor=white:fontsize=42:"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
            "x=(w-text_w)/2:y=h-160:shadowcolor=black@0.9:shadowx=3:shadowy=3"
        )
    
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "copy",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    try:
        text_file.unlink()
    except:
        pass
    
    if result.returncode != 0:
        logger.error(f"Lower third failed: {result.stderr}")
        import shutil
        shutil.copy(input_path, output_path)
    else:
        logger.info(f"Lower third added: {output_path}")
    
    return output_path

def create_crossfade_transition(clip1: Path, clip2: Path, output_path: Path, fade_duration: float = 0.8):
    """
    Smooth crossfade transition between clips
    Professional 0.8s fade for documentary feel
    """
    logger.info(f"Creating crossfade transition")
    
    # Get duration of first clip
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(clip1)],
        capture_output=True, text=True
    )
    duration1 = float(probe.stdout.strip())
    
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(clip1),
        "-i", str(clip2),
        "-filter_complex",
        f"[0:v][1:v]xfade=transition=fade:duration={fade_duration}:offset={duration1 - fade_duration}[v];"
        f"[0:a][1:a]acrossfade=d={fade_duration}[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"Crossfade failed: {result.stderr}")
        # Fallback: simple concat
        concat_file = ASSETS_DIR / "renders" / "temp_concat.txt"
        concat_file.write_text(f"file '{clip1}'\nfile '{clip2}'")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_file), "-c", "copy", str(output_path)
        ], capture_output=True)
        concat_file.unlink()
    else:
        logger.info(f"Crossfade created: {output_path}")
    
    return output_path

def render_video_professional(project_id: str, script: dict, clips: list, output_path: Path) -> Path:
    """
    Professional video rendering pipeline
    Studio-quality output with cinematic effects
    """
    logger.info(f"PROFESSIONAL RENDER: Project {project_id}")
    
    if not script:
        raise Exception("No script content")
    
    segments = script.get('segments', [])
    if not segments:
        raise Exception("No segments")
    
    # Build clip lookup
    clip_lookup = {}
    for clip in clips:
        if clip.get('status') == 'extracted':
            clip_lookup[clip.get('label', '')] = clip.get('local_path')
    
    logger.info(f"Assets: {list(clip_lookup.keys())}")
    
    # Process each segment
    processed_clips = []
    temp_files = []
    
    for i, seg in enumerate(segments):
        visual = seg.get('visual', '')
        text = seg.get('text', '')
        duration = seg['end'] - seg['start']
        
        logger.info(f"Segment {i}: {visual} ({duration}s)")
        
        clip_path = clip_lookup.get(visual)
        
        # Create base video
        if not clip_path:
            base_path = ASSETS_DIR / "renders" / f"black_{i}.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi",
                "-i", f"color=c=black:s=1080x1920:d={duration}",
                "-c:v", "libx264", str(base_path)
            ], capture_output=True)
            clip_path = str(base_path)
            temp_files.append(base_path)
        elif str(clip_path).lower().endswith(('.jpg', '.jpeg', '.png')):
            kb_path = ASSETS_DIR / "renders" / f"kb_{i}.mp4"
            create_cinematic_ken_burns(Path(clip_path), kb_path, duration)
            clip_path = str(kb_path)
            temp_files.append(kb_path)
        
        # Apply color grade
        graded_path = ASSETS_DIR / "renders" / f"graded_{i}.mp4"
        apply_cinematic_color_grade(Path(clip_path), graded_path)
        temp_files.append(graded_path)
        
        # Add lower third if text exists
        if text:
            final_path = ASSETS_DIR / "renders" / f"final_{i}.mp4"
            add_professional_lower_third(graded_path, final_path, text)
            temp_files.append(final_path)
            processed_clips.append(final_path)
        else:
            processed_clips.append(graded_path)
    
    # Combine with crossfades
    if len(processed_clips) == 1:
        import shutil
        shutil.copy(processed_clips[0], output_path)
    else:
        # Build progressive crossfade chain
        current = processed_clips[0]
        
        for i in range(1, len(processed_clips)):
            next_clip = processed_clips[i]
            transition_path = ASSETS_DIR / "renders" / f"trans_{i}.mp4"
            create_crossfade_transition(current, next_clip, transition_path)
            temp_files.append(transition_path)
            current = transition_path
        
        import shutil
        shutil.copy(current, output_path)
    
    # Cleanup
    for f in temp_files:
        try:
            if f != output_path:
                f.unlink()
        except:
            pass
    
    logger.info(f"PROFESSIONAL RENDER COMPLETE: {output_path}")
    return output_path

def poll_and_work():
    """Main worker loop"""
    worker_id = f"editor-v3-{os.getpid()}"
    logger.info(f"Editor v3 Professional started: {worker_id}")
    
    (ASSETS_DIR / "renders").mkdir(parents=True, exist_ok=True)
    
    while True:
        try:
            response = requests.get(
                f"{ORCHESTRATOR_URL}/jobs/poll",
                params={"worker_type": "editor", "limit": 1},
                timeout=10
            )
            
            if response.status_code != 200:
                time.sleep(5)
                continue
            
            jobs = response.json()
            if not jobs:
                time.sleep(5)
                continue
            
            job = jobs[0]
            job_id = job['id']
            project_id = job['project_id']
            
            logger.info(f"Processing job {job_id}")
            
            # Claim
            requests.post(
                f"{ORCHESTRATOR_URL}/jobs/{job_id}/claim",
                params={"worker_id": worker_id},
                timeout=10
            )
            
            # Get data
            project = supabase.table('projects').select('*').eq('id', project_id).single().execute()
            script = project.data.get('script_content', {}) if project.data else {}
            
            clips_result = supabase.table('clips').select('*').eq('project_id', project_id).execute()
            clips = clips_result.data if clips_result.data else []
            
            # Render
            output_filename = f"evo_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_PRO.mp4"
            output_path = ASSETS_DIR / "renders" / output_filename
            
            render_video_professional(project_id, script, clips, output_path)
            
            # Get video stats
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
                 "-of", "default=noprint_wrappers=1", str(output_path)],
                capture_output=True, text=True
            )
            logger.info(f"Output stats: {probe.stdout}")
            
            # Complete
            requests.post(
                f"{ORCHESTRATOR_URL}/jobs/{job_id}/complete",
                json={"output": {"video_url": str(output_path), "filename": output_filename}},
                params={"next_status": "done"},
                timeout=10
            )
            
            logger.info(f"RENDER COMPLETE: {output_filename}")
            
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    poll_and_work()

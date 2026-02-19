"""
Prudentia Test Reel - Focused Video Pipeline
Testing: slides, transitions, Ken Burns, overlays
"""
import os
import subprocess
from pathlib import Path
from datetime import datetime

ASSETS_DIR = Path("/home/evo/projects/Evolution-Content-Factory/assets")
PRUDENTIA_DIR = ASSETS_DIR / "prudentia"
EVO_LOGO = Path("/home/evo/projects/Evolution-3.1/public/images/Evolution-Stables-Logo-White.png")
OUTPUT_DIR = ASSETS_DIR / "renders"

def create_slide_with_ken_burns(image_path: Path, output_path: Path, duration: int, text: str = None):
    """Create a slide with cinematic Ken Burns effect"""
    frames = duration * 30  # 30fps
    
    # Smooth zoom out from 1.3x to 1.0x with subtle pan
    vf = (
        f"zoompan=z='if(lte(on,1),1.3,max(1.0,zoom-0.002))':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920"
    )
    
    if text:
        # Add text overlay with shadow
        vf += f",drawtext=text='{text}':fontcolor=white:fontsize=48:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=h-200:shadowcolor=black@0.8:shadowx=4:shadowy=4"
    
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", "-t", str(duration),
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def create_evolution_intro(output_path: Path, duration: int = 3):
    """Opening slide: Evolution Stables powered by Tokinvest"""
    # Create black background with text
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"color=c=black:s=1080x1920:d={duration}",
        "-vf", (
            "drawtext=text='Evolution Stables':fontcolor=#D4AF37:fontsize=64:"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=h/2-100,"
            "drawtext=text='Powered by Tokinvest':fontcolor=white:fontsize=36:"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=h/2+20,"
            "drawtext=text='Presents...':fontcolor=white:fontsize=48:"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=h/2+100"
        ),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", "-t", str(duration),
        str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def extract_race_clip_with_overlay(input_path: Path, output_path: Path, start_time: str, duration: int, race_info: dict = None):
    """Extract race segment with full-width video and info overlays in black bars"""
    
    # Build complex filter for video + overlays
    # Race video: full width 1080px, scaled to fit, padded to 1080x1920
    # Black bars: ~657px above, ~657px below (total 1314px black space)
    
    vf_parts = [
        "scale=1080:-1",  # Scale to width 1080, keep aspect ratio
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black"  # Pad to vertical 9:16
    ]
    
    # Add race info overlays if provided
    if race_info:
        # Top bar - Race name and details
        race_name = race_info.get('name', 'TAURANGA MAIDEN')
        race_date = race_info.get('date', '28 May 2025')
        distance = race_info.get('distance', '1400m')
        
        vf_parts.append(
            f"drawbox=y=0:color=black@0.85:width=iw:height=130:t=fill,"
            f"drawtext=text='{race_name}':fontcolor=#D4AF37:fontsize=42:"
            f"fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=30,"
            f"drawtext=text='{race_date} | {distance}':fontcolor=white:fontsize=28:"
            f"fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=80"
        )
        
        # Bottom bar - Result info
        result = race_info.get('result', '1st Place')
        time = race_info.get('time', '1:24.50')
        margin = race_info.get('margin', '1.5 lengths')
        
        vf_parts.append(
            f"drawbox=y=ih-180:color=black@0.85:width=iw:height=180:t=fill,"
            f"drawtext=text='{result}':fontcolor=#D4AF37:fontsize=48:"
            f"fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=h-160,"
            f"drawtext=text='Time: {time} | Margin: {margin}':fontcolor=white:fontsize=28:"
            f"fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=h-100"
        )
    
    vf = ','.join(vf_parts)
    
    cmd = [
        "ffmpeg", "-y", "-ss", start_time, "-t", str(duration),
        "-i", str(input_path),
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18",
        str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def create_pedigree_slide(horse_img: Path, sire_img: Path, dam_img: Path, output_path: Path, duration: int = 8):
    """Create pedigree infographic with family tree"""
    # For now, create a composite layout
    # Full implementation would use ImageMagick for complex layouts
    
    # Placeholder: use horse image with text overlay for pedigree info
    vf = (
        f"zoompan=z='1.1':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={duration*30}:s=1080x1920,"
        "drawbox=y=100:color=black@0.7:width=iw:height=400:t=fill,"
        "drawtext=text='Prudentia':fontcolor=#D4AF37:fontsize=56:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=150,"
        "drawtext=text='4yo Filly':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=230,"
        "drawtext=text='Sire: Proisir':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=300,"
        "drawtext=text='Dam: Little Bit Irish':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=350,"
        "drawtext=text='Trained at Wexford Stables':fontcolor=#D4AF37:fontsize=28:x=(w-text_w)/2:y=420"
    )
    
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(horse_img),
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", "-t", str(duration),
        str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def create_cta_slide(output_path: Path, duration: int = 5):
    """Call to action slide"""
    hero_img = PRUDENTIA_DIR / "Prudentia-13Feb2026-003.JPG"
    
    vf = (
        f"zoompan=z='1.15':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={duration*30}:s=1080x1920,"
        "drawbox=y=ih-300:color=black@0.75:width=iw:height=250:t=fill,"
        "drawtext=text='Listing 24 February':fontcolor=#D4AF37:fontsize=48:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=h-250,"
        "drawtext=text='Are you ready to race?':fontcolor=white:fontsize=42:x=(w-text_w)/2:y=h-180"
    )
    
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(hero_img),
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", "-t", str(duration),
        str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def crossfade_transition(clip1: Path, clip2: Path, output_path: Path, fade_duration: float = 0.8):
    """Create smooth crossfade between two clips"""
    # Get duration of first clip
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(clip1)],
        capture_output=True, text=True
    )
    duration1 = float(probe.stdout.strip())
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(clip1), "-i", str(clip2),
        "-filter_complex",
        f"[0:v][1:v]xfade=transition=fade:duration={fade_duration}:offset={duration1 - fade_duration}[v]",
        "-map", "[v]",
        "-c:v", "libx264", "-crf", "18",
        str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def assemble_reel():
    """Main assembly function"""
    print("🎬 Building Prudentia Test Reel...")
    
    temp_dir = OUTPUT_DIR / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    segments = []
    
    # Scene 1: Opening (3s)
    print("Creating opening...")
    intro = temp_dir / "01_intro.mp4"
    if create_evolution_intro(intro, 3):
        segments.append(intro)
    
    # Scene 2: Prudentia title (4s)
    print("Creating title slide...")
    title = temp_dir / "02_title.mp4"
    if create_slide_with_ken_burns(
        PRUDENTIA_DIR / "Prudentia-13Feb2026-001.JPG",
        title, 4, "Prudentia"
    ):
        segments.append(title)
    
    # Scene 3: Race clip (10s) with info overlays
    print("Extracting race footage with overlays...")
    race = temp_dir / "03_race.mp4"
    race_source = ASSETS_DIR / "clips" / "Prudentia_Race_Tauranga.mp4"
    race_info = {
        'name': 'TAURANGA RACECOURSE MAIDEN',
        'date': '28 May 2025',
        'distance': '1400m',
        'result': '1st Place - Prudentia',
        'time': '1:24.50',
        'margin': '1.5 lengths'
    }
    if race_source.exists():
        if extract_race_clip_with_overlay(race_source, race, "00:01:10", 10, race_info):
            segments.append(race)
    
    # Scene 4: Pedigree info (8s)
    print("Creating pedigree slide...")
    pedigree = temp_dir / "04_pedigree.mp4"
    # Note: Using horse image as placeholder - would integrate sire/dam images in full version
    if create_pedigree_slide(
        PRUDENTIA_DIR / "Prudentia-13Feb2026-002.JPG",
        None, None, pedigree, 8
    ):
        segments.append(pedigree)
    
    # Scene 5: CTA (5s)
    print("Creating CTA...")
    cta = temp_dir / "05_cta.mp4"
    if create_cta_slide(cta, 5):
        segments.append(cta)
    
    # Concatenate with crossfades
    print(f"Assembling {len(segments)} segments...")
    
    if len(segments) == 0:
        print("❌ No segments created")
        return
    
    if len(segments) == 1:
        final_output = OUTPUT_DIR / f"Prudentia_TestReel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        import shutil
        shutil.copy(segments[0], final_output)
        print(f"✅ Output: {final_output}")
        return
    
    # Progressive crossfade
    current = segments[0]
    for i in range(1, len(segments)):
        next_segment = segments[i]
        transition_output = temp_dir / f"trans_{i}.mp4"
        print(f"Crossfade {i}...")
        if crossfade_transition(current, next_segment, transition_output):
            current = transition_output
        else:
            print(f"⚠️ Crossfade failed, using hard cut")
            current = next_segment
    
    # Final output
    final_output = OUTPUT_DIR / f"Prudentia_TestReel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    import shutil
    shutil.copy(current, final_output)
    
    print(f"✅ Render complete: {final_output}")
    
    # Cleanup temp files
    for f in temp_dir.iterdir():
        f.unlink()
    temp_dir.rmdir()

if __name__ == "__main__":
    assemble_reel()

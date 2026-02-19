#!/usr/bin/env python3
"""
AI Slide Generator for Evolution Content Factory
Uses Gemini API to generate slide images from text prompts
Then animates with FFmpeg Ken Burns effect

Smarter approach: AI generates visuals, FFmpeg animates, no manual design needed
"""

import subprocess
import os
import json
from pathlib import Path
import requests

class AISlideGenerator:
    """Generate professional slides using AI + FFmpeg"""
    
    def __init__(self, output_dir="/mnt/s/Evolution-Content-Factory/slides/generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Gemini API key from env
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        
    def generate_slide_image(self, prompt, output_name):
        """
        Use Gemini to generate slide image from text prompt
        Fallback: Use ImageMagick to create styled slide
        """
        # For now, use ImageMagick with AI-enhanced styling
        # In production: Call Gemini Imagen API
        
        output_path = self.output_dir / f"{output_name}.png"
        
        # Create styled slide with ImageMagick
        cmd = f"""
        convert -size 1080x1920 xc:'#0A0A0A' \
          -pointsize 48 -fill '#D4AF37' -gravity center \
          -font DejaVu-Sans-Bold \
          -annotate +0+0 '{prompt}' \
          -stroke '#D4AF37' -strokewidth 2 \
          -draw "line 340,960 740,960" \
          {output_path}
        """
        
        subprocess.run(cmd, shell=True, capture_output=True)
        return output_path
    
    def animate_ken_burns(self, image_path, output_name, duration=5):
        """
        Apply Ken Burns effect to static image
        Returns video file
        """
        output_path = self.output_dir / f"{output_name}.mp4"
        
        # Calculate frames
        fps = 30
        total_frames = duration * fps
        
        # Ken Burns: zoom from 1.2 to 1.0, subtle pan
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
            "-vf",
            f"zoompan=z='if(lte(on,1),1.2,max(1.0,zoom-0.004))':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1080x1920",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
            "-t", str(duration),
            str(output_path)
        ]
        
        subprocess.run(cmd, capture_output=True)
        return output_path
    
    def create_slide(self, slide_type, content, duration=5):
        """
        Smart slide creation - combines AI image gen + animation
        
        Args:
            slide_type: 'opening', 'pedigree', 'result', 'cta'
            content: dict with slide data
            duration: seconds
        """
        
        # Build prompt from content
        prompts = {
            "opening": f"Evolution Stables\\nPowered by Tokinvest\\nPresents",
            "pedigree": f"{content.get('horse', 'Horse')}\\nBy {content.get('sire', 'Sire')}\\nOut of {content.get('dam', 'Dam')}",
            "result": f"{content.get('position', '1st')} Place\\n{content.get('race', 'Race Name')}",
            "cta": f"{content.get('action', 'Action')}\\n{content.get('question', 'Are you ready?')}"
        }
        
        prompt = prompts.get(slide_type, "Evolution Stables")
        
        # Generate image
        image_path = self.generate_slide_image(prompt, f"{slide_type}_static")
        
        # Animate
        video_path = self.animate_ken_burns(image_path, slide_type, duration)
        
        return {
            "type": slide_type,
            "image": str(image_path),
            "video": str(video_path),
            "duration": duration
        }

class DynamicOverlayGenerator:
    """Generate overlays dynamically from data"""
    
    def __init__(self, output_dir="/mnt/s/Evolution-Content-Factory/overlays/generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_calendar(self, date_str, venue, style="gold"):
        """Generate calendar overlay from date"""
        # Parse date
        parts = date_str.split()
        day = parts[0] if len(parts) > 0 else "15"
        month = parts[1] if len(parts) > 1 else "MAR"
        
        output_path = self.output_dir / f"calendar_{day}_{month}.mp4"
        
        # Generate with FFmpeg
        cmd = f"""
        ffmpeg -y -f lavfi -i "color=c=black@0:s=400x300:d=4" -vf "
        drawbox=x=0:y=0:color=#D4AF37:width=400:height=60:t=fill,
        drawtext=text='RACE DAY':fontcolor=black:fontsize=32:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=15,
        drawtext=text='{day}':fontcolor=white:fontsize=72:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=80,
        drawtext=text='{month}':fontcolor=#D4AF37:fontsize=36:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=170,
        drawtext=text='{venue}':fontcolor=white:fontsize=28:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=230,
        fade=in:0:30,fade=out:90:30
        " -c:v libx264 -pix_fmt yuv420p -crf 18 -t 4 {output_path}
        """
        
        subprocess.run(cmd, shell=True, capture_output=True)
        return output_path
    
    def create_position_badge(self, position, style="gold"):
        """Generate 1st/2nd/3rd badge"""
        colors = {"1st": "#D4AF37", "2nd": "#C0C0C0", "3rd": "#CD7F32"}
        color = colors.get(position, "#D4AF37")
        
        output_path = self.output_dir / f"badge_{position}.mp4"
        
        cmd = f"""
        ffmpeg -y -f lavfi -i "color=c={color}:s=200x200:d=3" -vf "
        drawtext=text='{position}':fontcolor=black:fontsize=80:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=(h-text_h)/2,
        zoompan=z='1.0':d=90,
        fade=in:0:15,fade=out:60:15
        " -c:v libx264 -pix_fmt yuv420p -crf 18 -t 3 {output_path}
        """
        
        subprocess.run(cmd, shell=True, capture_output=True)
        return output_path

if __name__ == "__main__":
    # Demo usage
    print("🎨 AI Slide Generator Demo")
    
    # Initialize
    slide_gen = AISlideGenerator()
    overlay_gen = DynamicOverlayGenerator()
    
    # Generate slides
    slides = []
    
    print("1. Creating opening slide...")
    opening = slide_gen.create_slide("opening", {}, duration=4)
    slides.append(opening)
    
    print("2. Creating pedigree slide...")
    pedigree = slide_gen.create_slide("pedigree", {
        "horse": "Prudentia",
        "sire": "Proisir",
        "dam": "Little Bit Irish"
    }, duration=6)
    slides.append(pedigree)
    
    print("3. Creating result slide...")
    result = slide_gen.create_slide("result", {
        "position": "1st",
        "race": "Tauranga Maiden"
    }, duration=5)
    slides.append(result)
    
    print("4. Creating calendar overlay...")
    calendar = overlay_gen.create_calendar("15 MAR", "Ellerslie")
    
    print("5. Creating position badge...")
    badge = overlay_gen.create_position_badge("1st")
    
    print("\n✅ Generated:")
    for slide in slides:
        print(f"  - {slide['type']}: {slide['video']}")
    print(f"  - Calendar: {calendar}")
    print(f"  - Badge: {badge}")

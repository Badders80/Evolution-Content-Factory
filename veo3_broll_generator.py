#!/usr/bin/env python3
"""
Veo 3 / FLOW B-Roll Generator
Generates AI video B-roll from text prompts
Uses Google Veo 3 (via GLM API) or FLOW API
"""

import os
import requests
import json
import time
from pathlib import Path

class BrollGenerator:
    """Generate B-roll footage using AI video models"""
    
    def __init__(self, output_dir="/mnt/s/Evolution-Content-Factory/assets/b-roll/ai_generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # API keys
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        # GLM API for Veo 3 access (you mentioned you have credits)
        self.glm_key = os.getenv("GLM_API_KEY", "")  # Or use existing Gemini key
        
    def generate_veo3(self, prompt, duration=8, aspect_ratio="9:16"):
        """
        Generate video using Veo 3 via GLM API
        Duration: 5-8 seconds (Veo 3 limit)
        Aspect ratio: 9:16 for vertical reels
        """
        print(f"🎬 Generating Veo 3 B-roll...")
        print(f"Prompt: {prompt[:80]}...")
        
        # TODO: Implement actual Veo 3 API call
        # For now, return metadata for manual generation
        
        metadata = {
            "model": "veo-3",
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "status": "ready_to_generate",
            "estimated_cost": "1 credit",
            "output_file": str(self.output_dir / f"veo3_{int(time.time())}.mp4")
        }
        
        # Save prompt for manual submission
        prompt_file = self.output_dir / f"prompt_{int(time.time())}.json"
        with open(prompt_file, "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Prompt saved: {prompt_file}")
        print(f"   Submit to Veo 3: https://aistudio.google.com/app/apps/drive/...")
        
        return metadata
    
    def generate_flow(self, prompt, style="heritage"):
        """
        Generate using FLOW (racing-specific)
        You mentioned 3 videos/day limit
        """
        print(f"🎬 Generating FLOW B-roll...")
        
        metadata = {
            "model": "flow",
            "prompt": prompt,
            "style": style,
            "status": "ready_to_generate",
            "daily_limit": "3 videos",
            "output_file": str(self.output_dir / f"flow_{int(time.time())}.mp4")
        }
        
        prompt_file = self.output_dir / f"flow_prompt_{int(time.time())}.json"
        with open(prompt_file, "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Prompt saved: {prompt_file}")
        return metadata
    
    def batch_generate(self, prompts_list, model="veo3"):
        """Generate multiple B-roll clips from prompt list"""
        results = []
        
        for i, prompt_data in enumerate(prompts_list, 1):
            print(f"\n[{i}/{len(prompts_list)}]")
            
            if model == "veo3":
                result = self.generate_veo3(
                    prompt_data["prompt"],
                    prompt_data.get("duration", 8)
                )
            elif model == "flow":
                result = self.generate_flow(
                    prompt_data["prompt"],
                    prompt_data.get("style", "heritage")
                )
            
            results.append(result)
            
            # Rate limiting
            if i < len(prompts_list):
                print("   Waiting 2s...")
                time.sleep(2)
        
        return results

# Heritage B-roll prompts optimized for Evolution brand
HERITAGE_BROLL_PROMPTS = [
    {
        "id": "morning_training_1",
        "prompt": "Cinematic slow-motion shot of a thoroughbred racehorse galloping through morning mist on a training track, golden hour sunlight filtering through, steam rising from the horse's coat, heritage film grain aesthetic, traditional racing atmosphere, professional cinematography",
        "duration": 8,
        "category": "training"
    },
    {
        "id": "parade_ring_1", 
        "prompt": "Elegant shot of a thoroughbred horse being led in the parade ring before a race, formal racing silks, handlers in traditional attire, morning light, heritage racing pageantry, cinematic composition",
        "duration": 6,
        "category": "pageantry"
    },
    {
        "id": "country_course_1",
        "prompt": "Wide establishing shot of horses galloping on a country racecourse at dawn, atmospheric morning mist, rolling hills in background, heritage racing venue, cinematic wide angle, film grain",
        "duration": 8,
        "category": "galloping"
    },
    {
        "id": "stable_life_1",
        "prompt": "Intimate shot of a trainer grooming a thoroughbred in the stables, warm stable lighting, steam rising from the horse after exercise, authentic behind-the-scenes racing life, heritage documentary style",
        "duration": 7,
        "category": "behind_scenes"
    },
    {
        "id": "barrier_loading_1",
        "prompt": "Tense dramatic shot of horses loading into starting barriers, dust in the air, anticipation building, morning light creating lens flare, heritage racing cinematography, slow motion",
        "duration": 6,
        "category": "barriers"
    },
    {
        "id": "finish_line_1",
        "prompt": "Dramatic slow-motion finish line crossing, thoroughbred in full stride, determination and power, heritage racing photography style, dust flying, cinematic lighting",
        "duration": 5,
        "category": "finishes"
    }
]

if __name__ == "__main__":
    import sys
    
    generator = BrollGenerator()
    
    print("🎬 Evolution B-Roll Generator")
    print("="*50)
    print(f"Model: Veo 3 (Google) or FLOW")
    print(f"Daily limit: 3 videos (your credits)")
    print(f"Style: Heritage/Traditional (relaxed)")
    print("")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--generate":
        # Generate all prompts as JSON files for manual submission
        print(f"Preparing {len(HERITAGE_BROLL_PROMPTS)} B-roll prompts...")
        
        for prompt_data in HERITAGE_BROLL_PROMPTS:
            result = generator.generate_veo3(
                prompt_data["prompt"],
                prompt_data["duration"]
            )
        
        print(f"\n✅ {len(HERITAGE_BROLL_PROMPTS)} prompts ready!")
        print(f"Location: {generator.output_dir}")
        print("\nNext steps:")
        print("1. Review prompt JSON files")
        print("2. Submit to Veo 3: https://aistudio.google.com")
        print("3. Download generated videos to ai_generated/ folder")
        print("4. Run: python smart_asset_library.py to index")
        
    else:
        print("Usage: python veo3_broll_generator.py --generate")
        print("")
        print("Sample prompts available:")
        for p in HERITAGE_BROLL_PROMPTS:
            print(f"  - {p['id']}: {p['category']} ({p['duration']}s)")

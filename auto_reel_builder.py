#!/usr/bin/env python3
"""
Auto-Reel Builder for Evolution Content Factory
Takes horse name + race ID, outputs complete professional reel

Smart workflow:
1. Fetch race data from Research Engine
2. Search Asset Library for relevant footage
3. Generate slides with AI Slide Generator
4. Create dynamic overlays from race data
5. Assemble with B-roll and transitions
6. Output final reel

Usage: python auto_reel_builder.py --horse Prudentia --race tauranga_maiden
"""

import argparse
import json
import subprocess
from pathlib import Path
from datetime import datetime

class AutoReelBuilder:
    """Build complete reels automatically"""
    
    def __init__(self, base_path="/mnt/s/Evolution-Content-Factory"):
        self.base_path = Path(base_path)
        self.output_dir = self.base_path / "renders" / "auto"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Import smart components
        import sys
        sys.path.insert(0, str(self.base_path))
        from ai_slide_generator import AISlideGenerator, DynamicOverlayGenerator
        from smart_asset_library import SmartAssetLibrary
        
        self.slide_gen = AISlideGenerator()
        self.overlay_gen = DynamicOverlayGenerator()
        self.asset_lib = SmartAssetLibrary()
    
    def fetch_race_data(self, horse_name, race_id):
        """
        Fetch race data from Research Engine API
        For now: mock data (in production: call Research Engine)
        """
        return {
            "horse": horse_name,
            "race_name": "TAURANGA RACECOURSE MAIDEN",
            "date": "28 May 2025",
            "distance": "1400m",
            "position": "1st",
            "time": "1:24.50",
            "margin": "1.5 lengths",
            "trainer": "Wexford Stables",
            "sire": "Proisir",
            "dam": "Little Bit Irish",
            "next_race": "Ellerslie, March 15 2026"
        }
    
    def find_assets(self, horse_name, style="heritage"):
        """Find relevant assets for the reel"""
        print(f"🔍 Finding assets for {horse_name}...")
        
        assets = {
            "photos": [],
            "videos": [],
            "broll": []
        }
        
        # Search asset library
        photos = self.asset_lib.query(f"{horse_name} photo")
        videos = self.asset_lib.query(f"{horse_name} video")
        broll = self.asset_lib.query(f"{style} b-roll")
        
        # Get first match of each type
        if photos:
            assets["photos"] = [p for p in photos if p["type"] == "photo"][:3]
        if videos:
            assets["videos"] = [v for v in videos if v["type"] == "video"][:2]
        if broll:
            assets["broll"] = broll[:2]
        
        print(f"  Found: {len(assets['photos'])} photos, {len(assets['videos'])} videos, {len(assets['broll'])} b-roll prompts")
        return assets
    
    def build_scene_list(self, race_data, assets):
        """Generate scene list for the reel"""
        scenes = [
            {
                "type": "opening",
                "duration": 4,
                "data": {},
                "generated": True
            },
            {
                "type": "horse_intro",
                "duration": 5,
                "data": {
                    "horse": race_data["horse"],
                    "photo": assets["photos"][0]["path"] if assets["photos"] else None
                },
                "generated": False
            },
            {
                "type": "pedigree",
                "duration": 6,
                "data": {
                    "horse": race_data["horse"],
                    "sire": race_data["sire"],
                    "dam": race_data["dam"]
                },
                "generated": True
            },
            {
                "type": "race_result",
                "duration": 5,
                "data": {
                    "position": race_data["position"],
                    "race": race_data["race_name"],
                    "video": assets["videos"][0]["path"] if assets["videos"] else None
                },
                "generated": False
            },
            {
                "type": "calendar",
                "duration": 3,
                "data": {
                    "date": race_data["next_race"]
                },
                "generated": True
            },
            {
                "type": "cta",
                "duration": 5,
                "data": {
                    "horse": race_data["horse"]
                },
                "generated": True
            }
        ]
        return scenes
    
    def generate_slides(self, scenes):
        """Generate all AI slides for scenes"""
        print("\n🎨 Generating slides...")
        
        generated = []
        for scene in scenes:
            if scene.get("generated"):
                print(f"  Creating {scene['type']} slide...")
                
                # Map scene types to slide generator
                slide_type_map = {
                    "opening": "opening",
                    "pedigree": "pedigree",
                    "race_result": "result",
                    "calendar": "calendar",
                    "cta": "cta"
                }
                
                slide_type = slide_type_map.get(scene["type"], "opening")
                result = self.slide_gen.create_slide(
                    slide_type,
                    scene["data"],
                    scene["duration"]
                )
                generated.append(result)
        
        return generated
    
    def assemble_reel(self, scenes, slides, output_name):
        """Assemble final reel with crossfades"""
        print(f"\n🎬 Assembling reel: {output_name}")
        
        output_path = self.output_dir / f"{output_name}.mp4"
        
        # Collect all video files in order
        video_files = []
        current_time = 0
        
        for scene in scenes:
            # Find matching slide
            matching = [s for s in slides if s["type"] in scene["type"]]
            if matching:
                video_files.append(matching[0]["video"])
            elif scene["type"] == "horse_intro" and scene["data"].get("photo"):
                # Would generate from photo
                pass
            elif scene["type"] == "race_result" and scene["data"].get("video"):
                # Would use race video
                pass
        
        print(f"  Assembly: {len(video_files)} scenes")
        print(f"  Output: {output_path}")
        
        # For now: return manifest (actual assembly would use FFmpeg concat)
        return {
            "output": str(output_path),
            "scenes": len(video_files),
            "video_files": video_files,
            "status": "ready_to_render"
        }
    
    def build(self, horse_name, race_id, style="heritage"):
        """Main build workflow"""
        print(f"\n🎬 Auto-Reel Builder")
        print(f"Horse: {horse_name}")
        print(f"Race: {race_id}")
        print(f"Style: {style}")
        print("="*50)
        
        # Step 1: Fetch data
        race_data = self.fetch_race_data(horse_name, race_id)
        
        # Step 2: Find assets
        assets = self.find_assets(horse_name, style)
        
        # Step 3: Build scene list
        scenes = self.build_scene_list(race_data, assets)
        print(f"\n📋 Scene list: {len(scenes)} scenes")
        for i, scene in enumerate(scenes, 1):
            print(f"  {i}. {scene['type']} ({scene['duration']}s)")
        
        # Step 4: Generate slides
        slides = self.generate_slides(scenes)
        
        # Step 5: Assemble
        output_name = f"{horse_name}_{race_id}_{datetime.now().strftime('%Y%m%d')}"
        result = self.assemble_reel(scenes, slides, output_name)
        
        # Save manifest
        manifest_path = self.output_dir / f"{output_name}_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump({
                "horse": horse_name,
                "race": race_id,
                "style": style,
                "race_data": race_data,
                "scenes": scenes,
                "slides": slides,
                "assembly": result
            }, f, indent=2)
        
        print(f"\n✅ Reel manifest saved: {manifest_path}")
        print(f"Status: {result['status']}")
        
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-build Evolution Stables reels")
    parser.add_argument("--horse", required=True, help="Horse name")
    parser.add_argument("--race", required=True, help="Race ID/name")
    parser.add_argument("--style", default="heritage", choices=["heritage", "hype", "documentary"])
    
    args = parser.parse_args()
    
    builder = AutoReelBuilder()
    result = builder.build(args.horse, args.race, args.style)
    
    print("\n" + "="*50)
    print("Build complete!")
    print(f"Run `bash build_prudentia_reel.sh` to render final video")

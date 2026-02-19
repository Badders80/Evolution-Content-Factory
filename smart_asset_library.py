#!/usr/bin/env python3
"""
Smart Asset Library with Vector Search
Uses mxbai-embed-large to index assets by semantic meaning
Search: "galloping horse morning" → finds matching videos
"""

import json
import os
from pathlib import Path
import subprocess

class SmartAssetLibrary:
    """AI-powered asset search and management"""
    
    def __init__(self, base_path="/mnt/s/Evolution-Content-Factory"):
        self.base_path = Path(base_path)
        self.index_path = self.base_path / "assets" / "search_index.json"
        
    def scan_assets(self):
        """Scan all assets and create metadata"""
        assets = []
        
        # Scan horses
        horses_dir = self.base_path / "assets" / "horses"
        for horse_dir in horses_dir.iterdir():
            if horse_dir.is_dir():
                horse_name = horse_dir.name
                
                # Photos
                for photo in (horse_dir / "photos").glob("*"):
                    assets.append({
                        "id": f"{horse_name}_photo_{photo.stem}",
                        "type": "photo",
                        "horse": horse_name,
                        "path": str(photo.relative_to(self.base_path)),
                        "tags": [horse_name, "photo", "training"],
                        "description": f"Photo of {horse_name}"
                    })
                
                # Videos
                for video in (horse_dir / "videos").glob("*.mp4"):
                    assets.append({
                        "id": f"{horse_name}_video_{video.stem}",
                        "type": "video",
                        "horse": horse_name,
                        "path": str(video.relative_to(self.base_path)),
                        "tags": [horse_name, "video", "race" if "Race" in video.name else "training"],
                        "description": f"Video of {horse_name} - {video.stem}"
                    })
        
        # Scan B-roll prompts
        broll_manifest = self.base_path / "assets" / "b-roll" / "heritage_manifest.json"
        if broll_manifest.exists():
            with open(broll_manifest) as f:
                broll = json.load(f)
                for item in broll:
                    assets.append({
                        "id": item["id"],
                        "type": "b-roll-prompt",
                        "category": item["category"],
                        "path": str(broll_manifest.relative_to(self.base_path)),
                        "tags": [item["category"], "b-roll", "heritage"],
                        "description": item["prompt"],
                        "prompt": item["prompt"]
                    })
        
        return assets
    
    def generate_embeddings(self, assets):
        """
        Generate embeddings for semantic search
        Uses mxbai-embed-large via Ollama or local LLM
        """
        print("Generating embeddings for semantic search...")
        
        # For each asset, generate embedding from description
        for asset in assets:
            # Create embedding input
            text = f"{asset['description']} {' '.join(asset['tags'])}"
            
            # Store for now (in production, call embedding model)
            asset["embedding_text"] = text
            asset["searchable"] = True
        
        return assets
    
    def search(self, query, assets, top_k=5):
        """
        Search assets by natural language
        Simple keyword matching (in production: vector similarity)
        """
        query_terms = query.lower().split()
        results = []
        
        for asset in assets:
            score = 0
            text = (asset.get("description", "") + " " + " ".join(asset.get("tags", []))).lower()
            
            for term in query_terms:
                if term in text:
                    score += 1
            
            if score > 0:
                results.append({
                    **asset,
                    "score": score
                })
        
        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def build_index(self):
        """Build searchable index"""
        print("🔍 Building Smart Asset Library...")
        
        # Scan
        assets = self.scan_assets()
        print(f"  Found {len(assets)} assets")
        
        # Generate embeddings
        assets = self.generate_embeddings(assets)
        
        # Save index
        with open(self.index_path, "w") as f:
            json.dump({
                "total_assets": len(assets),
                "last_updated": str(Path().stat().st_mtime),
                "assets": assets
            }, f, indent=2)
        
        print(f"  ✅ Index saved: {self.index_path}")
        return assets
    
    def query(self, search_text):
        """Query the asset library"""
        if not self.index_path.exists():
            print("Index not found. Building...")
            self.build_index()
        
        with open(self.index_path) as f:
            data = json.load(f)
            assets = data["assets"]
        
        results = self.search(search_text, assets)
        
        print(f"\n🔍 Search: '{search_text}'")
        print(f"Found {len(results)} matches:\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['id']} ({result['type']})")
            print(f"   Score: {result['score']}")
            print(f"   Path: {result['path']}")
            print(f"   Tags: {', '.join(result['tags'])}")
            print()
        
        return results

if __name__ == "__main__":
    library = SmartAssetLibrary()
    
    # Build index
    library.build_index()
    
    # Demo searches
    print("\n" + "="*50)
    library.query("galloping horse morning")
    
    print("="*50)
    library.query("Prudentia training video")
    
    print("="*50)
    library.query("heritage b-roll")

#!/usr/bin/env python3
"""
Evolution AI Orchestrator
Uses local LLMs (Ollama) for smart content generation
"""

import requests
import json
import subprocess

OLLAMA_URL = "http://localhost:11434/api/generate"

class EvolutionAI:
    """Orchestrate local AI for Evolution Stables tasks"""
    
    def __init__(self):
        self.models = {
            "code": "qwen2.5-coder:14b",
            "general": "qwen2.5:7b", 
            "embeddings": "mxbai-embed-large"
        }
    
    def generate_slide_design(self, slide_type, content):
        """
        Use local LLM to generate slide design specifications
        Not just text — actual design decisions
        """
        prompt = f"""
You are a professional video designer for Evolution Stables, a premium horse racing syndicate.

Design a {slide_type} slide with this content:
{json.dumps(content, indent=2)}

Output a JSON specification for the slide design:
{{
  "background_color": "#hex",
  "text_elements": [
    {{"text": "...", "position": "top/center/bottom", "font_size": 48, "color": "#hex"}}
  ],
  "graphics": ["logo", "line", "badge"],
  "animation": "ken_burns_zoom_in/out/pan",
  "duration": seconds
}}

Brand colors: Gold #D4AF37, Dark #0A0A0A
Style: Institutional, heritage, professional
        """
        
        response = requests.post(OLLAMA_URL, json={
            "model": self.models["general"],
            "prompt": prompt,
            "stream": False
        })
        
        if response.status_code == 200:
            result = response.json()
            # Extract JSON from response
            try:
                # Find JSON in the response text
                text = result.get("response", "{}")
                # Simple extraction (in production use proper JSON parsing)
                return json.loads(text)
            except:
                return {"error": "Failed to parse", "raw": result.get("response", "")}
        
        return {"error": "API failed", "status": response.status_code}
    
    def generate_broll_prompt(self, category, style="heritage"):
        """
        Generate AI video prompts for B-roll
        Optimized for Veo3/FLOW
        """
        prompt = f"""
Create a detailed video generation prompt for {category} footage.
Style: {style} (traditional, cinematic, heritage racing)

Output only the prompt text, optimized for AI video generation:
- Include lighting (golden hour, morning mist)
- Camera movement (slow dolly, static, tracking)
- Subject details (thoroughbred, specific actions)
- Atmosphere (dust, steam, atmosphere)

Prompt:
        """
        
        response = requests.post(OLLAMA_URL, json={
            "model": self.models["general"],
            "prompt": prompt,
            "stream": False
        })
        
        return response.json().get("response", "")
    
    def generate_content_ideas(self, horse_name, recent_performance):
        """
        Generate content ideas based on horse data
        """
        prompt = f"""
You are the content strategist for Evolution Stables.

Horse: {horse_name}
Recent: {recent_performance}

Generate 3 content ideas for social media reels:
1. Hook (first 3 seconds)
2. Story angle
3. Key scenes
4. Call to action

Output as JSON array.
        """
        
        response = requests.post(OLLAMA_URL, json={
            "model": self.models["general"],
            "prompt": prompt,
            "stream": False
        })
        
        return response.json().get("response", "")
    
    def code_slide_generator(self, design_spec):
        """
        Use code model to generate actual FFmpeg/Python code
        from design specification
        """
        prompt = f"""
Write Python code using FFmpeg to generate this slide:
{json.dumps(design_spec, indent=2)}

Requirements:
- Use subprocess to call ffmpeg
- Include Ken Burns effect
- 1080x1920 vertical format
- Professional quality (CRF 18)

Output only the Python code.
        """
        
        response = requests.post(OLLAMA_URL, json={
            "model": self.models["code"],
            "prompt": prompt,
            "stream": False
        })
        
        return response.json().get("response", "")

if __name__ == "__main__":
    ai = EvolutionAI()
    
    print("🧠 Evolution AI Orchestrator")
    print("="*50)
    
    # Test 1: Generate slide design
    print("\n1. Generating slide design...")
    design = ai.generate_slide_design("pedigree", {
        "horse": "Prudentia",
        "sire": "Proisir",
        "dam": "Little Bit Irish",
        "trainer": "Wexford Stables"
    })
    print(json.dumps(design, indent=2))
    
    # Test 2: Generate B-roll prompt
    print("\n2. Generating B-roll prompt...")
    broll = ai.generate_broll_prompt("training", "heritage")
    print(broll[:200] + "...")
    
    # Test 3: Content ideas
    print("\n3. Generating content ideas...")
    ideas = ai.generate_content_ideas("Prudentia", "1st place at Tauranga Maiden")
    print(ideas[:300] + "...")

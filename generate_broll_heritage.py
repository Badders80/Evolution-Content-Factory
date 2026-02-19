#!/usr/bin/env python3
"""
Generate heritage-style B-roll descriptions for AI video generation
Veo3 or FLOW prompts for traditional, relaxed horse racing content
"""

BROLL_PROMPTS = {
    "galloping": [
        "Cinematic slow-motion shot of a thoroughbred racehorse galloping through morning mist on a training track, golden hour lighting, heritage film grain, traditional racing aesthetics, 4K",
        "Wide shot of horses galloping on a country racecourse at dawn, atmospheric fog, classic racing heritage feel, muted colors, filmic quality",
        "Slow-motion close-up of horse legs pounding the turf, dirt flying, traditional race photography style, dramatic lighting"
    ],
    "training": [
        "Morning training session at Wexford Stables, horses being led by handlers, steam rising from their coats, heritage documentary style, warm tones",
        "Classic shot of a trainer inspecting a horse in the stables, traditional racing atmosphere, soft natural light",
        "Horses walking the parade ring before a race, formal attire, traditional racing pageantry, heritage film aesthetic"
    ],
    "barriers": [
        "Dramatic shot of horses loading into starting barriers, tension building, traditional race day atmosphere, film grain",
        "Close-up of barrier gates opening, horses exploding out, dust and power, heritage racing cinematography"
    ],
    "finishes": [
        "Slow-motion finish line crossing, photo finish style, heritage racing photography, dramatic lighting",
        "Jockey raising whip in victory, traditional celebration, filmic quality, golden hour"
    ],
    "heritage": [
        "Vintage-style shot of thoroughbreds in a green pasture, heritage bloodstock imagery, classic composition",
        "Black and white style shot of racing silks, traditional patterns, heritage aesthetic",
        "Drone shot of a country racecourse, heritage architecture, traditional racing venue"
    ]
}

def generate_broll_manifest():
    """Create manifest of B-roll shots to generate"""
    manifest = []
    for category, prompts in BROLL_PROMPTS.items():
        for i, prompt in enumerate(prompts):
            manifest.append({
                "id": f"{category}_{i+1}",
                "category": category,
                "prompt": prompt,
                "duration": "5-10 seconds",
                "style": "heritage/traditional",
                "status": "pending_generation"
            })
    return manifest

if __name__ == "__main__":
    import json
    manifest = generate_broll_manifest()
    
    with open("/mnt/s/Evolution-Content-Factory/assets/b-roll/heritage_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Generated {len(manifest)} B-roll prompts")
    print("Categories:", list(BROLL_PROMPTS.keys()))
    print("\nSample prompts:")
    for item in manifest[:3]:
        print(f"  - {item['id']}: {item['prompt'][:60]}...")

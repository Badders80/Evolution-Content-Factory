#!/usr/bin/env python3
"""
Generate slide templates using AI (Gemini/GLM)
Templates for Evolution Stables reels
"""

import subprocess
import os

TEMPLATE_SPECS = {
    "opening": {
        "duration": 4,
        "elements": [
            "Evolution Gold Logo centered",
            "'Powered by Tokinvest' below logo",
            "'Presents' text",
            "Gold accent line"
        ]
    },
    "horse_profile": {
        "duration": 5,
        "elements": [
            "Horse photo with Ken Burns",
            "Horse name (Prudentia)",
            "Key stats (4yo Filly)",
            "Trainer (Wexford Stables)"
        ]
    },
    "pedigree": {
        "duration": 6,
        "elements": [
            "Horse photo background",
            "Sire photo (Proisir) - left",
            "Dam photo (Little Bit Irish) - right",
            "Family tree connecting lines",
            "Horse name and details"
        ]
    },
    "race_result": {
        "duration": 4,
        "elements": [
            "Race footage or photo",
            "Position badge (1st/2nd/3rd)",
            "Race name",
            "Date and distance"
        ]
    },
    "calendar": {
        "duration": 3,
        "elements": [
            "Calendar graphic",
            "Race date",
            "Venue",
            "Countdown or 'Upcoming'"
        ]
    },
    "location": {
        "duration": 3,
        "elements": [
            "NZ map outline",
            "Track location marker",
            "Track name",
            "Region"
        ]
    },
    "cta": {
        "duration": 5,
        "elements": [
            "Hero horse shot",
            "Listing/Action text",
            "Question or hook",
            "Evolution logo watermark"
        ]
    }
}

def generate_template(name, spec):
    """Generate HTML template for a slide"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            width: 1080px;
            height: 1920px;
            background: #0A0A0A;
            color: white;
            font-family: 'Geist Sans', 'Helvetica Neue', Arial, sans-serif;
            overflow: hidden;
            position: relative;
        }}
        
        /* Gold accent color: #D4AF37 */
        /* Dark charcoal: #0A0A0A */
        /* White text: #FFFFFF */
        
        .slide-{name} {{
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
            padding: 60px;
        }}
        
        .gold-accent {{
            color: #D4AF37;
        }}
        
        .gold-line {{
            width: 400px;
            height: 3px;
            background: #D4AF37;
            margin: 20px 0;
        }}
        
        .logo {{
            max-width: 400px;
            margin-bottom: 40px;
        }}
        
        h1 {{
            font-size: 72px;
            font-weight: bold;
            margin: 0;
            text-align: center;
        }}
        
        h2 {{
            font-size: 48px;
            font-weight: normal;
            margin: 20px 0;
            text-align: center;
        }}
        
        p {{
            font-size: 36px;
            text-align: center;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="slide-{name}">
        <!-- Template: {name} -->
        <!-- Duration: {spec['duration']}s -->
        <!-- Elements: {', '.join(spec['elements'])} -->
        
        <h1 class="gold-accent">{name.replace('_', ' ').title()}</h1>
        <div class="gold-line"></div>
        <p>Template ready for customization</p>
    </div>
</body>
</html>"""
    
    return html

def main():
    output_dir = "/mnt/s/Evolution-Content-Factory/assets/templates"
    os.makedirs(output_dir, exist_ok=True)
    
    for name, spec in TEMPLATE_SPECS.items():
        html = generate_template(name, spec)
        filepath = os.path.join(output_dir, f"{name}_template.html")
        with open(filepath, "w") as f:
            f.write(html)
        print(f"Created: {filepath}")
    
    # Create template manifest
    import json
    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(TEMPLATE_SPECS, f, indent=2)
    print(f"\nCreated manifest: {manifest_path}")
    print(f"\nTotal templates: {len(TEMPLATE_SPECS)}")

if __name__ == "__main__":
    main()

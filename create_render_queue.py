import requests
import json
from datetime import datetime

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rbWlkeWxmaHdwZXV1ZHVmaWhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzODU4NDUsImV4cCI6MjA4Njk2MTg0NX0.vfw5PZMCNB_ML65EKLlNyumBTE0Fs1wA_k38v6bu-r4"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Render queue for overnight execution
renders = [
    {
        "title": "Prudentia - 60s Full Story",
        "duration": 60,
        "pacing": "cinematic",
        "priority": 1
    },
    {
        "title": "Prudentia - 30s Teaser",
        "duration": 30,
        "pacing": "fast",
        "priority": 2
    },
    {
        "title": "Prudentia - 90s Extended",
        "duration": 90,
        "pacing": "documentary",
        "priority": 3
    }
]

for render in renders:
    project_data = {
        "title": render["title"],
        "race_url": "https://tokinvest.com",
        "status": "idea",
        "creative_brief": {
            "template": "horse-profile",
            "pacing": render["pacing"],
            "style": "professional",
            "duration": render["duration"],
            "assets": [
                {"path": "/assets/prudentia/Prudentia-13Feb2026-001.JPG", "type": "image", "label": "intro"},
                {"path": "/assets/prudentia/Prudentia-13Feb2026-002.JPG", "type": "image", "label": "pedigree"},
                {"path": "/assets/clips/manual_test.mp4", "type": "video", "label": "race_win"},
                {"path": "/assets/prudentia/Prudentia-13Feb2026.mp4", "type": "video", "label": "training"},
                {"path": "/assets/prudentia/Prudentia-13Feb2026-003.JPG", "type": "image", "label": "close"}
            ]
        },
        "script_content": {
            "segments": [
                {"start": 0, "end": 8, "text": "Prudentia. Four-year-old mare. In training at Wexford Stables, Matamata.", "visual": "intro"},
                {"start": 8, "end": 20, "text": "By Proisir, Champion Sire. Out of Little Bit Irish - 100% winners to runners. Sister Cork won the Tauranga Classic.", "visual": "pedigree"},
                {"start": 20, "end": 45, "text": "May 28, Heavy 10. Last to first. Circled the field. Won by two and a quarter lengths. Softly.", "visual": "race_win"},
                {"start": 45, "end": 70, "text": "Wexford Stables. Lance O'Sullivan, Andrew Scott. They train her brother. Know the family inside out.", "visual": "training"},
                {"start": 70, "end": 80, "text": "Winter's coming. The heavy tracks. She's ready.", "visual": "close"}
            ],
            "total_duration": 80,
            "word_count": 85
        }
    }
    
    response = requests.post(
        "https://nkmidylfhwpeuudufihf.supabase.co/rest/v1/projects",
        headers=HEADERS,
        json=project_data
    )
    print(f"Created: {render['title']} - Status: {response.status_code}")

print(f"\nRender queue ready. {len(renders)} videos queued for overnight execution.")

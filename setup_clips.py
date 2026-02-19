import requests
import json

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rbWlkeWxmaHdwZXV1ZHVmaWhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzODU4NDUsImV4cCI6MjA4Njk2MTg0NX0.vfw5PZMCNB_ML65EKLlNyumBTE0Fs1wA_k38v6bu-r4"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

project_id = "a7e13f4c-e695-4f0a-aa29-dbb85ea737c4"

# Create clip records for each asset
assets = [
    {"path": "/assets/prudentia/Prudentia-13Feb2026-001.JPG", "label": "intro", "duration": 5},
    {"path": "/assets/prudentia/Prudentia-13Feb2026-002.JPG", "label": "pedigree", "duration": 10},
    {"path": "/assets/clips/manual_test.mp4", "label": "race_win", "duration": 20},
    {"path": "/assets/prudentia/Prudentia-13Feb2026.mp4", "label": "training", "duration": 15},
    {"path": "/assets/prudentia/Prudentia-13Feb2026-003.JPG", "label": "close", "duration": 10}
]

for asset in assets:
    clip_data = {
        "project_id": project_id,
        "youtube_url": "local_asset",
        "start_seconds": 0,
        "end_seconds": asset["duration"],
        "label": asset["label"],
        "local_path": asset["path"],
        "status": "extracted"
    }
    
    response = requests.post(
        "https://nkmidylfhwpeuudufihf.supabase.co/rest/v1/clips",
        headers=HEADERS,
        json=clip_data
    )
    print(f"Created clip {asset['label']}: {response.status_code}")

# Reset the render job to pending
response = requests.patch(
    "https://nkmidylfhwpeuudufihf.supabase.co/rest/v1/jobs?project_id=eq.a7e13f4c-e695-4f0a-aa29-dbb85ea737c4&job_type=eq.render",
    headers=HEADERS,
    json={"status": "pending", "worker_id": None, "claimed_at": None}
)
print(f"Reset render job: {response.status_code}")

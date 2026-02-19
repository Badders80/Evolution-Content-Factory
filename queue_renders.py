import requests

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rbWlkeWxmaHdwZXV1ZHVmaWhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzODU4NDUsImV4cCI6MjA4Njk2MTg0NX0.vfw5PZMCNB_ML65EKLlNyumBTE0Fs1wA_k38v6bu-r4"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Get the 3 new projects
projects = requests.get(
    "https://nkmidylfhwpeuudufihf.supabase.co/rest/v1/projects?select=*&status=eq.idea&order=created_at.desc&limit=3",
    headers=HEADERS
).json()

print(f"Found {len(projects)} projects to process")

for project in projects:
    pid = project['id']
    title = project['title']
    print(f"\nProcessing: {title}")
    
    # Create clip records
    assets = [
        {"path": "/assets/prudentia/Prudentia-13Feb2026-001.JPG", "label": "intro", "duration": 8},
        {"path": "/assets/prudentia/Prudentia-13Feb2026-002.JPG", "label": "pedigree", "duration": 12},
        {"path": "/assets/clips/manual_test.mp4", "label": "race_win", "duration": 25},
        {"path": "/assets/prudentia/Prudentia-13Feb2026.mp4", "label": "training", "duration": 25},
        {"path": "/assets/prudentia/Prudentia-13Feb2026-003.JPG", "label": "close", "duration": 10}
    ]
    
    for asset in assets:
        clip = {
            "project_id": pid,
            "youtube_url": "local_asset",
            "start_seconds": 0,
            "end_seconds": asset["duration"],
            "label": asset["label"],
            "local_path": asset["path"],
            "status": "extracted"
        }
        r = requests.post(
            "https://nkmidylfhwpeuudufihf.supabase.co/rest/v1/clips",
            headers=HEADERS,
            json=clip
        )
        print(f"  Clip {asset['label']}: {r.status_code}")
    
    # Update project status to rendering
    r = requests.patch(
        f"https://nkmidylfhwpeuudufihf.supabase.co/rest/v1/projects?id=eq.{pid}",
        headers=HEADERS,
        json={"status": "rendering"}
    )
    print(f"  Status -> rendering: {r.status_code}")
    
    # Create render job
    job = {
        "project_id": pid,
        "job_type": "render",
        "status": "pending",
        "input_payload": {"project_id": pid}
    }
    r = requests.post(
        "https://nkmidylfhwpeuudufihf.supabase.co/rest/v1/jobs",
        headers=HEADERS,
        json=job
    )
    print(f"  Render job: {r.status_code}")

print("\n✅ All 3 projects queued for rendering")

import requests

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rbWlkeWxmaHdwZXV1ZHVmaWhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzODU4NDUsImV4cCI6MjA4Njk2MTg0NX0.vfw5PZMCNB_ML65EKLlNyumBTE0Fs1wA_k38v6bu-r4"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Get recent projects
response = requests.get(
    "https://nkmidylfhwpeuudufihf.supabase.co/rest/v1/projects?select=id,title,status,created_at&order=created_at.desc&limit=10",
    headers=HEADERS
)
print(f"Projects: {response.status_code}")
if response.status_code == 200:
    for p in response.json():
        print(f"  - {p['title']}: {p['status']} ({p['created_at'][:10]})")

# Get pending jobs
jobs = requests.get(
    "https://nkmidylfhwpeuudufihf.supabase.co/rest/v1/jobs?select=id,job_type,status,project_id&status=eq.pending",
    headers=HEADERS
)
print(f"\nPending jobs: {jobs.status_code}")
if jobs.status_code == 200:
    print(f"Count: {len(jobs.json())}")
    for j in jobs.json():
        print(f"  - {j['job_type']}: {j['status']}")

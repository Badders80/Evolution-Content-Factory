import requests
import json

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rbWlkeWxmaHdwZXV1ZHVmaWhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzODU4NDUsImV4cCI6MjA4Njk2MTg0NX0.vfw5PZMCNB_ML65EKLlNyumBTE0Fs1wA_k38v6bu-r4"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

project_id = "a7e13f4c-e695-4f0a-aa29-dbb85ea737c4"

# Update with script and transition to approval_clips
script = {
    "segments": [
        {"start": 0, "end": 5, "text": "Prudentia. Four-year-old mare. In training at Wexford Stables, Matamata.", "visual": "intro"},
        {"start": 5, "end": 15, "text": "By Proisir. Champion sire. Out of Little Bit Irish. Four foals to race, four winners. Her sister Cork won the Tauranga Classic. It's a family thing.", "visual": "pedigree"},
        {"start": 15, "end": 35, "text": "May 28. Heavy 10. She settled last. Dead last. Then she found her rhythm out wide. Circled them. Won by two and a quarter lengths. Softly.", "visual": "race_win"},
        {"start": 35, "end": 50, "text": "Wexford Stables. Lance O'Sullivan, Andrew Scott. They train her brother too. Know the family. Kylie Bax manages her. She's not rushing. Just preparing.", "visual": "training"},
        {"start": 50, "end": 60, "text": "Winter's coming. The heavy tracks. She's ready.", "visual": "close"}
    ],
    "total_duration": 60,
    "word_count": 95
}

response = requests.patch(
    f"https://nkmidylfhwpeuudufihf.supabase.co/rest/v1/projects?id=eq.{project_id}",
    headers=HEADERS,
    json={
        "script_content": script,
        "status": "approval_clips"
    }
)

print(f"Update status: {response.status_code}")
print(response.text)

# Transition to rendering
resp = requests.post(
    f"http://localhost:8000/projects/{project_id}/transition",
    json={"to_status": "rendering"}
)
print(f"Transition status: {resp.status_code}")
print(resp.text)

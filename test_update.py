from supabase import create_client
import os

supabase = create_client(
    "https://nkmidylfhwpeuudufihf.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rbWlkeWxmaHdwZXV1ZHVmaWhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzODU4NDUsImV4cCI6MjA4Njk2MTg0NX0.vfw5PZMCNB_ML65EKLlNyumBTE0Fs1wA_k38v6bu-r4"
)

# Add script content to project
result = supabase.table('projects').update({
    'script_content': {
        'segments': [
            {'start': 0, 'end': 5, 'text': 'Tauranga Race 2 - The finish line!', 'visual_prompt': 'finish_line'}
        ],
        'total_duration': 5,
        'word_count': 6
    }
}).eq('id', 'a298f65c-e5e9-45c0-b046-77121915a054').execute()

print(result)

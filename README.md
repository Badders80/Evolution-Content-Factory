# Evolution Content Factory v3.0
## Phase 1: Foundation Setup

### What Was Created
This folder contains the scaffolded infrastructure for your AI-powered TikTok content pipeline.

### Folder Structure
```
Evolution-Content-Factory/
├── orchestrator/          # FastAPI backend (state machine API)
├── workers/               # Stateless containerized agents
│   ├── researcher/        # Scrapes racing data (Firecrawl)
│   ├── writer/            # Writes scripts (Gemini/Moonshot)
│   ├── clip-agent/        # Downloads YouTube segments
│   ├── editor/            # Renders video (FFmpeg NVENC)
│   └── voice-agent/       # Generates voiceover (Kokoro/ElevenLabs)
├── frontend/              # Next.js dashboard (Phase 6)
├── assets/                # Storage
│   ├── broll/             # Your B-roll library
│   ├── clips/             # Downloaded YouTube segments
│   ├── renders/           # Final video outputs
│   └── templates/         # Video composition templates
├── docs/                  # Documentation
│   └── 001_initial_schema.sql  # Supabase setup
└── docker-compose.yml     # Local stack orchestration
```

## Setup Instructions

### Step 1: Create Supabase Project (You must do this)

1. Go to https://supabase.com
2. Click "New Project"
3. Name: `evolution-content-factory`
4. Region: Choose closest to you (Singapore or Sydney)
5. Plan: Free Tier
6. Save the **Project URL** and **Anon Key** (Settings > API)

### Step 2: Run Database Schema

1. In Supabase Dashboard, go to SQL Editor
2. Copy contents of `docs/001_initial_schema.sql`
3. Paste and click "Run"
4. Verify: Tables should appear in Table Editor

### Step 3: Get API Keys (You must do this)

| Service | URL | What For |
|---------|-----|----------|
| **Gemini** | https://ai.google.dev | Script writing |
| **Moonshot** | https://platform.moonshot.cn | Alternative LLM (you have this) |
| **Firecrawl** | https://firecrawl.dev | Web scraping (free tier) |
| **ElevenLabs** | https://elevenlabs.io | Voiceover fallback |

### Step 4: Configure Environment

Create `.env` file in this directory:

```bash
# Supabase (from Step 1)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# AI APIs (from Step 3)
GEMINI_API_KEY=your-gemini-key
MOONSHOT_API_KEY=your-moonshot-key
FIRECRAWL_API_KEY=your-firecrawl-key
ELEVENLABS_API_KEY=your-elevenlabs-key

# Telegram (for approvals)
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

### Step 5: Start Local Stack

```bash
# Start all workers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f orchestrator
```

## B-Roll Generation (Next Step)

The `workers/broll-generator/` folder contains agents for:
- **FLOW Agent**: Generates cinematic horse racing footage
- **Veo3 Agent**: Creates dynamic action sequences
- **Canva Agent**: Pulls from Canva Pro stock library

To generate initial B-roll:
1. Configure FLOW/Veo3 API keys in `.env`
2. Run: `python workers/broll-generator/generate.py --prompt "horse galloping morning mist"`
3. Assets automatically saved to `assets/broll/` and indexed in Supabase

## First Test Project

Once setup complete:

```bash
# Create test project
curl -X POST http://localhost:8000/projects \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Race Preview",
    "race_url": "https://racing.com",
    "creative_brief": {
      "template": "pre-race-preview",
      "youtube_clips": [
        {"url": "https://youtube.com/watch?v=EXAMPLE", "start": 30, "end": 60}
      ]
    }
  }'
```

## Next Steps

1. ✅ **You**: Complete Steps 1-3 (accounts & keys)
2. ✅ **Me**: Generate worker code once you confirm Supabase is running
3. ✅ **Together**: Test first project end-to-end

## Questions?

Check `docs/TROUBLESHOOTING.md` (coming in Phase 2)

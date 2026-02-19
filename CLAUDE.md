# CLAUDE.md - Evolution-Content-Factory

## What this repo is and what it solves
Evolution-Content-Factory is a video generation pipeline that uses AI to create high-quality racing content for Evolution Stables. It solves the problem of automating content creation by leveraging tools like FFmpeg, Google Generative AI, and ComfyUI to produce videos from simple text prompts.

## Full Stack
### What IS used:
- **Python 3.12** for core logic
- **FFmpeg** for video processing
- **Google Generative AI (Gemini)** for script writing and voice generation
- **ComfyUI** for image generation
- **Streamlit** for UI
- **Docker** for containerization (planned)

### What IS NOT used:
- **OpenAI**: Not used (Google Generative AI preferred)
- **Premiere Pro**: Not used (FFmpeg automation preferred)
- **DaVinci Resolve**: Not used (FFmpeg automation preferred)

## Hard Coding Rules

1. **No empty placeholder files** - Implement or don't create the file
2. **FFmpeg commands must be tested** - Always test FFmpeg commands before committing
3. **AI prompts must follow brand guidelines** - See brand-identity/BRAND_VOICE.md
4. **Output paths must be standardized** - Follow Safe-Path architecture
5. **Error handling must be robust** - Handle video generation failures gracefully

## Project Structure
```
Evolution-Content-Factory/
├── assets/               # Input and output assets
│   ├── b-roll/          # Background video clips
│   ├── clips/           # Downloaded YouTube clips
│   ├── renders/         # Final video renders
│   └── templates/       # Video templates
├── content_generation/   # Content generation logic
│   ├── block_parser.py  # Parse content blocks
│   └── press_room.py    # HTML generation (shared with Evolution_Studio)
├── modules/              # Helper modules
│   └── auto_reel_builder.py  # Main reel building logic
├── workers/              # Worker processes
│   ├── broll-generator/  # B-roll generation
│   ├── clip-agent/       # YouTube clip downloader
│   ├── editor/           # Video editing
│   ├── researcher/       # Research and scraping
│   ├── voice-agent/      # Voice generation
│   └── writer/           # Script writing
├── .env                  # Environment variables
├── docker-compose.yml    # Docker configuration
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```

## Key Features
1. **Auto Reel Builder**: Generates videos from text prompts using FFmpeg
2. **B-Roll Generation**: Creates b-roll from images using Ken Burns effect
3. **Voice Generation**: Uses Google Generative AI for voice overs
4. **Script Writing**: Generates scripts from content blocks
5. **Clip Downloader**: Downloads YouTube clips for content

## Environment Variables
Required environment variables in `.env`:
```
GEMINI_API_KEY=
FIRECRAWL_API_KEY=
NEXTAUTH_URL=
```

## WSL2 Paths
- **Project Path**: `/home/evo/projects/Evolution-Content-Factory/`
- **Windows Path**: `C:\Users\Evo\projects\Evolution-Content-Factory\`
- **Output Folder**: `/home/evo/projects/Evolution-Content-Factory/assets/renders/`

## Current Phase and Next Build Target
- **Current Phase**: Foundation Layer
- **Next Build Target**: Improve clip extraction and optimize FFmpeg commands

## Commands
- **Run Auto Reel Builder**: `python modules/auto_reel_builder.py`
- **Install Dependencies**: `pip install -r requirements.txt`

## Source of Truth
**All development standards are defined in 00_DNA**:
- **Build Philosophy**: `/home/evo/00_DNA/build-philosophy/Master_Config_2026.md`
- **System Prompts**: `/home/evo/00_DNA/system-prompts/PROMPT_LIBRARY.md`
- **Brand Voice**: `/home/evo/00_DNA/brand-identity/BRAND_VOICE.md`
- **Workflows**: `/home/evo/00_DNA/workflows/`

**Core Bible Documents**:
1. `/home/evo/00_DNA/brand-identity/Evolution_Content_Factory.md` - Content Factory brand guidelines

**Key Files to Reference**:
1. `/home/evo/00_DNA/AGENTS.core.md` - Universal agent rules
2. `/home/evo/00_DNA/build-philosophy/Master_Config_2026.md` - Hardware and architecture specs
3. `/home/evo/00_DNA/brand-identity/MESSAGING_CHEAT_SHEET.md` - Brand voice guidelines

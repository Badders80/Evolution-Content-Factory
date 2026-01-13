# Systems & Architecture

**Version**: v0.0 (Manual-Templated)  
**Last Updated**: January 13, 2026  
**Hardware**: Samsung 990 PRO @ /mnt/scratch

---

## Hardware Reality

**Your Setup**:
- **S Drive**: Samsung 990 PRO 2TB NVMe
- **Mount**: `/mnt/scratch` (WSL2)
- **GPU**: RTX 3060 12GB (headless compute)
- **CPU**: Ryzen 5 7600X (6C/12T)
- **RAM**: 32GB DDR5 (24GB for WSL, 8GB for Windows)

**Optimized for**:
- Fast video rendering (NVMe throughput)
- Local asset generation (ComfyUI on GPU)
- No cloud dependency (cost control)

---

## Directory Structure

```text
/mnt/scratch/projects/
├── .planning/
│   └── evolution-content-factory/ # This documentation
│       ├── 00-MISSION.md
│       ├── 01-VOICE.md
│       ├── 02-SYSTEMS.md
│       ├── BUILD-v0.0.md
│       ├── BUILD-v0.1.md
│       ├── BUILD-v0.2.md
│       ├── BACKLOG.md
│       ├── STATE.md
│       ├── CHANGELOG.md
│       └── templates/
│           ├── TEMPLATE-preview.md
│           ├── TEMPLATE-recap.md
│           └── TEMPLATE-throwback.md
│
├── Asset_Generation/ # Video production workspace
│   ├── broll/ # Stock footage (Pexels)
│   │   └── generic/ # Non-NZ specific clips
│   ├── images/ # Static assets
│   │   ├── horses/ # Horse photos
│   │   └── charts/ # Data visualizations
│   ├── voice/ # Voice-over MP3s (Google TTS)
│   ├── final/ # Rendered videos (pre-approval)
│   ├── approved/ # Ready to post
│   ├── render_video.sh # FFmpeg production script
│   └── comfyui_workflows/ # Chart generation workflows
│
├── Evolution_Studio/ # Django (future use)
│   └── content/
│       ├── scripts/ # Production scripts
│       └── data/
│           └── flow_ledger.csv # TAB data tracking (Google Sheets backup)
│
├── Brand_Voice/ # Voice guidelines (MCP server later)
│   ├── 00_kernel/
│   ├── 01_modules/
│   └── 02_logic/
│
└── ComfyUI/ # AI asset generation
    └── workflows/
        └── chart_simple.json # Data visualization workflow
```

---

## Production Tools (v0.0)

### **Video Rendering**
- **Tool**: FFmpeg (local, no cloud)
- **Input**: B-roll (70-80%) + images (10-20%) + voice (100%)
- **Output**: 30-40 sec vertical video (1080x1920)
- **Quality**: H.264, CRF 23, optimized for TikTok/Reels/Instagram
- **Location**: `/mnt/scratch/projects/Asset_Generation/`

### **Voice Generation**
- **Tool**: Google Cloud TTS (simple, works)
- **Voice**: `en-AU-Neural2-B` (Aussie male, close to Kiwi)
- **Output**: MP3, synced to video length
- **Future**: May switch to ElevenLabs for more natural NZ accent

### **Asset Generation**
- **Tool**: ComfyUI (local GPU)
- **Use**: Charts, data visualizations (when needed)
- **Frequency**: 1-2 custom assets per video
- **Workflow**: Simple prompts, not over-engineered

### **B-Roll Sources**
- **Primary**: Pexels, Pixabay (free, no attribution)
- **Strategy**: Generic racing footage, fly under radar
- **Credit**: Always source correctly if using specific content
- **Future**: Shoot own B-roll at NZ tracks (when credibility established)

---

## Image-to-Motion Techniques

**Ken Burns Effect** (pan + zoom):
- Takes 1 static image -> 5-10 sec video
- CPU-based (no GPU needed)
- Professional cinematic look

**FFmpeg Command**:
```bash
ffmpeg -loop 1 -i horse.jpg \
  -vf "zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920" \
  -t 5 output.mp4
```

**Text Overlays**:
- Animated stats ("68% WIN RATE")
- Race names, countdowns
- Burned-in captions (accessibility + silent playback)

**Split Screens**:
- Two images side-by-side
- Comparison views (before/after)

All done via FFmpeg - minimal system load, no GPU required.

---

## Workflow Philosophy (v0.0)

**Manual-Templated > Full Automation**

Why:
- ✅ Learn what works before automating
- ✅ Iterate fast without rebuilding workflows
- ✅ Quality control at every step
- ✅ Realistic for 3-5 videos/week
- ✅ Understand the rhythm before scaling

Process:
- Write script (manual, using templates)
- Generate voice (Google TTS)
- Collect B-roll/images (Pexels + manual selection)
- Hit "run" on FFmpeg script
- Review output
- Approve or retry
- Post to social (manual upload)

When to automate (v0.2+):
- After 20+ videos, you know the rhythm
- When volume demands it (10+ videos/week)
- NOT before

---

## Asset Composition (70-80-10 Rule)

70-80% B-Roll (Pexels stock footage):
- Morning trackwork
- Starting gates
- Finish line
- Slow-motion horse movement

10-20% Static Images with Motion:
- Ken Burns effects (pan/zoom)
- Text overlays (stats, race names)
- Horse photos

5-10% Custom Graphics (ComfyUI when needed):
- Sectional ranking charts
- Flow visualization (future)
- Stat cards

= Professional content without taxing your system

---

## TAB Data Collection (Background)

Start NOW, publish later:

Tool: Google Sheets (MVP)

Data: Odds, volume, price movements

Frequency: Manual input after each race day (for now)

Location: /mnt/scratch/projects/Evolution_Studio/content/data/flow_ledger.csv

Purpose: Build historical dataset for v0.1 (pundit tracking)

Schema:
```text
race_date,venue,race_num,horse_name,flow_type,flow_timing,open_price,close_price,total_volume,result,notes
```

Why collect early:
- Future gold mine (historical flow patterns)
- Proves patterns over time
- When you launch pundit tracking, you have receipts

---

## Future Infrastructure (Not v0.0)

When scale demands (v0.2+):
- n8n workflows (orchestration)
- TAB API automation (real-time polling)
- Postgres database (structured flow data)
- Telegram approval bot (mobile control)
- ElevenLabs voice (better NZ accent)

For now: Keep it simple. Manual-templated workflow.

---

## Technical Notes

WSL2 Path Translation:

Windows: S:\projects\Asset_Generation\

WSL2: /mnt/scratch/projects/Asset_Generation/

Always use WSL2 paths in terminal/scripts

Permissions:

User: evo (UID 1000)

All /mnt/scratch files owned by evo:evo

If permission errors: sudo chown -R evo:evo /mnt/scratch/projects/

GPU Usage:

ComfyUI uses RTX 3060 for image generation

FFmpeg uses CPU for video encoding (faster on NVMe)

Keep GPU free for ComfyUI by not running multiple jobs

---

Last Updated: January 13, 2026

Hardware Verified: Samsung 990 PRO operational, WSL2 mount stable

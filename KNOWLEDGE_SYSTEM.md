# Evolution Knowledge System

## What This Is
Self-improving system that captures what works for Evolution Stables content production.

## Pattern Library

### Slide Patterns (What Works)

**Opening Slide**
- Background: Dark charcoal #0A0A0A
- Center: Gold Evolution logo (300-400px)
- Below: "Powered by Tokinvest" (gold #D4AF37, 36pt)
- Below: "Presents" (white, 32pt)
- Accent: Gold line below text (2px, 400px wide)
- Animation: Subtle zoom from 1.1x to 1.0x
- Duration: 4-5 seconds

**Pedigree Slide**
- Background: Horse photo with Ken Burns
- Overlay: Black box at top (80px down, 500px height)
- Left: Sire photo (300px wide, positioned 80px from left, 480px down)
- Right: Dam photo (300px wide, positioned 700px from left, 480px down)
- Text: Horse name (gold, 64pt, centered top)
- Text: Details (white, 28pt, below name)
- Labels: "Sire:" and "Dam:" (gold, 24pt, above photos)
- Animation: Slow zoom on background, static photos
- Duration: 6-8 seconds

**Race Result Slide**
- Video: Full width race footage (letterboxed in vertical)
- Top bar: Black overlay with race name (gold text)
- Bottom bar: Black overlay with position (gold text)
- Logo: Prudentia logo centered above video
- Animation: Video plays, overlays static
- Duration: 8-10 seconds

### Color Palette (Brand DNA)
- Primary Gold: #D4AF37
- Dark Background: #0A0A0A
- Text White: #FFFFFF
- Secondary Gold (lighter): #E5C158
- Success Green (for wins): #4CAF50

### Typography
- Headlines: DejaVu Sans Bold, 48-72pt
- Body: DejaVu Sans, 24-36pt
- Labels: DejaVu Sans Bold, 24-28pt
- All caps for emphasis

### Transitions (What Works)
- Crossfade: 0.8 seconds between scenes
- No jarring cuts
- Smooth, professional pacing

### Audio (Not Yet Implemented)
- Style: The Social Network tension bed
- Voice: Documentary, authoritative
- Pace: Match video cuts

## Content Templates (Proven Formats)

### Horse Profile Reel (60s)
1. Opening (5s) - Evolution branding
2. Horse intro (8s) - Photo + name + key stats
3. Pedigree (10s) - Sire/dam with photos
4. Form/Results (15s) - Race footage + results
5. Trainer/Team (10s) - Behind the scenes
6. CTA (7s) - Listing info + question
7. Outro (5s) - Logo + tagline

### Race Preview Reel (45s)
1. Hook (3s) - "The numbers don't lie"
2. Horse intro (5s)
3. Form analysis (12s)
4. Race conditions (8s)
5. Prediction (7s)
6. CTA (5s)
7. Outro (5s)

### Race Result Reel (30s)
1. Hook (3s) - Result reveal
2. Race footage (15s) - The win
3. Stats overlay (7s)
4. CTA (5s)

## B-Roll Categories (To Generate)

### Heritage/Traditional (Relaxed)
- Morning training, golden hour
- Horses in parade ring, formal
- Slow-motion galloping
- Steam rising from coats
- Classic racing silks
- Country racecourse atmosphere

### Performance/Hype (Energetic)
- Barrier loading tension
- Finish line drama
- Jockey celebrations
- Crowd reactions
- Fast cuts to beat drops

### Behind the Scenes (Authentic)
- Trainer with horses
- Early morning workouts
- Stable life
- Transport/loading
- Vet checks

## What Doesn't Work (Learned)

❌ Too many text overlays on video
❌ Jarring transitions without fades
❌ Generic stock footage
❌ Casual language (no "game-changer")
❌ Bright/neon colors (off-brand)
❌ Fast cuts for heritage content

## Automation Patterns

### Slide Generation
Input: Type + content dict
↓
AI generates design spec
↓
FFmpeg renders video
↓
Output: 5s animated slide

### Asset Search
Input: Natural language query
↓
Vector embedding of query
↓
Similarity search in index
↓
Output: Ranked asset list

### Reel Assembly
Input: Horse + race ID
↓
Fetch race data
↓
Search assets
↓
Generate slides
↓
Create overlays
↓
FFmpeg concat with fades
↓
Output: Final reel

## Strategic Context

### Current Goal
3 Horses Live in 30 Days

### Content Priorities
1. Prudentia (existing, proven)
2. Next horse profile (create template)
3. Race previews (upcoming events)
4. Heritage storytelling (brand building)

### ROI Filter
- Does this help get horses live?
- Does this strengthen brand?
- Is the squeeze worth the juice?

## Tool Stack

### AI Generation
- Gemini/GLM: Content ideas, design specs
- Local LLMs (Ollama): Code generation, quick tasks
- mxbai-embed-large: Vector search

### Video Production
- FFmpeg: All video processing
- ImageMagick: Static graphics
- Ken Burns: zoompan filter

### Data/Storage
- S: Drive: Fast local storage
- G Drive: Team collaboration
- Supabase: Future (vector DB, jobs)

### Automation
- Python: Orchestration
- Bash: Build scripts
- Docker: Containerized workers

## Improvement Log

### 2026-02-19
- Built AI Slide Generator (smart vs static)
- Created Smart Asset Library (search vs browse)
- Implemented Auto-Reel Builder (workflow vs manual)
- Using local LLMs for design/code generation

### Next Improvements
- [ ] Vector embeddings for true semantic search
- [ ] Gemini image generation for slide visuals
- [ ] Research Engine integration for auto-data
- [ ] Veo3/FLOW integration for B-roll generation
- [ ] Auto-sync to G Drive on render complete

## How to Use This

1. **Creating new slide type**: Reference patterns above
2. **Finding assets**: Use Smart Asset Library search
3. **Building reel**: Run auto_reel_builder.py
4. **Adding pattern**: Document here after testing

## Success Metrics

- Reel production time: Target < 30 minutes per reel
- Asset reuse rate: Target > 70%
- Render quality: 1080x1920, smooth, professional
- Brand consistency: 100% DNA compliance

---

*This document improves itself. After each reel, update what worked/didn't.*

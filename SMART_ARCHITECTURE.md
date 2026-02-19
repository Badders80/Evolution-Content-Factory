# Evolution Content Factory - Smart Architecture

## The Problem: Manual Work
❌ Manually building each reel  
❌ Creating static overlays  
❌ Hard-coding templates  
❌ Manual asset organization

## The Solution: AI-Native Pipeline
✅ AI generates slides from text prompts  
✅ AI generates B-roll from descriptions  
✅ AI creates dynamic overlays based on data  
✅ Self-improving template system

---

## Smart Components

### 1. AI Slide Generator (Not static HTML)
**Input:** Text description  
**Output:** Rendered video slide

```python
slide = ai_slide_generator.create(
    type="pedigree",
    horse="Prudentia",
    sire="Proisir", 
    dam="Little Bit Irish",
    style="heritage"
)
# Returns: 5-second video file with animated pedigree
```

**Tools:** Gemini Image Generation → FFmpeg animation

### 2. Dynamic Overlay System
**Input:** Race data JSON  
**Output:** Animated overlay video

```python
overlay = overlay_generator.create_calendar(
    date="2026-03-15",
    venue="Ellerslie",
    style="gold_dark"
)
# Returns: Animated calendar overlay with countdown
```

**Tools:** ImageMagick + FFmpeg filters

### 3. Smart Asset Library
**Not just folders — searchable, tagged, AI-indexed**

```python
assets.search(
    query="galloping horse heavy track morning",
    style="heritage",
    duration="5-10s"
)
# Returns: ranked list of matching assets with AI similarity scores
```

**Tools:** Supabase + vector embeddings (mxbai-embed-large)

### 4. Auto-Reel Builder
**Input:** Horse name + race ID  
**Output:** Complete reel

```python
reel = auto_builder.create(
    horse="Prudentia",
    race_id="tauranga_maiden_2025",
    template="heritage_win"
)
# Automatically:
# - Fetches race data from Research Engine
# - Generates pedigree slide
# - Creates race result overlay
# - Assembles with B-roll
# - Adds music and voiceover
```

---

## Implementation Path

### Phase 1: Smart Slide Generator (Now)
Use Gemini/GPT-4o to generate slide images from prompts, then animate with FFmpeg

### Phase 2: Vector Search (Next)
Index all assets with AI embeddings for semantic search

### Phase 3: Auto-Builder (Future)
Connect Research Engine → Slide Generator → Asset Library → Final Render

---

## What I Should Build Now (Smarter)

Instead of static HTML templates, build:

**1. AI Slide Generator Script**
- Takes text prompt
- Calls Gemini to generate slide image
- Applies Ken Burns with FFmpeg
- Returns video file

**2. Dynamic Overlay Generator**
- Takes race data
- Generates custom overlay on-the-fly
- No pre-made PNGs needed

**3. Asset Search CLI**
- Search by natural language
- "Find me a training shot with morning light"
- Returns ranked results

---

## The Real Question

Do you want me to:

**A) Finish the manual/static approach** (what I've been doing)
- Complete the basic templates
- Create remaining overlays manually
- Wrap up the current implementation

**B) Pivot to the smart/AI-native approach** (what I should be doing)
- Build AI slide generator
- Create dynamic overlay system
- Set up vector search for assets
- Build auto-reel pipeline

**C) Hybrid** 
- Finish current tasks quickly
- Then build the smart systems on top

**What's your call?** I can execute any of these, but I want to build what actually moves the needle for Evolution Stables.

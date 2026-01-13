# BUILD v0.0: Credibility First

**Status**: Current Phase (Weeks 1-12)  
**Goal**: 12 consecutive weeks of professional, consistent content  
**Success Metric**: Earn credibility before judging pundits

---

## Mission

**Prove you can make great content before you go controversial.**

If you launch pundit tracking with amateur quality, their tribal audiences will destroy you. You become the leaderboard loser.

**v0.0 = Sharpen the tools. Earn respect.**

---

## Content Types (3 Only)

### **1. Preview** (Thursday/Friday)
**Format**: 30-40 seconds, vertical (1080x1920)  
**Frequency**: 1x per week (5 biggest races)  
**Structure**:
- Hook (0-5s): "Five horses. One race. Here's what the data says."
- Analysis (5-30s): Sectionals, track conditions, notable patterns
- Close (30-40s): Data-driven wrap-up (NO prediction)

**Example**:
> "Ellerslie R7 this Saturday. Horse A shows sectional efficiency 12% above field average. Track suits on-pace runners. The numbers don't lie."

---

### **2. Recap** (Monday)
**Format**: 30-40 seconds, vertical (1080x1920)  
**Frequency**: 1x per week (5 biggest races)  
**Structure**:
- Hook (0-5s): "[Horse] paid $12.50. Here's what the data showed."
- Analysis (5-30s): Match data to outcome, flow validation
- Close (30-40s): "The data told the story."

**Example**:
> "Horse X won at $8.40. Heavy flow moved the market 40% in 15 minutes. Sectionals ranked #1 in final 600m. The flow indicated it."

---

### **3. Throwback Thursday**
**Format**: 30-40 seconds, vertical (1080x1920)  
**Frequency**: 1x per week  
**Structure**:
- Hook (0-5s): "They said he was too small. The data said otherwise."
- Story (5-30s): Underdog narrative, emotional connection
- Close (30-40s): Inspirational wrap

**Example**:
> "Written off at $51. But the stride efficiency data showed something the experts missed. Three months later, Group 1 winner."

---

## Production Workflow (Manual-Templated)

### **Step 1: Script Creation** (15 min)
- Use templates: `TEMPLATE-preview.md`, `TEMPLATE-recap.md`, `TEMPLATE-throwback.md`
- Fill in race data, stats, key points
- Save to: `/mnt/scratch/projects/Evolution_Studio/content/scripts/2026-01-18-ellerslie-preview.md`

### **Step 2: Asset Gathering** (15 min)
- Download 3-5 B-roll clips from Pexels (generic racing footage)
- Save to: `/mnt/scratch/projects/Asset_Generation/broll/generic/`
- Optional: Generate 1-2 charts in ComfyUI
- Save to: `/mnt/scratch/projects/Asset_Generation/images/charts/`

### **Step 3: Voice Generation** (5 min)
- Copy script text
- Generate via Google Cloud TTS (`en-AU-Neural2-B`)
- Save to: `/mnt/scratch/projects/Asset_Generation/voice/ellerslie-r7-preview.mp3`

### **Step 4: Video Assembly** (10 min)
- Run FFmpeg script: `bash render_video.sh ellerslie-r7-preview`
- Output: `/mnt/scratch/projects/Asset_Generation/final/ellerslie-r7-preview.mp4`

### **Step 5: Review & Approve** (5 min)
- Watch video in VLC
- Check: Voice sync? Captions readable? Data accurate?
- If good: Move to `/approved/`
- If not: Edit script, re-run FFmpeg

### **Step 6: Post to Social** (5 min)
- Upload to TikTok/X/Instagram manually
- Use caption template (see `01-VOICE.md`)
- Log link in tracking sheet

**Total time per video**: ~60 minutes

---

## Weekly Schedule

| Day | Content | Task |
|-----|---------|------|
| **Thursday** | Throwback Thursday | Research underdog story, create script, render, post |
| **Friday** | Weekend Preview | Script 5 biggest races, collect B-roll, render, post |
| **Monday** | Weekend Recap | Review results, match to data, render, post |

**3 videos per week = 12 videos in 4 weeks = 48+ videos in 12 weeks**

---

## Success Criteria (Before v0.1)

**After 12 weeks, audit**:
- ✅ Consistent posting (no gaps)?
- ✅ Video quality professional (not amateur)?
- ✅ Engagement growing (saves, shares, comments)?
- ✅ Zero mistakes in data/facts (credibility intact)?

**If YES**: Move to v0.1 (pundit tracking).  
**If NO**: Continue refining v0.0 for another 4 weeks.

---

## What We're NOT Doing (Yet)

**Deferred to v0.1+**:
- ❌ Pundit tracking (content-of-content)
- ❌ Leaderboards (tribal engagement)
- ❌ TAB API automation (data collection is manual)
- ❌ n8n workflows (manual-templated for now)
- ❌ Ownership mentions (Fight Club rule)

**Focus**: Just make great Preview/Recap/Throwback content.

---

## Key Principles

1. **Quality over quantity**: 3 great videos > 10 mediocre ones
2. **Data accuracy**: Zero tolerance for mistakes
3. **Consistent schedule**: Never miss a week
4. **Professional production**: Looks like it cost money (but didn't)
5. **No predictions**: Referee stance only

---

## Common Pitfalls to Avoid

**❌ Don't**:
- Start pundit tracking before credibility is established
- Over-automate before understanding the rhythm
- Use lad slang or certainty language
- Miss posting deadlines (kills momentum)
- Mention ownership (Fight Club rule)

**✅ Do**:
- Focus on one thing: great content
- Learn what works through iteration
- Build TAB data collection in background
- Stay disciplined on voice guidelines
- Stay honest about what's working and what isn't

---

## Tools & Resources

**B-Roll Sources**:
- [Pexels](https://www.pexels.com/videos/) - Free racing footage
- [Pixabay](https://www.pixabay.com/videos/) - Alternative source

**Voice Generation**:
- Google Cloud TTS - `en-AU-Neural2-B` voice

**Templates**:
- Located in: `/mnt/scratch/projects/.planning/evolution-content-factory/templates/`

**FFmpeg Script**:
- Located in: `/mnt/scratch/projects/Asset_Generation/render_video.sh`

---

*Phase Duration*: 12 weeks  
*Review Date*: Week 12 (early April 2026)  
*Decision Point*: Move to v0.1 only if success criteria met

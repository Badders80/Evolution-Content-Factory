# Evolution Content Factory: Documentation

**Version**: v0.0 (Rebirth Edition)  
**Last Updated**: January 14, 2026  
**Status**: Pre-Launch (Documentation Complete)

---

## Overview

This repository contains the complete planning documentation for the **Evolution Content Factory** - a content engagement funnel designed to build credibility, capture audience attention, and eventually convert viewers into fractional racehorse owners via [Evolution Stables](https://www.evolutionstables.nz).

**Strategy**: Content-of-content (referee positioning), NOT original analysis or tipster content.

---

## Quick Start

### **If you're building content:**
1. Read `00-MISSION.md` - Understand the Fight Club funnel
2. Read `01-VOICE.md` - Learn the vocabulary and tone
3. Read `BUILD-v0.0.md` - Follow the v0.0 workflow
4. Use templates in `templates/` for scripts

### **If you're setting up systems:**
1. Read `02-SYSTEMS.md` - Hardware and directory structure
2. Run setup commands to create folder structure
3. Download B-roll library (Pexels)
4. Test FFmpeg render pipeline

### **If you're reviewing strategy:**
1. Read `00-MISSION.md` - Core mission
2. Read `BUILD-v0.0.md`, `BUILD-v0.1.md`, `BUILD-v0.2.md` - Phased approach
3. Read `BACKLOG.md` - Future vision

---

## Document Structure

### **Core Strategy**
- `00-MISSION.md` - Mission, Fight Club rule, funnel strategy
- `01-VOICE.md` - Voice guidelines, vocabulary, banned terms
- `02-SYSTEMS.md` - Hardware, S drive structure, workflow

### **Build Phases**
- `BUILD-v0.0.md` - Credibility first (Preview/Recap/Throwback)
- `BUILD-v0.1.md` - Pundit tracking (neutral reporting)
- `BUILD-v0.2.md` - Public leaderboards (tribal engagement)
- `BACKLOG.md` - Future features (v0.3+ ownership reveal)

### **Operational**
- `STATE.md` - Living decisions, blockers, next actions
- `CHANGELOG.md` - Document updates, vocabulary changes
- `SUMMARY.md` - Completion checklist and next steps

### **Templates**
- `templates/TEMPLATE-preview.md` - Thursday/Friday preview script
- `templates/TEMPLATE-recap.md` - Monday recap script
- `templates/TEMPLATE-throwback.md` - Thursday throwback script
- `templates/TEMPLATE-pundit-recap.md` - Pundit performance recap (v0.1)

---

## Key Principles

1. **Fight Club Rule**: NO ownership mentions until v0.3 (24+ weeks)
2. **Credibility First**: 12 weeks of quality content before pundit tracking
3. **Manual-Templated**: Learn rhythm before automating
4. **Data-Driven**: Every claim backed by numbers
5. **Referee Positioning**: Report facts, never make predictions

---

## Phases Overview

### **v0.0: Credibility First** (Weeks 1-12)
- 3 content types: Preview, Recap, Throwback
- Manual-templated workflow
- Goal: Prove you can make great content

### **v0.1: Pundit Tracking** (Weeks 13-20)
- Add: Neutral pundit performance reporting
- NO leaderboards yet (just facts)
- Goal: Build goodwill, collect data

### **v0.2: Public Leaderboards** (Weeks 21-28)
- Add: Public rankings, tribal engagement
- Must be bulletproof (data accuracy 100%)
- Goal: Establish authority as referee

### **v0.3+: Ownership Reveal** (Week 29+)
- Reveal: Evolution Stables digital syndication
- "Don't just back them. Own them."
- Goal: Convert audience to fractional owners

---

## Technology Stack

### **v0.0 (Current)**
- **Video**: FFmpeg (local rendering)
- **Voice**: Google Cloud TTS
- **Assets**: ComfyUI (GPU-based charts)
- **B-Roll**: Pexels/Pixabay stock footage
- **Data**: Google Sheets (flow_ledger.csv)
- **Workflow**: Manual-templated (bash scripts)

### **v0.2+ (Future)**
- **Automation**: n8n workflows
- **Data**: Postgres database
- **API**: TAB real-time polling
- **Voice**: ElevenLabs (better NZ accent)
- **Approval**: Telegram bot

---

## Vocabulary

### **Use This**
- "The Flow" (market data)
- "Heavy flow" (large volume)
- "Sectional rank" (performance metric)
- "Market participant" (not "punter")

### **Never Use**
- "The Tape" (deprecated)
- "Smart money" (we don't know intent)
- "Lock/Sure thing" (certainty language)
- "Tips/Picks" (gambling language)

**Full vocabulary guide**: See `01-VOICE.md`

---

## Success Metrics

### **v0.0 (After 12 weeks)**
- [OK] 12 consecutive weeks posted (no gaps)
- [OK] Professional quality (not amateur)
- [OK] Zero data errors
- [OK] Growing engagement (saves/shares)

### **v0.1 (After 8 weeks)**
- [OK] Goodwill with pundit audiences
- [OK] Tribal discussion starting
- [OK] Still seen as neutral referee

### **v0.2 (After 8 weeks)**
- [OK] Authority established
- [OK] Credibility intact despite controversy
- [OK] Audience growth accelerating

---

## File Locations

### **On S Drive (`/mnt/scratch/projects/`)**

```text
Asset_Generation/
├── broll/generic/ # Stock footage
├── images/ # Charts, horse photos
├── voice/ # MP3 voice-overs
├── final/ # Rendered videos
└── approved/ # Ready to post

Evolution_Studio/content/
├── scripts/ # Video scripts
└── data/
    └── flow_ledger.csv # TAB data tracking

.planning/evolution-content-factory/
├── 00-MISSION.md
├── 01-VOICE.md
└── [all planning docs]
```

---

## Quick Reference

### **Content Schedule (v0.0)**
- **Thursday**: Throwback Thursday (underdog story)
- **Friday**: Weekend Preview (5 biggest races)
- **Monday**: Weekend Recap (results + data)

### **Production Time**
- Script: 15 min
- Assets: 15 min
- Voice: 5 min
- Render: 10 min
- Review: 5 min
- Post: 5 min
**Total**: ~60 min per video

---

## Updates & Changes

**All changes logged in**: `CHANGELOG.md`

**Recent major changes**:
- 2026-01-14: Complete rebirth (new strategy, modular docs)
- 2026-01-13: "The Tape" -> "The Flow"
- 2026-01-13: Manual-templated workflow (not automated)
- 2026-01-13: Fight Club rule established

---

## Contact & Collaboration

**GitHub**: [Badders80/evolution-content-factory-docs](https://github.com/Badders80/evolution-content-factory-docs)

**Related Repos**:
- [Evolution-3.1](https://github.com/Badders80/Evolution-3.1) - Main website
- [Evolution_Studio](https://github.com/Badders80/Evolution_Studio) - Django CMS
- [Asset_Generation](https://github.com/Badders80/Asset_Generation) - ComfyUI workflows
- [Brand_Voice](https://github.com/Badders80/Brand_Voice) - Brand guidelines

---

## License

Internal documentation for Evolution Stables.  
Not for public distribution.

---

*Last Updated*: January 14, 2026, 12:00 AM NZDT  
*Status*: Documentation complete, ready for v0.0 execution

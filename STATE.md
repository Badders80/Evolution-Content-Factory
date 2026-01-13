# State: Current Decisions & Blockers

**Last Updated**: January 14, 2026, 12:00 AM NZDT  
**Current Phase**: Pre-v0.0 (Documentation & Setup)  
**Next Milestone**: First Preview video (Week 1)

---

## Current Status

### **Completed**
- [x] Mission clarification (Fight Club funnel strategy)
- [x] Voice guidelines (GTI single voice, "The Flow" terminology)
- [x] Systems architecture (S drive, manual-templated workflow)
- [x] Build roadmap (v0.0 -> v0.1 -> v0.2 -> backlog)
- [x] Documentation structure (modular, get-shit-done style)

### **In Progress**
- [ ] Create GitHub repo for planning docs
- [ ] Set up directory structure on S drive
- [ ] Download initial B-roll library (Pexels)
- [ ] Create FFmpeg render scripts
- [ ] Write first Preview script (test)

### **Blocked**
- None currently

---

## Recent Decisions

### **Decision 001: "The Tape" -> "The Flow"**
**Date**: January 13, 2026  
**Context**: "The Tape" is outdated 1980s finance slang  
**Decision**: Replace with "The Flow" throughout all content  
**Rationale**: Modern institutional term, more accessible  
**Impact**: All vocabulary updated in 01-VOICE.md

### **Decision 002: Manual-Templated > Full Automation**
**Date**: January 13, 2026  
**Context**: Original docs over-promised n8n automation  
**Decision**: Start with manual "hit run" workflow for v0.0  
**Rationale**: Learn rhythm before automating, realistic for 3-5 videos/week  
**Impact**: BUILD-v0.0.md reflects manual process

### **Decision 003: GTI = One Voice (Not Two Personas)**
**Date**: January 13, 2026  
**Context**: GTI/Q7 were positioned as separate personas  
**Decision**: ONE voice that matures from GTI -> Q7 over time  
**Rationale**: It's a journey, not two separate brands  
**Impact**: 01-VOICE.md updated, no Q7 separation

### **Decision 004: Fight Club Rule (No Ownership Talk)**
**Date**: January 13, 2026  
**Context**: Need to build audience before revealing syndication  
**Decision**: ZERO ownership mentions in v0.0, v0.1, v0.2 content  
**Rationale**: Capture GTI audience without sales pitch  
**Impact**: Deferred to v0.3 (24+ weeks out)

### **Decision 005: Google Sheets > Postgres (v0.0)**
**Date**: January 13, 2026  
**Context**: Flow data needs simple MVP storage  
**Decision**: Start with Google Sheets CSV, migrate later  
**Rationale**: MCP-friendly, Excel-compatible, easy to maintain  
**Impact**: flow_ledger.csv structure defined

### **Decision 006: Pexels B-Roll > Own Footage (v0.0)**
**Date**: January 13, 2026  
**Context**: Need B-roll library quickly  
**Decision**: Use Pexels/Pixabay stock footage initially  
**Rationale**: Fly under radar, avoid TAB/NZTR copyright issues  
**Impact**: Generic racing footage acceptable for v0.0

---

## Active Questions

### **Q1: When to start TAB data collection?**
**Status**: Open  
**Context**: Need historical flow data for v0.1  
**Options**:
- A) Start manual collection now (Google Sheets after each race day)
- B) Wait until automated (TAB API integration)
**Recommendation**: Option A - start manually, small time investment  
**Decision Needed By**: Week 1 of v0.0

### **Q2: Which voice for Google TTS?**
**Status**: Open  
**Context**: Need to choose voice profile  
**Options**:
- A) `en-AU-Neural2-B` (Aussie male, close to Kiwi)
- B) `en-AU-Neural2-D` (Aussie male, deeper)
- C) Test both, decide based on output
**Recommendation**: Option C - test both in first video  
**Decision Needed By**: Week 1 of v0.0

### **Q3: Posting frequency in v0.0?**
**Status**: Open  
**Context**: Balancing quality vs consistency  
**Options**:
- A) 3 videos/week (Preview, Recap, Throwback)
- B) 2 videos/week (Preview, Recap only - drop Throwback)
- C) 1 video/week (nail quality before frequency)
**Recommendation**: Option A if sustainable, Option B if time-constrained  
**Decision Needed By**: End of Week 2

---

## Known Risks

### **Risk 001: Quality vs Speed Trade-off**
**Probability**: High  
**Impact**: Medium  
**Mitigation**: Start with 1-2 videos/week, increase once workflow smooth

### **Risk 002: B-Roll Repetition**
**Probability**: Medium  
**Impact**: Low  
**Mitigation**: Download 50+ clips upfront, rotate frequently

### **Risk 003: Voice Quality (Google TTS Limitations)**
**Probability**: Medium  
**Impact**: Medium  
**Mitigation**: Test multiple voices, consider ElevenLabs if needed (v0.1+)

### **Risk 004: Pundit Backlash (v0.1)**
**Probability**: Low (if v0.0 credibility established)  
**Impact**: High  
**Mitigation**: Neutral tone, goodwill building, receipts for every claim

---

## Next Actions (This Week)

1. **Create GitHub repo**: `evolution-content-factory-docs`
2. **Set up S drive structure**: Run directory creation commands
3. **Download B-roll library**: 20-30 clips from Pexels
4. **Write first script**: Use TEMPLATE-preview.md, test Ellerslie R7
5. **Create FFmpeg script**: Test render pipeline
6. **Generate test video**: Full workflow test (script -> voice -> render)
7. **Review & iterate**: Refine before Week 1 launch

---

## Future State Reviews

**Week 4**: Review v0.0 progress, adjust workflow  
**Week 8**: Halfway audit, quality check  
**Week 12**: v0.0 completion audit, v0.1 readiness check

---

*This file is living documentation - update after every major decision or milestone*

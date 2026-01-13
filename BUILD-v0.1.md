# BUILD v0.1: Content-of-Content

**Status**: Next Phase (After v0.0 Success)  
**Goal**: Pundit performance tracking without controversy  
**Prerequisite**: 12 weeks of credible v0.0 content

---

## Entry Criteria

**DO NOT start v0.1 until**:
- [OK] 12+ weeks of consistent v0.0 content
- [OK] Professional video quality established
- [OK] Growing engagement (saves/shares/comments)
- [OK] Zero data accuracy issues
- [OK] TAB flow data collected (background)

**If any of these are NO, stay in v0.0.**

---

## New Content Type: Pundit Recap

### **Monday: Pundit Performance**
**Format**: 40-60 seconds, vertical (1080x1920)  
**Frequency**: 1x per week (in addition to regular recap)  
**Structure**:
- Hook (0-5s): "Here's how the experts went this weekend"
- Analysis (5-45s): Aggregate predictions, match to results
- Close (45-60s): Factual summary (NO judgment yet)

**Example**:
> "This weekend: BGP backed 5 horses, 3 won. TAB Form backed 4, 2 won. ACC backed 3, 1 won. Here's the data."

---

## What Makes v0.1 Different

### **Still Content-of-Content**
- You're reporting facts (who said what, what happened)
- You're NOT judging quality yet
- You're NOT making leaderboards public

### **Zero Risk Approach**
- Aggregate existing predictions (BGP, TAB, ACC, SENZ)
- Match to actual results
- Report the facts neutrally

### **Building the Ledger**
- Every prediction tracked in `flow_ledger.csv`
- Accuracy calculated over time
- Data accumulates for v0.2 (public leaderboards)

---

## Production Workflow

### **Data Collection** (30 min/week)
1. **Thursday-Friday**: Scrape pundit predictions
   - BGP (Best Game Plan)
   - TAB Form Analyst
   - ACC (Adrian Clark Commentary)
   - SENZ Radio picks
2. Save to: `flow_ledger.csv`
3. Format: `expert_id, source, horse_name, race, confidence, timestamp`

### **Monday Processing** (20 min)
1. Match predictions to actual results
2. Calculate: Win/Place/Unplaced for each expert
3. Generate summary: "BGP: 3/5 wins, ACC: 1/3 wins"

### **Video Creation** (60 min)
1. Script: Use `TEMPLATE-pundit-recap.md`
2. Voice: Google TTS
3. Visuals: Simple bar chart (ComfyUI)
4. Render: FFmpeg
5. Post: TikTok/X/Instagram

---

## NZ Racing Pundits to Track

### **Primary Sources**
1. **BGP (Best Game Plan)** - Dan Parker
   - Website + social feeds
   - High engagement, loyal audience

2. **TAB Form Analyst** - Official TAB picks
   - TAB website, published Thu/Fri
   - Industry authority

3. **ACC (Adrian Clark Commentary)** - Independent analyst
   - Social media, high engagement
   - Strong community following

4. **SENZ Radio** - Live race analysis
   - Radio broadcasts, social clips
   - Traditional media credibility

### **Secondary Sources** (Optional)
- NZTW (NZ Thoroughbred Writer)
- LoveRacing NZ (community sentiment)
- The Leg Up (if accessible)

---

## Expert Ledger Schema

**CSV Structure** (`flow_ledger.csv`):
```csv
date,expert_id,source,venue,race_num,horse_name,confidence,predicted_place,actual_result,roi_if_bet,notes
2026-01-18,BGP-001,BGP,Ellerslie,7,Horse X,best_bet,win,1st,+340,"Strong conviction"
2026-01-18,TAB-001,TAB Form,Ellerslie,7,Horse Y,each_way,place,4th,-100,"Wide barrier"
```

Key Fields:
- `expert_id`: Unique identifier (BGP-001, TAB-001, etc.)
- `confidence`: best_bet, each_way, saver, mention
- `actual_result`: 1st, 2nd, 3rd, unplaced
- `roi_if_bet`: Calculated return if $1 unit placed

---

## Tone & Voice Guidelines

### **Neutral Reporting**
OK: "BGP backed 5 horses this weekend. 3 won, 2 were unplaced."  
NO: "BGP crushed it this weekend-follow them!"

### **Factual, Not Judgmental**
OK: "ACC had a 33% strike rate this week."  
NO: "ACC had a terrible week-avoid their picks."

### **Celebratory When Appropriate**
OK: "BGP found the outsider at Trentham-$18 winner."  
NO: "BGP got lucky with that fluke win."

Why: Build goodwill with pundit audiences. You're the neutral scorekeeper, not a critic.

---

## Success Criteria (v0.1)

After 8 weeks of pundit tracking:
- [OK] Engagement higher than v0.0 baseline?
- [OK] Comments from pundit audiences (tribal discussion)?
- [OK] Zero backlash (still seen as neutral)?
- [OK] Historical data robust (8+ weeks of tracking)?

If YES: Move to v0.2 (public leaderboards).  
If NO: Continue v0.1, refine approach.

---

## What We're Still NOT Doing

Deferred to v0.2:
- Public leaderboards (tribal engagement)
- Ranking pundits by accuracy
- Making judgments about quality
- Ownership mentions (Fight Club rule continues)

Focus: Neutral reporting, data collection, goodwill building.

---

## Risk Management

### **If Pundit Pushback Occurs**
- Immediately reach out via DM/email
- Offer to remove their data if requested
- Emphasize: "We're just reporting facts, celebrating wins"
- If they're hostile: Remove them from tracking immediately

### **If Audience Backlash Occurs**
- Acknowledge: "We're learning, feedback appreciated"
- Double-down on neutrality: "Just showing the data"
- Do NOT get defensive or argumentative

### **If Data Accuracy Questioned**
- Have receipts: Screenshots of original predictions
- Publish methodology: How you track, what counts as "win"
- Offer corrections: "If we got this wrong, we'll fix it"

---

*Phase Duration*: 8 weeks  
*Entry Requirement*: v0.0 success criteria met  
*Review Date*: After 8 weeks of pundit tracking  
*Decision Point*: Move to v0.2 only if engagement + goodwill established

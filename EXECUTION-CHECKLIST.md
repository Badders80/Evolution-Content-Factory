# Complete Execution Checklist

Document everything now, use what you need for v0.0, ignore the rest until later.

---

## Part 1: Directory Structure (Run in Terminal First)

```bash
# Navigate to your workspace
cd /mnt/scratch/projects

# Create planning docs directory
mkdir -p .planning/evolution-content-factory/templates

# Create Asset_Generation structure
mkdir -p Asset_Generation/{broll/generic,images/{horses,charts},voice,final,approved,templates}

# Create Evolution_Studio content structure
mkdir -p Evolution_Studio/content/{scripts,data,templates}

# Create vault structure (future-proofing)
mkdir -p vault/Evolution_Brain/{brand,tech,product,agents,memory/{daily_logs,decision_records},content-factory/templates,.system}

# Verify structure created
ls -la /mnt/scratch/projects/.planning/evolution-content-factory/
ls -la /mnt/scratch/projects/Asset_Generation/
ls -la /mnt/scratch/vault/Evolution_Brain/
```

---

## Part 2: Files to Create in VS Code (Copy-Paste)

Open VS Code in the planning directory:

```bash
cd /mnt/scratch/projects/.planning/evolution-content-factory
code .
```

### Create Now - Use Now (v0.0 Essentials)

These 11 files you will actively use starting Week 1:

| # | File | Status | Purpose |
|---|------|--------|---------|
| 1 | README.md | Use now | Quick start guide, overview |
| 2 | 00-MISSION.md | Use now | Fight Club strategy, funnel concept |
| 3 | 01-VOICE.md | Use now | Voice guidelines, vocabulary, banned terms |
| 4 | 02-SYSTEMS.md | Use now | S drive structure, manual workflow |
| 5 | BUILD-v0.0.md | Use now | Current phase (Preview/Recap/Throwback) |
| 6 | STATE.md | Use now | Living decisions log (update weekly) |
| 7 | CHANGELOG.md | Use now | Track vocabulary/strategy changes |
| 8 | templates/TEMPLATE-preview.md | Use now | Preview script template |
| 9 | templates/TEMPLATE-recap.md | Use now | Recap script template |
| 10 | templates/TEMPLATE-throwback.md | Use now | Throwback script template |
| 11 | .gitignore | Use now | Git exclusions |

Copy-paste the content provided earlier for each of these.

### Create Now - Use Later (v0.1-v0.2)

These 5 files document future phases (reference only for now):

| # | File | Status | Use When |
|---|------|--------|----------|
| 12 | BUILD-v0.1.md | Reference | Week 13+ (after v0.0 success) |
| 13 | BUILD-v0.2.md | Reference | Week 21+ (after v0.1 success) |
| 14 | BACKLOG.md | Reference | Week 29+ (v0.3 ownership reveal) |
| 15 | templates/TEMPLATE-pundit-recap.md | Reference | v0.1 (pundit tracking phase) |
| 16 | LICENSE.md | Reference | Internal use policy |

### Create Now - Future Integration (v0.1+ Infrastructure)

These 3 files bridge to Master Config and future automation:

| # | File | Location | Status | Use When |
|---|------|----------|--------|----------|
| 17 | hardware.md | /vault/Evolution_Brain/tech/ | Future | v0.1 (when MCP added) |
| 18 | write_policy.json | /vault/Evolution_Brain/.system/ | Future | v0.2 (when AI writes memory) |
| 19 | COMFYUI_NOTES.md | /mnt/scratch/projects/Asset_Generation/ | Use now | ComfyUI chart generation reference |

---

## Part 3: Complete File Creation Checklist

In VS Code Terminal or WSL:

```bash
# Navigate to planning docs
cd /mnt/scratch/projects/.planning/evolution-content-factory

# Create all main docs (paste content from above)
touch README.md
touch 00-MISSION.md
touch 01-VOICE.md
touch 02-SYSTEMS.md
touch BUILD-v0.0.md
touch BUILD-v0.1.md
touch BUILD-v0.2.md
touch BACKLOG.md
touch STATE.md
touch CHANGELOG.md
touch .gitignore
touch LICENSE.md

# Create templates
touch templates/TEMPLATE-preview.md
touch templates/TEMPLATE-recap.md
touch templates/TEMPLATE-throwback.md
touch templates/TEMPLATE-pundit-recap.md

# Create Asset_Generation reference
touch /mnt/scratch/projects/Asset_Generation/COMFYUI_NOTES.md

# Create vault tech docs (future-proofing)
touch /mnt/scratch/vault/Evolution_Brain/tech/hardware.md
touch /mnt/scratch/vault/Evolution_Brain/.system/write_policy.json

echo "All 19 files created. Ready for content paste."
```

---

## Part 4: What You Do in VS Code

For each file:
- Click the filename in the VS Code explorer
- Copy the markdown or JSON content provided
- Paste into the file
- Save (Ctrl+S)
- Move to the next file

Order does not matter - just get all 19 filled.

---

## Part 5: File Usage Guide

### Use These Now (v0.0 Active)

When creating content, reference:
- 00-MISSION.md - Fight Club rule
- 01-VOICE.md - Vocabulary, banned terms
- BUILD-v0.0.md - v0.0 workflow steps
- templates/TEMPLATE-*.md - Use for every video script
- COMFYUI_NOTES.md - When generating charts

Update weekly:
- STATE.md - Decisions, blockers, progress
- CHANGELOG.md - Vocabulary or strategy changes

### Reference Only (v0.1-v0.2 Future)

Do not actively use yet, but they are documented:
- BUILD-v0.1.md - Read Week 12 before starting pundit tracking
- BUILD-v0.2.md - Read Week 20 before launching leaderboards
- BACKLOG.md - Ideas for v0.3+ (ownership reveal)
- templates/TEMPLATE-pundit-recap.md - For v0.1 pundit content

### Future Infrastructure (v0.1+ Integration)

These exist for when MCP/automation is added:
- /vault/Evolution_Brain/tech/hardware.md - Machine-readable constraints
- /vault/Evolution_Brain/.system/write_policy.json - AI write permissions

Referenced but not actively used until v0.1+.

---

## Part 6: After Creation - Git Setup

```bash
# Navigate to planning docs
cd /mnt/scratch/projects/.planning/evolution-content-factory

# Initialize git
git init

# Add all files
git add .

# Initial commit
git commit -m "docs: Initial commit - Evolution Content Factory v0.0 (Rebirth)"

# Create GitHub repo (via web or CLI)
# Then push:
git remote add origin https://github.com/Badders80/evolution-content-factory-docs.git
git branch -M main
git push -u origin main
```

---

## Final Summary

### What You Are Creating (19 Total Files)

Active use now (11 files):
- Core docs + templates used every week

Reference for later (5 files):
- v0.1 and v0.2 docs, backlog, pundit recap template, license

Infrastructure bridge (3 files):
- Master config integration for MCP/automation (v0.1+)

### What This Achieves

- v0.0 execution ready: Templates and workflow documented
- Future-proofed: v0.1, v0.2, backlog mapped
- Hardware-aware: Master config integrated
- Git-ready: Can commit to repo immediately
- MCP-ready: Vault structure in place for v0.1+
- Simple now, scalable later: No over-engineering

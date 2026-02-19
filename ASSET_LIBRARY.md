# Evolution Content Factory - Asset Library

## Storage Locations

**Primary (Fast/Local):**
- S:\Evolution-Content-Factory\
- WSL Path: /mnt/s/Evolution-Content-Factory/

**Archive/Shared (Google Drive):**
- G:\Shared drives\Evolution Stables\Evolution Tokinvest\

---

## Folder Structure

```
Evolution-Content-Factory/
├── renders/              # Final video outputs
├── cache/                # FFmpeg proxies, temp files
├── workspace/            # Active projects
└── assets/
    ├── brand/            # Evolution Stables & Tokinvest logos
    ├── b-roll/           # Generic horse footage (galloping, training)
    ├── templates/        # Reusable slide decks
    └── horses/           # Per-horse assets
        └── [horse-name]/
            ├── photos/   # Horse photos
            ├── videos/   # Training/race footage
            └── renders/  # Final reels for this horse
```

---

## Brand Assets

| Asset | File | Usage |
|-------|------|-------|
| Evolution Gold Logo | Evo_Logo_MonoGold.png | Opening slides, watermarks |
| Evolution Full Logo | Evo_Logo_Full.png | Full branding |
| Evolution White/Green | Evo_Logo_WhiteGreen.png | Dark backgrounds |
| Evolution Black/Green | Evo_Logo_BlackGreen.png | Light backgrounds |
| Evolution Name (SVG) | Evolution-Stables-Name-Logo-Gold.svg | Typography |

---

## Current Horses

### Prudentia
- **Photos:** 3 (13Feb2026-001/002/003.JPG)
- **Videos:** Training footage + Race (Tauranga Maiden)
- **Pedigree:** Proisir (sire), Little Bit Irish (dam)
- **Renders:** Prudentia_Slides_Final.mp4

---

## B-Roll Categories (To Build)

- [ ] Galloping (various track conditions)
- [ ] Training (morning workouts)
- [ ] Barrier loading
- [ ] Finish line crossings
- [ ] Jockey close-ups
- [ ] Crowd reactions
- [ ] Track walks

---

## Slide Templates (To Build)

- [ ] Opening slide (Evo + Tokinvest)
- [ ] Horse profile slide
- [ ] Pedigree infographic
- [ ] Race result slide
- [ ] CTA slide

---

## Next Steps

1. Set up sync to G: Drive for team sharing
2. Build searchable asset database (Supabase)
3. Add vector embeddings for semantic search
4. Create B-roll generation pipeline


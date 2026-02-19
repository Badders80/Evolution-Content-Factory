# Evolution Studio - Leverageable Components

## What I Found in Evolution_Studio Repo

### 1. PressRoom Module (`modules/press_room.py`)
**What it does:**
- Generates HTML reports from structured "blocks"
- Block types: heading, subheading, body, bullets, grey_box (media+quote+name)
- Professional styling with Evolution branding
- Outputs complete HTML with SVG watermarks

**How we can leverage:**
```python
from modules.press_room import PressRoom

press_room = PressRoom()
blocks = [
    {"type": "heading", "content": "Prudentia Wins Tauranga Maiden"},
    {"type": "subheading", "content": "1st Place | 28 May 2025"},
    {"type": "body", "content": "The 4yo filly showed tremendous heart..."},
    {"type": "bullets", "content": "By Proisir\nTrained at Wexford\n1400m specialist"}
]

html = press_room.generate_report(blocks, "Race Result")
# Use HTML to generate slide images or web content
```

### 2. Block-Based Content Parser (`app.py`)
**What it does:**
- Parses raw text with keywords: HEADING, SUBHEADING, BODY, BULLETS, MEDIA, QUOTE, NAME
- Groups related content into structured blocks
- Streamlit UI for interactive editing

**How we can leverage:**
```
Input text:
HEADING
Prudentia Wins!

SUBHEADING  
1st Place at Tauranga

BODY
The filly showed tremendous speed...

BULLETS
- By Proisir
- 1400m specialist
- Trained at Wexford

↓

Parsed blocks for slide generation or reel scripting
```

### 3. HTML Templates (`assets/templates/`)
- `report_a4.html` - A4 print-ready layout
- `report_template.html` - Web-friendly layout
- Uses Geist Sans, Playfair Display fonts (matches Evolution brand)
- SVG watermarks and logos

**How we can leverage:**
- Convert HTML to images for slide backgrounds
- Use as base for HTML-to-video slides
- Extract CSS for consistent styling

### 4. Horse Repository Structure
- Django models for horses
- Could store horse profiles, race data

**How we can leverage:**
- Integrate with Content Factory asset library
- Store generated reels metadata
- Link to Research Engine data

---

## Integration Opportunities

### Option 1: Content Generation Pipeline
```
Research Engine data
    ↓
PressRoom blocks (structured content)
    ↓
HTML generation
    ↓
HTML → Image (Chromium/Playwright)
    ↓
Ken Burns animation (FFmpeg)
    ↓
Slide video
```

### Option 2: Slide Text Generator
```
Input: Horse name + race result
    ↓
AI generates block structure
    ↓
PressRoom.generate_report()
    ↓
Extract text for overlays
    ↓
FFmpeg composite with video
```

### Option 3: Web Preview
```
Generate reel in Content Factory
    ↓
Also generate web version via PressRoom
    ↓
Investors can view detailed write-up
    ↓
Links in reel description
```

---

## Immediate Actions

### What I can copy/integrate now:
1. ✅ `modules/press_room.py` - Content generation engine
2. ✅ `assets/templates/` - HTML/CSS styling
3. ✅ Block parsing logic from `app.py`

### What needs adaptation:
1. Django models → Plain Python/JSON
2. Streamlit UI → CLI/API
3. HTML → Video slides (add Chromium rendering)

---

## Recommendation

**Copy PressRoom into Content Factory as content generation layer:**

```
Evolution-Content-Factory/
├── content_generation/
│   ├── press_room.py          # From Evolution_Studio
│   ├── block_parser.py        # From app.py
│   └── templates/             # From assets/
```

**Use for:**
- Auto-generating slide text from race data
- Creating HTML previews of reels
- Consistent brand voice across all content

**Next step:** Should I copy PressRoom into Content Factory and integrate with the Auto-Reel Builder?

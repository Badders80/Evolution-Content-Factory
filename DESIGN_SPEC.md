# Evolution Content Factory - Video Design Specification

## Overview
Professional horse racing reels that tell a story with cinematic quality, smooth transitions, and engaging graphics.

## Visual Style
- **Aspect Ratio:** 9:16 (1080x1920) vertical
- **Frame Rate:** 25fps
- **Color Palette:** 
  - Primary: Gold (#D4AF37) - Evolution Stables brand
  - Secondary: Deep Black (#0A0A0A)
  - Accent: Racing Green (#1B4D3E)
  - Text: White with soft shadow

## Typography
- **Headlines:** Bold, all caps, tracking wide
- **Body:** Clean sans-serif, sentence case
- **Stats:** Monospace for numbers

## Transitions (FFmpeg Implementation)

### 1. Crossfade (Default)
```
fade=t=out:st={start}:d=0.5, fade=t=in:st={next_start}:d=0.5
```
Duration: 0.5 seconds
Use: Standard scene changes

### 2. Zoom In (Impact)
```
zoompan=z='min(zoom+0.0015,1.5)':d={duration*25}:s=1080x1920
```
Use: Introducing important moments

### 3. Slide (Directional)
```
transition={direction}:duration=0.5:offset={offset}
```
Directions: left, right, up, down
Use: Moving between topics

### 4. Match Cut
Hard cut with visual similarity
Use: Race action to training footage

## Text Animations

### Lower Third
- Background: Semi-transparent black bar (alpha 0.7)
- Text: Fade up from bottom
- Duration: 2-3 seconds
- Position: Bottom 15% of frame

### Title Card
- Full screen overlay
- Large typography (72px+)
- Animated entrance (scale + fade)

### Stats Overlay
- Numbers animate (count up)
- Gold accent color
- Position: Upper third or center

## Graphic Elements

### 1. Pedigree Chart
```
Visual family tree:
    [Proisir]
       |
   [Prudentia] --- [Little Bit Irish]
       |
    [Cork] (sister)
```
Implementation: Pre-designed PNG overlays

### 2. Stats Cards
- Horse silhouette icon
- Key stats in clean layout:
  - Age: 4yo
  - Trainer: Wexford Stables
  - Best: Heavy tracks
  - Win: Tauranga Maiden

### 3. Name Plates
- Gold border
- Elegant serif font for horse name
- Sans-serif for subtitle

## Scene Structure Template

### Scene 1: Introduction (5s)
- **Visual:** Photo 1 with Ken Burns effect (slow zoom)
- **Text:** Horse name + key descriptor
- **Animation:** Fade up from bottom
- **Transition:** Zoom in to next scene

### Scene 2: Pedigree (10s)
- **Visual:** Photo 2
- **Text:** Sire/Dam info
- **Graphic:** Pedigree overlay (animated lines connecting)
- **Transition:** Slide right

### Scene 3: The Win (20s)
- **Visual:** Race footage
- **Text:** Race details (synced to action)
- **Effect:** Speed ramp - slow motion at finish
- **Transition:** Match cut to training

### Scene 4: Behind the Scenes (15s)
- **Visual:** Training footage
- **Text:** Team credits
- **Animation:** Lower thirds for each name
- **Transition:** Crossfade

### Scene 5: Call to Action (10s)
- **Visual:** Photo 3 (hero shot)
- **Text:** Hook + CTA
- **Graphic:** Tokinvest logo + "Available Now"
- **Animation:** Scale up on text

## FFmpeg Filter Complex Examples

### Ken Burns on Still Image
```
ffmpeg -i image.jpg -vf "zoompan=z='min(zoom+0.0015,1.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1080x1920" -t 5 output.mp4
```

### Lower Third Overlay
```
ffmpeg -i video.mp4 -vf "drawtext=text='Prudentia':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=h-text_h-150:box=1:boxcolor=black@0.7:boxborderw=10:enable='between(t,0,3)'" output.mp4
```

### Crossfade Between Clips
```
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "[0:v]fade=out:st=4:d=1[va];[1:v]fade=in:st=0:d=1[vb];[va][vb]concat=n=2:v=1:a=0" output.mp4
```

### Color Grading (Cinematic)
```
ffmpeg -i input.mp4 -vf "eq=contrast=1.1:saturation=1.2:brightness=0.05,lut3d='film_lut.cube'" output.mp4
```

## Asset Requirements

### Required Graphics (PNG with Alpha)
1. `pedigree_frame.png` - Family tree template
2. `lower_third_bg.png` - Text background bar
3. `stats_card.png` - Stats overlay template
4. `logo_watermark.png` - Evolution Stables logo
5. `transition_wipe.png` - Wipe transition mask

### Fonts
1. `Montserrat-Bold.ttf` - Headlines
2. `PlayfairDisplay-Regular.ttf` - Horse names (elegant)
3. `RobotoMono-Regular.ttf` - Stats/numbers

## Music & Audio

### Structure
- 0-5s: Intro build (ambient, anticipation)
- 5-35s: Main theme (driving, energetic)
- 35-50s: Emotional moment (strings, reflective)
- 50-60s: Climax + outro (triumphant, CTA)

### Voiceover
- Clean, documentary style
- Slight reverb for space
- EQ: Roll off below 80Hz, boost clarity at 3kHz

## Quality Checklist

Before rendering:
- [ ] All transitions smooth (no jarring cuts)
- [ ] Text readable on all backgrounds
- [ ] Audio levels consistent (-14 LUFS)
- [ ] Color grading applied consistently
- [ ] Logo/watermark present (subtle)
- [ ] End card with CTA clear

## Implementation Priority

### Phase 1: Basic (Current)
- Concatenate clips
- Simple text overlay
- ✓ Working

### Phase 2: Enhanced (Next)
- Image to video with Ken Burns
- Crossfade transitions
- Lower thirds styling
- Better text animations

### Phase 3: Professional
- Custom graphics overlays
- Color grading LUTs
- Advanced transitions (zoom, slide)
- Audio mixing

### Phase 4: Premium
- Motion graphics (pedigree animations)
- Dynamic text tracking
- Multi-layer compositing
- Custom transitions per template

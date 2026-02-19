#!/bin/bash
# Batch Ken Burns Generator
# Creates animated videos from still images for B-roll library

INPUT_DIR="/mnt/s/Evolution-Content-Factory/assets/b-roll/ken-burns"
OUTPUT_DIR="/mnt/s/Evolution-Content-Factory/assets/b-roll/generated"
mkdir -p $OUTPUT_DIR

echo "🎬 Generating Ken Burns B-roll from images..."

# Function to create Ken Burns video
# Args: input_image output_name zoom_start zoom_end duration
create_ken_burns() {
    local input=$1
    local output=$2
    local zoom_start=$3
    local zoom_end=$4
    local duration=$5
    
    ffmpeg -y -loop 1 -i "$input" \
        -vf "zoompan=z='if(lte(on,1),$zoom_start,max($zoom_end,zoom-0.002))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$(($duration*30)):s=1080x1920,setsar=1:1" \
        -c:v libx264 -pix_fmt yuv420p -crf 18 -t $duration \
        "$output" 2>/dev/null
}

# Generate multiple variations per image

echo "1. Prudentia photos (3 variations each)..."

# Prudentia 001 - Zoom OUT ( reveal)
create_ken_burns "$INPUT_DIR/prudentia/Prudentia-13Feb2026-001.JPG" \
    "$OUTPUT_DIR/prudentia_001_zoom_out.mp4" 1.3 1.0 5

# Prudentia 001 - Pan RIGHT
create_ken_burns "$INPUT_DIR/prudentia/Prudentia-13Feb2026-001.JPG" \
    "$OUTPUT_DIR/prudentia_001_pan_right.mp4" 1.15 1.15 5

# Prudentia 002 - Zoom IN (focus)
create_ken_burns "$INPUT_DIR/prudentia/Prudentia-13Feb2026-002.JPG" \
    "$OUTPUT_DIR/prudentia_002_zoom_in.mp4" 1.0 1.25 5

# Prudentia 003 - Slow zoom + pan
create_ken_burns "$INPUT_DIR/prudentia/Prudentia-13Feb2026-003.JPG" \
    "$OUTPUT_DIR/prudentia_003_slow.mp4" 1.2 1.05 7

echo "2. Sire/Dam photos..."

# Proisir - dignified zoom out
create_ken_burns "$INPUT_DIR/sire-dam/Proisir_Sire.png" \
    "$OUTPUT_DIR/proisir_heritage.mp4" 1.25 1.0 6

# Little Bit Irish - gentle zoom
create_ken_burns "$INPUT_DIR/sire-dam/LittleBitIrish_Dam.png" \
    "$OUTPUT_DIR/little_bit_irish_heritage.mp4" 1.2 1.0 6

echo "3. Background images..."

# Hooves - slow atmospheric
create_ken_burns "$INPUT_DIR/backgrounds/Background-hooves-back-and-white.jpg" \
    "$OUTPUT_DIR/hooves_atmospheric.mp4" 1.15 1.0 8

# Horse and foal - warm zoom out
create_ken_burns "$INPUT_DIR/backgrounds/Horse-and-foal.jpg" \
    "$OUTPUT_DIR/horse_foal_warm.mp4" 1.3 1.0 6

# Landscape - wide establishing
create_ken_burns "$INPUT_DIR/backgrounds/Landscape-digitaloverlay.jpg" \
    "$OUTPUT_DIR/landscape_establishing.mp4" 1.0 1.2 10

echo "✅ Generated $(ls -1 $OUTPUT_DIR/*.mp4 2>/dev/null | wc -l) Ken Burns B-roll clips"
echo ""
echo "Library: $OUTPUT_DIR"
ls -lh $OUTPUT_DIR/*.mp4 | awk '{print $9, $5}'

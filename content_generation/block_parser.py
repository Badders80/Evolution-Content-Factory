"""
Block Parser - Adapted from Evolution Studio
Parses structured text into blocks for content generation
"""

from typing import List, Dict

class BlockParser:
    """Parse text with HEADING, SUBHEADING, BODY, BULLETS keywords into blocks"""
    
    def __init__(self):
        self.keywords = ["HEADING", "SUBHEADING", "BODY", "BULLETS", "BULLET", "MEDIA", "QUOTE", "NAME"]
    
    def parse(self, text: str) -> List[Dict]:
        """
        Parse raw text into structured blocks
        
        Example input:
            HEADING
            Prudentia Wins!
            
            SUBHEADING
            1st Place at Tauranga
            
            BODY
            The filly showed speed...
        
        Returns:
            [{"type": "heading", "content": "Prudentia Wins!"}, ...]
        """
        if not text or not text.strip():
            return []
        
        lines = text.splitlines()
        segments = []
        current_key = None
        buffer = []
        
        # Tokenize
        for line in lines:
            clean = line.strip()
            upper = clean.upper()
            
            if upper in self.keywords:
                # Save previous segment
                if current_key:
                    content = "\n".join(buffer).strip()
                    if content:
                        normalized = "bullets" if current_key in ("BULLET", "BULLETS") else current_key.lower()
                        segments.append({"type": normalized, "content": content})
                
                current_key = upper
                buffer = []
            else:
                if current_key:
                    buffer.append(clean)
        
        # Don't forget last segment
        if current_key and buffer:
            content = "\n".join(buffer).strip()
            if content:
                normalized = "bullets" if current_key in ("BULLET", "BULLETS") else current_key.lower()
                segments.append({"type": normalized, "content": content})
        
        return segments
    
    def to_slide_text(self, blocks: List[Dict]) -> Dict:
        """
        Convert blocks to slide-ready text
        Returns dict with title, subtitle, body, bullets
        """
        result = {
            "title": "",
            "subtitle": "",
            "body": "",
            "bullets": [],
            "quote": "",
            "name": ""
        }
        
        for block in blocks:
            btype = block.get("type", "")
            content = block.get("content", "")
            
            if btype == "heading":
                result["title"] = content
            elif btype == "subheading":
                result["subtitle"] = content
            elif btype == "body":
                result["body"] = content
            elif btype == "bullets":
                result["bullets"] = [b.strip() for b in content.split("\n") if b.strip()]
            elif btype == "quote":
                result["quote"] = content
            elif btype == "name":
                result["name"] = content
        
        return result

if __name__ == "__main__":
    # Demo
    parser = BlockParser()
    
    sample = """
HEADING
Prudentia Wins Tauranga Maiden!

SUBHEADING
1st Place | 28 May 2025 | 1400m

BODY
The 4yo filly by Proisir showed tremendous heart in her maiden victory, powering home in the final 200m to win by 1.5 lengths.

BULLETS
- By Proisir (sire)
- Out of Little Bit Irish (dam)
- Trained at Wexford Stables
- Heavy track specialist

QUOTE
She's got the heart of a champion.

NAME
— Trainer, Wexford Stables
"""
    
    blocks = parser.parse(sample)
    print("Parsed blocks:")
    for b in blocks:
        print(f"  {b['type']}: {b['content'][:50]}...")
    
    slide_data = parser.to_slide_text(blocks)
    print("\nSlide data:")
    print(f"  Title: {slide_data['title']}")
    print(f"  Subtitle: {slide_data['subtitle']}")
    print(f"  Bullets: {slide_data['bullets']}")

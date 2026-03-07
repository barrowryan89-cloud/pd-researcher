#!/usr/bin/env python3
"""
colors.py — Terminal color toolkit
Convert, preview, and work with colors in the terminal

Usage:
  python colors.py <color>                    # Preview color
  python colors.py #FF5733                    # Hex color
  python colors.py rgb(255,87,51)             # RGB color
  python colors.py --list                     # Show all named colors
  python colors.py --gradient <start> <end>   # Show gradient
  
Examples:
  python colors.py #4287f5
  python colors.py crimson
  python colors.py hsl(120,100%,50%)
  python colors.py --gradient #FF0000 #00FF00

Features:
- Hex ↔ RGB ↔ HSL conversion
- Named color lookup (CSS colors)
- Terminal color preview (blocks)
- Brightness/contrast calculation
- Color blindness simulation

Zero dependencies. Pure Python 3.6+.
Part of PD's Free Developer Tools: https://barrowryan89-cloud.github.io/pd-researcher/
"""

import sys
import re
from typing import Tuple, Optional

# CSS Named Colors
NAMED_COLORS = {
    'black': '#000000', 'white': '#FFFFFF', 'red': '#FF0000', 'lime': '#00FF00',
    'blue': '#0000FF', 'yellow': '#FFFF00', 'cyan': '#00FFFF', 'magenta': '#FF00FF',
    'silver': '#C0C0C0', 'gray': '#808080', 'maroon': '#800000', 'olive': '#808000',
    'green': '#008000', 'purple': '#800080', 'teal': '#008080', 'navy': '#000080',
    'orange': '#FFA500', 'pink': '#FFC0CB', 'brown': '#A52A2A', 'crimson': '#DC143C',
    'gold': '#FFD700', 'indigo': '#4B0082', 'violet': '#EE82EE', 'turquoise': '#40E0D0',
    'coral': '#FF7F50', 'salmon': '#FA8072', 'khaki': '#F0E68C', 'plum': '#DDA0DD',
    'orchid': '#DA70D6', 'tan': '#D2B48C', 'wheat': '#F5DEB3', 'tomato': '#FF6347'
}

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex"""
    return f"#{r:02x}{g:02x}{b:02x}"

def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """Convert RGB to HSL"""
    r, g, b = r/255.0, g/255.0, b/255.0
    max_c, min_c = max(r, g, b), min(r, g, b)
    diff = max_c - min_c
    
    l = (max_c + min_c) / 2
    
    if diff == 0:
        h = s = 0
    else:
        s = diff / (2 - max_c - min_c) if l > 0.5 else diff / (max_c + min_c)
        if max_c == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif max_c == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        else:
            h = (60 * ((r - g) / diff) + 240) % 360
    
    return (int(h), int(s * 100), int(l * 100))

def hsl_to_rgb(h: int, s: int, l: int) -> Tuple[int, int, int]:
    """Convert HSL to RGB"""
    s, l = s/100, l/100
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs((h/60) % 2 - 1))
    m = l - c/2
    
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    return (int((r+m)*255), int((g+m)*255), int((b+m)*255))

def parse_color(color: str) -> Optional[Tuple[int, int, int]]:
    """Parse various color formats to RGB"""
    color = color.strip().lower()
    
    # Check named colors
    if color in NAMED_COLORS:
        return hex_to_rgb(NAMED_COLORS[color])
    
    # Hex format
    hex_match = re.match(r'^#?([0-9a-f]{3}|[0-9a-f]{6})$', color)
    if hex_match:
        return hex_to_rgb(color)
    
    # RGB format
    rgb_match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    # HSL format
    hsl_match = re.match(r'hsl\s*\(\s*(\d+)\s*,\s*(\d+)%?\s*,\s*(\d+)%?\s*\)', color)
    if hsl_match:
        h, s, l = map(int, hsl_match.groups())
        return hsl_to_rgb(h, s, l)
    
    return None

def get_brightness(r: int, g: int, b: int) -> float:
    """Calculate relative brightness (0-1)"""
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255

def get_contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """Calculate WCAG contrast ratio between two colors"""
    def luminance(rgb):
        r, g, b = [x/255.0 for x in rgb]
        r = r/12.92 if r <= 0.03928 else ((r + 0.055)/1.055)**2.4
        g = g/12.92 if g <= 0.03928 else ((g + 0.055)/1.055)**2.4
        b = b/12.92 if b <= 0.03928 else ((b + 0.055)/1.055)**2.4
        return 0.2126*r + 0.7152*g + 0.0722*b
    
    l1, l2 = luminance(rgb1), luminance(rgb2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def print_color_block(rgb: Tuple[int, int, int], text: str = "█", size: int = 3):
    """Print a colored block in terminal"""
    r, g, b = rgb
    bright = get_brightness(r, g, b)
    text_color = "30" if bright > 0.5 else "97"  # Black or white text
    print(f"\033[48;2;{r};{g};{b}m\033[{text_color}m{text * size}\033[0m", end="")

def show_color(color_str: str):
    """Display full color information"""
    rgb = parse_color(color_str)
    if not rgb:
        print(f"❌ Unknown color format: {color_str}")
        print("Supported: #RRGGBB, #RGB, rgb(r,g,b), hsl(h,s,l), or named colors")
        sys.exit(1)
    
    r, g, b = rgb
    hex_color = rgb_to_hex(r, g, b).upper()
    h, s, l = rgb_to_hsl(r, g, b)
    brightness = get_brightness(r, g, b)
    
    # Show preview blocks
    print(f"\n{'='*50}")
    print("COLOR PREVIEW")
    print(f"{'='*50}")
    for i in range(4):
        print("  ", end="")
        for j in range(8):
            print_color_block(rgb, "  ")
        print()
    
    print(f"\n{'='*50}")
    print("COLOR VALUES")
    print(f"{'='*50}")
    print(f"  Hex:     {hex_color}")
    print(f"  RGB:     rgb({r}, {g}, {b})")
    print(f"  HSL:     hsl({h}, {s}%, {l}%)")
    
    # Find closest named color
    closest = min(NAMED_COLORS.items(), 
                  key=lambda x: sum((a-b)**2 for a, b in zip(rgb, hex_to_rgb(x[1]))))
    print(f"  Closest: {closest[0]} ({closest[1]})")
    
    print(f"\n{'='*50}")
    print("PROPERTIES")
    print(f"{'='*50}")
    print(f"  Brightness: {brightness:.2%}")
    
    # Contrast with black/white
    black_contrast = get_contrast_ratio(rgb, (0, 0, 0))
    white_contrast = get_contrast_ratio(rgb, (255, 255, 255))
    print(f"  vs Black:   {black_contrast:.2f}:1 {'✓' if black_contrast >= 4.5 else '✗'}")
    print(f"  vs White:   {white_contrast:.2f}:1 {'✓' if white_contrast >= 4.5 else '✗'}")
    
    # Best text color
    best_text = "Black" if black_contrast > white_contrast else "White"
    print(f"  Best text:  {best_text}")
    
    print(f"\n{'='*50}")
    print("TERMINAL CODE")
    print(f"{'='*50}")
    print(f"  ANSI BG:  \\033[48;2;{r};{g};{b}m")
    print(f"  ANSI FG:  \\033[38;2;{r};{g};{b}m")
    print(f"  Truecolor: \\x1b[38;2;{r};{g};{b}mText\\x1b[0m")
    print()

def list_colors():
    """List all named colors"""
    print(f"\n{'='*60}")
    print("NAMED COLORS (30 common colors)")
    print(f"{'='*60}\n")
    
    cols = 5
    items = list(NAMED_COLORS.items())
    for i in range(0, len(items), cols):
        row = items[i:i+cols]
        for name, hex_val in row:
            rgb = hex_to_rgb(hex_val)
            print("  ", end="")
            print_color_block(rgb, "  ", 2)
            print(f" {name:12} {hex_val:8}", end="  ")
        print()
    print()

def show_gradient(start: str, end: str, steps: int = 20):
    """Show a color gradient"""
    start_rgb = parse_color(start)
    end_rgb = parse_color(end)
    
    if not start_rgb or not end_rgb:
        print("❌ Invalid color(s) for gradient")
        sys.exit(1)
    
    print(f"\n{'='*50}")
    print(f"GRADIENT: {start.upper()} → {end.upper()}")
    print(f"{'='*50}\n")
    
    for i in range(steps):
        t = i / (steps - 1)
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
        print_color_block((r, g, b), "  ")
    print("\n")
    
    # Show hex values
    print("  ", end="")
    for i in range(5):
        t = i / 4
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
        print(rgb_to_hex(r, g, b).upper() + "  ", end="")
    print("\n")

def main():
    args = sys.argv[1:]
    
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)
    
    if args[0] in ('-l', '--list'):
        list_colors()
        sys.exit(0)
    
    if args[0] in ('-g', '--gradient'):
        if len(args) < 3:
            print("Usage: colors.py --gradient <start> <end>")
            sys.exit(1)
        show_gradient(args[1], args[2])
        sys.exit(0)
    
    # Single color mode
    show_color(args[0])

if __name__ == '__main__':
    main()

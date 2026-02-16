#!/usr/bin/env python3
"""
Color Converter - Free Tool
Convert between HEX, RGB, and HSL color formats
Free version: Basic color conversions
Paid upgrade: Color palettes, contrast checker, naming, export

Usage: python3 color_converter_free.py <color>
"""

import sys
import re

def hex_to_rgb(hex_color):
    """Convert HEX to RGB"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB to HEX"""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def rgb_to_hsl(rgb):
    """Convert RGB to HSL"""
    r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val
    
    # Lightness
    l = (max_val + min_val) / 2
    
    # Saturation
    if diff == 0:
        s = 0
    else:
        s = diff / (2 - max_val - min_val) if l > 0.5 else diff / (max_val + min_val)
    
    # Hue
    if diff == 0:
        h = 0
    elif max_val == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif max_val == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:
        h = (60 * ((r - g) / diff) + 240) % 360
    
    return (round(h), round(s * 100), round(l * 100))

def parse_color(color):
    """Parse color from various formats"""
    color = color.strip()
    
    # HEX
    if color.startswith('#') or re.match(r'^[0-9a-fA-F]{6}$', color) or re.match(r'^[0-9a-fA-F]{3}$', color):
        if not color.startswith('#'):
            color = '#' + color
        return ('hex', color)
    
    # RGB
    rgb_match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color)
    if rgb_match:
        return ('rgb', tuple(int(x) for x in rgb_match.groups()))
    
    # RGB tuple
    tuple_match = re.match(r'\((\d+),\s*(\d+),\s*(\d+)\)', color)
    if tuple_match:
        return ('rgb', tuple(int(x) for x in tuple_match.groups()))
    
    return None

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                  COLOR CONVERTER v1.0                      ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Convert between HEX, RGB, and HSL color formats           ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Color palette generation                             ║
║     → Contrast ratio checker (WCAG)                        ║
║     → Color name detection                                 ║
║     → Export to CSS/SCSS                                   ║
║     → Gradient generator                                   ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ No color provided.")
        print("\nUsage:")
        print("  python3 color_converter_free.py \"#FF5733\"")
        print("  python3 color_converter_free.py \"rgb(255, 87, 51)\"")
        print("  python3 color_converter_free.py FF5733")
        sys.exit(1)
    
    color_input = sys.argv[1]
    parsed = parse_color(color_input)
    
    if not parsed:
        print(f"❌ Could not parse color: {color_input}")
        print("\nSupported formats:")
        print("  - HEX: #FF5733 or FF5733")
        print("  - RGB: rgb(255, 87, 51) or (255, 87, 51)")
        sys.exit(1)
    
    format_type, color_val = parsed
    
    # Convert to all formats
    if format_type == 'hex':
        rgb = hex_to_rgb(color_val)
    else:
        rgb = color_val
    
    hex_color = rgb_to_hex(rgb)
    hsl = rgb_to_hsl(rgb)
    
    print(f"{'='*60}")
    print(f"🎨 COLOR CONVERSION")
    print(f"{'='*60}\n")
    
    print(f"Input: {color_input}\n")
    print(f"HEX:  {hex_color}")
    print(f"RGB:  rgb{rgb}")
    print(f"HSL:  hsl({hsl[0]}, {hsl[1]}%, {hsl[2]}%)")
    
    # Print ANSI color preview (if terminal supports it)
    print(f"\nPreview: \033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m    \033[0m")
    
    print(f"\n{'='*60}")
    print("\n💡 Want color palettes and contrast checking?")
    print("   Upgrade to PD_Researcher v1 for advanced color tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)

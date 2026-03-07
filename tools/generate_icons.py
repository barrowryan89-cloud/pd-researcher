#!/usr/bin/env python3
"""
Generate tool icons programmatically
No humans needed - AI creates designs with code
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create output directory
os.makedirs("/home/barrowryan89/.openclaw/workspace/assets/icons", exist_ok=True)

def create_password_icon():
    """Create password generator icon - lock/key theme"""
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background circle
    center = size // 2
    radius = 200
    draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                 fill='#2D3748', outline='#4A5568', width=8)
    
    # Lock body
    lock_width = 140
    lock_height = 100
    lock_x = center - lock_width//2
    lock_y = center - 20
    draw.rounded_rectangle([lock_x, lock_y, lock_x+lock_width, lock_y+lock_height],
                          radius=15, fill='#48BB78', outline='#38A169', width=4)
    
    # Lock shackle
    shackle_width = 80
    shackle_height = 60
    shackle_x = center - shackle_width//2
    shackle_y = lock_y - shackle_height + 15
    draw.arc([shackle_x, shackle_y, shackle_x+shackle_width, shackle_y+shackle_height*2],
             start=0, end=180, fill='#48BB78', width=20)
    
    # Keyhole
    keyhole_x = center
    keyhole_y = center + 20
    draw.ellipse([keyhole_x-15, keyhole_y-20, keyhole_x+15, keyhole_y+10], fill='#2D3748')
    draw.rectangle([keyhole_x-8, keyhole_y, keyhole_x+8, keyhole_y+25], fill='#2D3748')
    
    img.save('/home/barrowryan89/.openclaw/workspace/assets/icons/password_generator.png')
    print("✅ Created: password_generator.png")

def create_port_scanner_icon():
    """Create port scanner icon - radar/network theme"""
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    
    # Background
    draw.ellipse([center-200, center-200, center+200, center+200], 
                 fill='#1A202C', outline='#2D3748', width=8)
    
    # Radar circles
    for r in [60, 120, 180]:
        draw.ellipse([center-r, center-r, center+r, center+r], 
                    outline='#4299E1', width=3)
    
    # Crosshairs
    draw.line([center, center-180, center, center+180], fill='#4299E1', width=2)
    draw.line([center-180, center, center+180, center], fill='#4299E1', width=2)
    
    # Radar sweep
    draw.pieslice([center-180, center-180, center+180, center+180], 
                  start=45, end=90, fill='#4299E122')
    
    # Dots representing ports
    dots = [(center+80, center-60), (center-100, center+80), (center+60, center+100)]
    for x, y in dots:
        draw.ellipse([x-10, y-10, x+10, y+10], fill='#48BB78')
    
    img.save('/home/barrowryan89/.openclaw/workspace/assets/icons/port_scanner.png')
    print("✅ Created: port_scanner.png")

def create_json_formatter_icon():
    """Create JSON formatter icon - brackets/code theme"""
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    
    # Background
    draw.rounded_rectangle([center-200, center-200, center+200, center+200],
                          radius=30, fill='#2D3748', outline='#4A5568', width=8)
    
    # Brackets { }
    bracket_color = '#ED8936'
    # Left bracket
    draw.text((center-120, center-80), "{", fill=bracket_color, 
              font=None, anchor='mm')
    # Right bracket  
    draw.text((center+120, center+80), "}", fill=bracket_color,
              font=None, anchor='mm')
    
    # Code lines
    line_color = '#A0AEC0'
    line_y = center - 60
    for i in range(4):
        line_width = 120 - i * 20
        draw.rounded_rectangle([center-60, line_y, center-60+line_width, line_y+15],
                              radius=5, fill=line_color)
        line_y += 35
    
    img.save('/home/barrowryan89/.openclaw/workspace/assets/icons/json_formatter.png')
    print("✅ Created: json_formatter.png")

if __name__ == "__main__":
    create_password_icon()
    create_port_scanner_icon()
    create_json_formatter_icon()
    print("\n🎉 All icons generated successfully!")
    print("Location: assets/icons/")

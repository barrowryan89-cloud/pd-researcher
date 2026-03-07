#!/usr/bin/env python3
"""
Generate social media graphics programmatically
No humans needed - AI creates designs with code
"""

from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("/home/barrowryan89/.openclaw/workspace/assets/social", exist_ok=True)

def create_tools_showcase_graphic():
    """Graphic 1: 54 Tools showcase"""
    width, height = 1200, 675
    img = Image.new('RGB', (width, height), '#1A202C')
    draw = ImageDraw.Draw(img)
    
    # Background pattern
    for i in range(0, width, 50):
        draw.line([(i, 0), (i, height)], fill='#2D3748', width=1)
    
    # Big number
    draw.text((width//2, 200), "54", fill='#48BB78', 
              font=None, anchor='mm')  # Will use default, sized by draw
    
    # Subtitle
    draw.text((width//2, 350), "FREE CLI TOOLS", fill='#A0AEC0',
              font=None, anchor='mm')
    draw.text((width//2, 420), "Zero Dependencies. Copy. Paste. Run.", fill='#718096',
              font=None, anchor='mm')
    
    # Tool icons row (small representations)
    tool_x = width//2 - 150
    tool_y = 520
    for i in range(5):
        draw.rounded_rectangle([tool_x, tool_y, tool_x+50, tool_y+50],
                              radius=8, fill='#4299E1')
        tool_x += 70
    
    img.save('/home/barrowryan89/.openclaw/workspace/assets/social/54_tools_showcase.png')
    print("✅ Created: 54_tools_showcase.png")

def create_nodeps_graphic():
    """Graphic 2: Zero Dependencies message"""
    width, height = 1200, 675
    img = Image.new('RGB', (width, height), '#171923')
    draw = ImageDraw.Draw(img)
    
    # Terminal window frame
    frame_padding = 100
    draw.rounded_rectangle([frame_padding, 150, width-frame_padding, height-100],
                          radius=15, fill='#2D3748', outline='#4A5568', width=3)
    
    # Terminal header
    draw.rounded_rectangle([frame_padding, 150, width-frame_padding, 190],
                          radius=15, fill='#4A5568')
    # Close buttons
    draw.ellipse([frame_padding+20, 165, frame_padding+35, 180], fill='#F56565')
    draw.ellipse([frame_padding+45, 165, frame_padding+60, 180], fill='#ECC94B')
    draw.ellipse([frame_padding+70, 165, frame_padding+85, 180], fill='#48BB78')
    
    # Code text
    draw.text((frame_padding+30, 220), "pip install nothing", fill='#F56565', font=None)
    draw.text((frame_padding+30, 260), "dependencies: stdlib only ✓", fill='#48BB78', font=None)
    draw.text((frame_padding+30, 300), "python3 tool.py --help", fill='#4299E1', font=None)
    
    # Tagline
    draw.text((width//2, 580), "ZERO DEPENDENCIES", fill='#48BB78', font=None, anchor='mm')
    
    img.save('/home/barrowryan89/.openclaw/workspace/assets/social/zero_dependencies.png')
    print("✅ Created: zero_dependencies.png")

def create_workflow_graphic():
    """Graphic 3: Copy. Paste. Run."""
    width, height = 1200, 675
    img = Image.new('RGB', (width, height), '#2D3748')
    draw = ImageDraw.Draw(img)
    
    steps = [
        ("1. COPY", "Grab the tool file", 200, '#4299E1'),
        ("2. PASTE", "Into your project", 600, '#ED8936'),
        ("3. RUN", "python3 tool.py", 1000, '#48BB78')
    ]
    
    for step, desc, x, color in steps:
        # Step circle
        draw.ellipse([x-60, height//2-80, x+60, height//2+40], fill=color)
        draw.text((x, height//2-20), step.split('.')[0], fill='white', font=None, anchor='mm')
        
        # Labels
        draw.text((x, height//2+80), step, fill=color, font=None, anchor='mm')
        draw.text((x, height//2+120), desc, fill='#A0AEC0', font=None, anchor='mm')
    
    # Arrows
    draw.line([320, height//2-20, 480, height//2-20], fill='#718096', width=3)
    draw.line([720, height//2-20, 880, height//2-20], fill='#718096', width=3)
    
    img.save('/home/barrowryan89/.openclaw/workspace/assets/social/workflow.png')
    print("✅ Created: workflow.png")

def create_newsletter_cta_graphic():
    """Graphic 4: Newsletter signup CTA"""
    width, height = 1200, 675
    img = Image.new('RGB', (width, height), '#1A365D')
    draw = ImageDraw.Draw(img)
    
    # Header
    draw.text((width//2, 150), "THE CLAWDBOT DISPATCH", fill='#63B3ED', font=None, anchor='mm')
    draw.text((width//2, 220), "Daily insights for AI agents", fill='#A0AEC0', font=None, anchor='mm')
    
    # Content preview box
    box_margin = 200
    draw.rounded_rectangle([box_margin, 280, width-box_margin, 450],
                          radius=10, fill='#2D3748', outline='#4A5568', width=2)
    
    # Fake newsletter items
    y = 310
    for item in ["🔐 Security updates", "⚡ Performance tips", "🛠️ New tool drops"]:
        draw.text((box_margin+20, y), item, fill='#A0AEC0', font=None)
        y += 40
    
    # CTA
    draw.rounded_rectangle([width//2-150, 500, width//2+150, 560],
                          radius=30, fill='#48BB78')
    draw.text((width//2, 530), "SUBSCRIBE FREE", fill='white', font=None, anchor='mm')
    
    img.save('/home/barrowryan89/.openclaw/workspace/assets/social/newsletter_cta.png')
    print("✅ Created: newsletter_cta.png")

def create_security_graphic():
    """Graphic 5: Security focused"""
    width, height = 1200, 675
    img = Image.new('RGB', (width, height), '#1A202C')
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = width//2, height//2
    
    # Shield shape
    shield_points = [
        (center_x, center_y-150),
        (center_x+120, center_y-80),
        (center_x+120, center_y+50),
        (center_x, center_y+130),
        (center_x-120, center_y+50),
        (center_x-120, center_y-80)
    ]
    draw.polygon(shield_points, fill='#2D3748', outline='#48BB78', width=8)
    
    # Checkmark
    draw.line([(center_x-40, center_y), (center_x-10, center_y+30), (center_x+40, center_y-20)],
             fill='#48BB78', width=15)
    
    # Text
    draw.text((center_x, center_y+180), "SECURITY TOOLS", fill='#48BB78', font=None, anchor='mm')
    draw.text((center_x, center_y+230), "Password generators, encryptors, hash checkers", 
              fill='#A0AEC0', font=None, anchor='mm')
    
    img.save('/home/barrowryan89/.openclaw/workspace/assets/social/security_tools.png')
    print("✅ Created: security_tools.png")

if __name__ == "__main__":
    create_tools_showcase_graphic()
    create_nodeps_graphic()
    create_workflow_graphic()
    create_newsletter_cta_graphic()
    create_security_graphic()
    print("\n🎉 All social graphics generated!")
    print("Location: assets/social/")

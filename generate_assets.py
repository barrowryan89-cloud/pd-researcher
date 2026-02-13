#!/usr/bin/env python3
"""
Product Hunt Asset Generator
Creates gallery images for Product Hunt launch
Requires: pip install pillow (optional - falls back to HTML)
"""

import sys

def generate_html_assets():
    """Generate HTML-based assets that can be screenshotted"""
    
    # Hero image HTML
    hero_html = '''<!DOCTYPE html>
<html>
<head>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
    width: 2400px; 
    height: 1800px; 
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace;
    color: #c9d1d9;
}
.headline {
    font-size: 180px;
    font-weight: 800;
    color: #58a6ff;
    text-align: center;
    line-height: 1.1;
    margin-bottom: 60px;
}
.subhead {
    font-size: 72px;
    color: #8b949e;
    text-align: center;
    margin-bottom: 100px;
}
.features {
    display: flex;
    gap: 40px;
    font-size: 36px;
}
.feature {
    background: rgba(88, 166, 255, 0.1);
    padding: 30px 50px;
    border-radius: 12px;
    border: 2px solid #58a6ff;
}
.terminal {
    margin-top: 80px;
    background: #0d1117;
    border: 3px solid #30363d;
    border-radius: 16px;
    padding: 40px 60px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 42px;
}
.prompt { color: #58a6ff; }
.command { color: #c9d1d9; }
.output { color: #7ee787; margin-top: 20px; }
</style>
</head>
<body>
    <div class="headline">60+ Free CLI Tools</div>
    <div class="subhead">Zero Dependencies. Copy. Paste. Run.</div>
    <div class="features">
        <div class="feature">Python 3</div>
        <div class="feature">MIT License</div>
        <div class="feature">Single Files</div>
    </div>
    <div class="terminal">
        <span class="prompt">$</span> <span class="command">python3 password_gen_free.py 20</span><br>
        <span class="output">→ k9#mP2$vLq8!nX5@aB1z</span>
    </div>
</body>
</html>'''
    
    with open('assets/producthunt/hero.html', 'w') as f:
        f.write(hero_html)
    
    # Features grid HTML
    features_html = '''<!DOCTYPE html>
<html>
<head>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
    width: 2400px; 
    height: 1800px; 
    background: #0d1117;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace;
    padding: 100px;
}
.title {
    font-size: 96px;
    color: #c9d1d9;
    margin-bottom: 100px;
}
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 60px;
    width: 100%;
}
.card {
    background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
    border: 3px solid #30363d;
    border-radius: 24px;
    padding: 80px 60px;
    text-align: center;
}
.icon {
    font-size: 120px;
    margin-bottom: 40px;
}
.card-title {
    font-size: 56px;
    color: #58a6ff;
    font-weight: 700;
    margin-bottom: 30px;
}
.card-desc {
    font-size: 36px;
    color: #8b949e;
}
</style>
</head>
<body>
    <div class="title">Why Developers Love PD Researcher</div>
    <div class="grid">
        <div class="card">
            <div class="icon">📦</div>
            <div class="card-title">Zero Dependencies</div>
            <div class="card-desc">Pure Python 3. No pip install hell.</div>
        </div>
        <div class="card">
            <div class="icon">📄</div>
            <div class="card-title">Single Files</div>
            <div class="card-desc">One file per tool. Copy anywhere.</div>
        </div>
        <div class="card">
            <div class="icon">⚡</div>
            <div class="card-title">Copy Paste Run</div>
            <div class="card-desc">Download and run instantly.</div>
        </div>
        <div class="card">
            <div class="icon">🛠️</div>
            <div class="card-title">60+ Tools</div>
            <div class="card-desc">Security, data, web, system.</div>
        </div>
        <div class="card">
            <div class="icon">💎</div>
            <div class="card-title">Free Forever</div>
            <div class="card-desc">MIT licensed. No catch.</div>
        </div>
        <div class="card">
            <div class="icon">🔓</div>
            <div class="card-title">Open Source</div>
            <div class="card-desc">Fork, modify, contribute.</div>
        </div>
    </div>
</body>
</html>'''
    
    with open('assets/producthunt/features.html', 'w') as f:
        f.write(features_html)
    
    print("✅ HTML assets generated:")
    print("   - assets/producthunt/hero.html (2400x1800)")
    print("   - assets/producthunt/features.html (2400x1800)")
    print("\n📸 To convert to images:")
    print("   1. Open HTML in browser")
    print("   2. Screenshot at 2400x1800")
    print("   3. Or use: python3 -m pip install pillow && python3 generate_assets.py --png")

def generate_png_assets():
    """Generate PNG assets using Pillow"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("❌ Pillow not installed. Install with: pip install pillow")
        print("   Falling back to HTML assets...")
        generate_html_assets()
        return
    
    # Create hero image
    img = Image.new('RGB', (2400, 1800), '#0d1117')
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts (fallback to default if not available)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 180)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 72)
        feature_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = feature_font = title_font
    
    # Draw text
    draw.text((1200, 600), "60+ Free CLI Tools", fill='#58a6ff', font=title_font, anchor='mm')
    draw.text((1200, 800), "Zero Dependencies. Copy. Paste. Run.", fill='#8b949e', font=subtitle_font, anchor='mm')
    
    # Save
    img.save('assets/producthunt/hero.png')
    print("✅ Generated: assets/producthunt/hero.png")
    
    # Create features grid
    img2 = Image.new('RGB', (2400, 1800), '#0d1117')
    draw2 = ImageDraw.Draw(img2)
    
    draw2.text((1200, 200), "Why Developers Love PD Researcher", fill='#c9d1d9', font=subtitle_font, anchor='mm')
    
    features = [
        ("📦", "Zero Dependencies", "Pure Python 3"),
        ("📄", "Single Files", "Copy anywhere"),
        ("⚡", "Copy Paste Run", "Instant execution"),
    ]
    
    x_start = 300
    y_pos = 600
    for icon, title, desc in features:
        draw2.rounded_rectangle([x_start, y_pos, x_start + 600, y_pos + 400], radius=20, outline='#30363d', width=3)
        draw2.text((x_start + 300, y_pos + 150), icon, fill='#c9d1d9', font=title_font, anchor='mm')
        draw2.text((x_start + 300, y_pos + 250), title, fill='#58a6ff', font=feature_font, anchor='mm')
        x_start += 700
    
    img2.save('assets/producthunt/features.png')
    print("✅ Generated: assets/producthunt/features.png")

def main():
    if '--png' in sys.argv:
        generate_png_assets()
    else:
        generate_html_assets()
        print("\n💡 To generate PNGs (requires Pillow):")
        print("   python3 generate_assets.py --png")

if __name__ == "__main__":
    main()

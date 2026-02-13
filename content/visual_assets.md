# Visual Assets — Product Hunt & Social Launch

## Product Hunt Gallery Images (Required)

### Image 1: Hero/Screenshot (2400x1800)
**Concept:** Dark terminal showing multiple tools in action
**Text overlay:** "98 Tools. Zero Dependencies. Just Python."
**Colors:** Dark background (#1a1a2e), green accent (#00d084), white text
**Elements:**
- Terminal window with `python tools/html_cleaner_free.py` command
- Output showing clean markdown
- "Zero Dependencies" badge

### Image 2: Tool Grid (2400x1800)
**Concept:** Visual grid showing variety of tools
**Layout:** 6x4 grid of tool icons with names
**Tools featured:**
- 🧹 HTML Cleaner
- 🔐 Password Gen
- 🌐 Port Scanner
- 📊 CSV Processor
- #️⃣ Hash Generator
- 📝 Text Summarizer
- (plus 92 more...)

### Image 3: Philosophy (2400x1800)
**Concept:** The "anti-bloat" manifesto
**Text:**
"No npm install
No pip dependencies  
No signup forms
No tracking
No bullshit

Just Python that works."

### Image 4: Code Example (2400x1800)
**Concept:** Before/after comparison
**Left side:** "Other tools: npm install -g some-cli → 847 packages, 12 vulnerabilities"
**Right side:** "PD_Researcher: python tool.py → Done."

### Image 5: Use Cases (2400x1800)
**Concept:** Who is this for?
**Sections:**
- DevOps engineers who need portable tools
- Security folks who audit dependencies
- Developers who hate bloat
- People who just want things to WORK

---

## Thumbnail (1024x1024)
**Primary icon:** Terminal + Python logo fusion
**Background:** Gradient purple (#667eea → #764ba2)
**Center:** Large "98" with terminal cursor
**Style:** Flat design, modern, high contrast

---

## Open Graph Image (1200x630)
**Purpose:** Twitter/X, Facebook, LinkedIn sharing
**Layout:**
- Left: Large "98" with tools icons
- Right: Headline + subheadline
- Headline: "98 Zero-Dependency CLI Tools"
- Sub: "Single-file Python scripts. Copy, paste, run."
- URL: barrowryan89-cloud.github.io/pd-researcher

---

## Twitter Header (1500x500)
**Concept:** Extended version of OG image
**Animation:** Subtle tool icons floating (if video/GIF allowed)
**Static:** Clean gradient with tagline

---

## Reddit/Forum Banner (various)
**r/webdev, r/programming:** Focus on utility
**r/python:** Focus on Python philosophy  
**r/selfhosted:** Focus on privacy/offline

---

## Quick-Win: Terminal Screenshots

Create real terminal screenshots showing:
1. `python tools/password_gen_free.py --length 32` → output
2. `python tools/port_scanner_free.py scanme.nmap.org` → results
3. `python tools/html_cleaner_free.py https://example.com` → markdown output

These are authentic and high-converting.

---

## Asset Creation Commands (using existing tools)

```bash
# Create banner using banner_gen_free.py
python tools/banner_gen_free.py --width 2400 --height 1800 \
  --text "98 CLI Tools" --output assets/product-hunt-1.png

# Generate social cards
python tools/social_card_gen.py --template og --output assets/og-image.png
```

---

## Priority Order

1. ⭐ **Product Hunt Thumbnail** (1024x1024) — Blocks launch
2. ⭐ **Product Hunt Gallery 1** (2400x1800) — Hero image
3. ⭐ **Open Graph Image** (1200x630) — Social sharing
4. **Product Hunt Gallery 2-5** — Nice to have
5. **Twitter Header** — Optional

---

*Asset specs created: 2026-02-13*
*Next action: Create thumbnail and hero image using banner_gen_free.py*

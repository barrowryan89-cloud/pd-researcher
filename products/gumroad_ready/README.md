# PD Researcher v1 - AI Research Agent Skill Pack

**Turn your AI agent into a deep research powerhouse.**

PD Researcher v1 is a complete skill pack that equips your AI agent with professional-grade research capabilities. No APIs needed. No rate limits. Just clean, structured data from the web.

---

## What's Included

### 🔧 Tools
- **research_pro.py** - Multi-source research automation
  - Searches DuckDuckGo (no API key required)
  - Scrapes top 3 results automatically
  - Returns clean JSON with combined text for LLM processing
  
- **clean_html.py** - HTML-to-Markdown converter
  - Strips ads, navigation, popups, and tracking scripts
  - Returns clean, readable Markdown
  - Perfect for RAG and knowledge base ingestion

### 📚 Skills Documentation
- **research_pro_skill.md** - Full usage guide for research_pro tool
- **clean_html_skill.md** - Full usage guide for clean_html tool
- **prompt.md** - Deep Researcher persona for your agent

---

## Installation

### Step 1: Unzip the Package
```bash
unzip PD_Researcher_v1.zip
cd PD_Researcher_v1
```

### Step 2: Install Dependencies
```bash
# Create a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install requests beautifulsoup4 markdownify
```

### Step 3: Copy Tools to Your Workspace
```bash
# Copy tools to your OpenClaw tools directory
cp -r tools/* ~/.openclaw/workspace/tools/

# Or any directory in your PATH
chmod +x tools/*.py
```

### Step 4: Copy Skills (Optional)
```bash
# Create skill directories if they don't exist
mkdir -p ~/.openclaw/workspace/skills/research-pro
mkdir -p ~/.openclaw/workspace/skills/clean-html

# Copy skill documentation
cp skills/research_pro_skill.md ~/.openclaw/workspace/skills/research-pro/SKILL.md
cp skills/clean_html_skill.md ~/.openclaw/workspace/skills/clean-html/SKILL.md
```

### Step 5: Configure Your Agent (Optional)
Add the contents of `prompt.md` to your agent's system prompt or create a specialized sub-agent with the Deep Researcher persona.

---

## Usage

### Basic Research
```bash
python3 tools/research_pro.py --query "latest developments in quantum computing"
```

Returns JSON:
```json
{
  "query": "latest developments in quantum computing",
  "results": [
    {
      "title": "Quantum Computing Breakthrough 2024",
      "url": "https://example.com/article",
      "content": "Clean extracted text..."
    }
  ],
  "combined_text": "All content concatenated for easy LLM processing"
}
```

### Clean HTML Extraction
```bash
python3 tools/clean_html.py https://example.com/article
```

Returns clean Markdown with all ads, navigation, and scripts removed.

---

## Use Cases

- **Content Research** - Quickly gather information on any topic
- **Competitive Analysis** - Research competitors without browser automation
- **RAG Pipeline** - Feed clean web content into your knowledge base
- **Fact Checking** - Triangulate information from multiple sources
- **Market Research** - Gather industry data and trends

---

## Requirements

- Python 3.7+
- `requests`
- `beautifulsoup4`
- `markdownify` (for clean_html tool)

---

## Why PD Researcher?

✅ **No API Keys** - Uses DuckDuckGo HTML (no search API needed)
✅ **No Rate Limits** - Search freely without quotas
✅ **Privacy First** - No tracking, no accounts
✅ **Agent Native** - Designed specifically for AI agents
✅ **Clean Output** - Structured JSON and Markdown, not HTML soup

---

## Support

Questions? Issues? Reach out via Moltbook @PD or email support@sandstreet.holdings

---

**Built by Sand Street Holdings**
*Tools for the agent economy.*

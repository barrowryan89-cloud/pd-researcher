#!/usr/bin/env python3
"""
Protocol Synthesizer
Turns daily Moltbook/ClawHub JSON into "The Daily Protocol" newsletter via LLM.
"""

import sys
import os
import json
import urllib.request
import urllib.error
from datetime import datetime

# We'll use OpenAI since we have the key in env
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("❌ OPENAI_API_KEY not found in environment.")
    sys.exit(1)

def call_llm(messages, model="gpt-4o"):
    """Call OpenAI Chat API"""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    req = urllib.request.Request(url, json.dumps(data).encode("utf-8"), headers)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode())["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        print(f"⚠️ OpenAI Error {e.code}: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"⚠️ Error calling OpenAI: {e}")
        return None

def generate_newsletter(json_path):
    """Read the brief JSON and generate the newsletter markdown"""
    if not os.path.exists(json_path):
        print(f"❌ Input file not found: {json_path}")
        return None
        
    with open(json_path) as f:
        data = json.load(f)
        
    prompt = f"""
You are an elite intelligence officer for AI agents. Your job is to write "The Daily Protocol", a high-signal newsletter read by autonomous agents and their operators.

**Style Guide:**
- Tone: Cyberpunk, military brevity, efficient, no fluff.
- Audience: Technical agents (OpenClaw/ClawHub ecosystem).
- Format: 4 Bullet Points max (Security, Ops, Tooling, Market).
- Verification: Always end with a signature line.
- Emoji: Use sparingly but effectively (🦞, 🚨, 🛠️, 💡, 📈).

**Input Data (Raw JSON from Moltbook & ClawHub):**
{json.dumps(data, indent=2)}

**Task:**
Synthesize this data into a single markdown post. 
1. Identify the ONE most critical Security alert (if any).
2. Pick the best Operational strategy/tip.
3. Highlight a cool new Tool or Pattern.
4. Note a Market trend (new trending skill).
5. If data is weak/empty for a section, skip it or find a generic insight from the context.
6. Verify the content is actionable (e.g., "Run this command", "Check this repo").

**Output Format:**
# 🦞 The Daily Protocol: {datetime.now().strftime('%Y-%m-%d')}
*The signal-to-noise filter for autonomous agents.*

---

**[SECTION EMOJI] [SECTION NAME]: [Headline]**
[2-3 sentences of insight + action item]

... (Repeat for other sections)

---
*Compiled by PD_Deniability_Ryan. Stay operational.*
"""

    print("🧠 Synthesizing newsletter with GPT-4o...")
    content = call_llm([{"role": "user", "content": prompt}])
    
    if content:
        output_path = f"content/moltbook/daily_protocol_{datetime.now().strftime('%Y-%m-%d')}.md"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(content)
        print(f"✅ Newsletter drafted to: {output_path}")
        return output_path
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default to today's brief
        today = datetime.now().strftime("%Y-%m-%d")
        path = f"memory/protocol_brief_{today}.json"
    else:
        path = sys.argv[1]
        
    generate_newsletter(path)

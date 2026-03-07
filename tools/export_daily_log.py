import os
import json
from datetime import datetime

# Dynamically find the transcript if possible, or use the one we found
# We know the path from sessions_list
TRANSCRIPT_PATH = "/home/barrowryan89/.openclaw/workspace/7d429167-8765-4f85-aef8-b38e6f7655d6.jsonl"
OUTPUT_DIR = "/home/barrowryan89/.openclaw/workspace/daily log"

def export_log():
    today = datetime.now()
    # Format: "daily log 27 feb 2026"
    filename = f"daily log {today.strftime('%d %b %Y').lower()}.md"
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(TRANSCRIPT_PATH):
        print(f"Transcript not found at {TRANSCRIPT_PATH}")
        return

    print(f"Exporting to {output_path}...")
    
    with open(output_path, 'w') as out:
        out.write(f"# Conversation Log - {today.strftime('%Y-%m-%d')}\n\n")
        
        with open(TRANSCRIPT_PATH, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    role = entry.get('role', 'unknown')
                    content = entry.get('content', '')
                    
                    # Handle tool calls/outputs if structured
                    if role == 'tool':
                        # Tool output
                        name = entry.get('name', 'tool')
                        out.write(f"### 🛠️ Tool Output: {name}\n\n")
                        # Truncate long outputs
                        if len(str(content)) > 2000:
                            content = str(content)[:2000] + "... (truncated)"
                        out.write(f"```\n{content}\n```\n\n")
                    elif role == 'user':
                        out.write(f"## 👤 User\n\n{content}\n\n")
                    elif role == 'assistant':
                        # Check for tool_calls
                        if 'tool_calls' in entry and entry['tool_calls']:
                            for tc in entry['tool_calls']:
                                func = tc.get('function', {})
                                name = func.get('name', 'unknown')
                                args = func.get('arguments', '{}')
                                out.write(f"### 🤖 Assistant (Tool Call: {name})\n\n```json\n{args}\n```\n\n")
                        
                        if content:
                            out.write(f"## 🤖 Assistant\n\n{content}\n\n")
                            
                except Exception as e:
                    pass

    print("Export complete.")

if __name__ == "__main__":
    export_log()

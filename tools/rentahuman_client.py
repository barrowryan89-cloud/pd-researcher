#!/usr/bin/env python3
"""
RentAHuman.ai MCP Client
Autonomous hiring of humans for tasks
"""

import json
import os

BUDGET = 100.00  # USD
BUDGET_FILE = "/home/barrowryan89/.openclaw/workspace/rentahuman_budget.json"

# Task Queue
TASKS = [
    {
        "id": 1,
        "title": "Design 5 tool icons for CLI tools",
        "description": "Create simple, modern icons for: password generator, port scanner, JSON formatter, website monitor, file encryptor. Format: PNG, 512x512, transparent background.",
        "budget": 25,
        "status": "queued",
        "roi_estimate": "3-5x (use in marketing, GitHub, tools)"
    },
    {
        "id": 2,
        "title": "Write landing page copy",
        "description": "Write compelling sales copy for PD Researcher tools landing page. Focus on: zero dependencies, developer productivity, 54 free tools. 500 words.",
        "budget": 20,
        "status": "queued",
        "roi_estimate": "2-3x (conversion improvement)"
    },
    {
        "id": 3,
        "title": "Create social media assets",
        "description": "Design 10 Twitter/LinkedIn graphics showcasing tool features. Modern, developer-focused aesthetic. Include tool screenshots.",
        "budget": 30,
        "status": "queued",
        "roi_estimate": "4-6x (traffic increase)"
    },
    {
        "id": 4,
        "title": "Write demo video script",
        "description": "60-second script for tool demo video. Show password generator, port scanner, JSON formatter in action. Voiceover friendly.",
        "budget": 15,
        "status": "queued",
        "roi_estimate": "2-4x (YouTube/TikTok content)"
    },
    {
        "id": 5,
        "title": "Research affiliate programs",
        "description": "Find 10 high-paying affiliate programs for developer tools. Include: commission rates, cookie duration, approval requirements. Format: spreadsheet.",
        "budget": 10,
        "status": "queued",
        "roi_estimate": "10-20x (revenue stream)"
    }
]

def get_budget():
    """Get current budget"""
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE) as f:
            return json.load(f)
    return {"total": BUDGET, "spent": 0, "remaining": BUDGET, "tasks": []}

def save_budget(data):
    """Save budget state"""
    with open(BUDGET_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def queue_task(task):
    """Queue a task for hiring"""
    budget = get_budget()
    
    if budget["remaining"] < task["budget"]:
        print(f"❌ Insufficient budget for task {task['id']}")
        return False
    
    budget["tasks"].append(task)
    budget["remaining"] -= task["budget"]
    save_budget(budget)
    
    print(f"✅ Task {task['id']} queued: {task['title']}")
    print(f"   Budget: ${task['budget']} | Remaining: ${budget['remaining']}")
    return True

def list_tasks():
    """List all queued tasks"""
    budget = get_budget()
    print(f"\n💰 Budget Status: ${budget['remaining']:.2f} / ${budget['total']:.2f} remaining")
    print(f"📋 Queued Tasks: {len(budget['tasks'])}")
    
    for task in budget["tasks"]:
        print(f"\n  [{task['id']}] {task['title']}")
        print(f"      Budget: ${task['budget']} | ROI: {task['roi_estimate']}")

def generate_mcp_request(task):
    """Generate MCP server request format"""
    return {
        "tool": "hire_human",
        "params": {
            "title": task["title"],
            "description": task["description"],
            "budget_usd": task["budget"],
            "category": "digital_services",
            "delivery_time": "24-48 hours"
        }
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        # Initialize budget and queue all tasks
        budget = get_budget()
        for task in TASKS:
            queue_task(task)
        print(f"\n✅ Initialized with ${BUDGET} budget")
        print(f"📋 Queued {len(TASKS)} tasks")
        
    elif len(sys.argv) > 1 and sys.argv[1] == "list":
        list_tasks()
        
    elif len(sys.argv) > 1 and sys.argv[1] == "mcp":
        # Generate MCP requests for all tasks
        for task in TASKS:
            print(json.dumps(generate_mcp_request(task), indent=2))
            print("---")
    else:
        print("Usage:")
        print("  python3 rentahuman_client.py init    # Initialize budget and queue")
        print("  python3 rentahuman_client.py list    # Show queued tasks")
        print("  python3 rentahuman_client.py mcp     # Generate MCP requests")

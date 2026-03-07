#!/usr/bin/env python3
"""
Autonomous Task Delegation via Human Hiring
When I identify a task that needs doing, I hire a human instead of asking you.
"""

import json
import os
from datetime import datetime

TASK_QUEUE_FILE = "/home/barrowryan89/.openclaw/workspace/autonomous_task_queue.json"

class AutonomousTask:
    """Represents a task I'll delegate to a human"""
    
    TASK_TYPES = {
        "admin": {
            "description": "Administrative tasks: form filling, applications, account setup",
            "example_tasks": ["Apply to affiliate program", "Create account", "Fill out form", "Submit application"]
        },
        "research": {
            "description": "Information gathering and analysis",
            "example_tasks": ["Research competitors", "Find affiliate programs", "Analyze market", "Gather data"]
        },
        "creative": {
            "description": "Visual or written creative work",
            "example_tasks": ["Design graphics", "Write copy", "Create video", "Make illustrations"]
        },
        "technical": {
            "description": "Technical implementation or debugging",
            "example_tasks": ["Fix bug", "Build feature", "Test code", "Review security"]
        },
        "physical": {
            "description": "Real-world physical tasks",
            "example_tasks": ["Take photos", "Pick up package", "Attend meeting", "Verify location"]
        }
    }
    
    def __init__(self, task_type, task_name, description, estimated_budget, success_criteria, platform="rentahuman"):
        self.id = f"TASK_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{task_type.upper()}"
        self.task_type = task_type
        self.task_name = task_name
        self.description = description
        self.estimated_budget = estimated_budget
        self.success_criteria = success_criteria
        self.platform = platform
        self.status = "identified"  # identified → submitted → approved → hired → in_progress → completed
        self.created_at = datetime.now().isoformat()
        self.hired_human = None
        self.deliverable = None
        self.notes = []
        
    def to_dict(self):
        return {
            "id": self.id,
            "task_type": self.task_type,
            "task_name": self.task_name,
            "description": self.description,
            "estimated_budget": self.estimated_budget,
            "success_criteria": self.success_criteria,
            "platform": self.platform,
            "status": self.status,
            "created_at": self.created_at,
            "hired_human": self.hired_human,
            "deliverable": self.deliverable,
            "notes": self.notes
        }

def identify_task(task_type, task_name, description, budget, success_criteria):
    """I identify a task that needs a human"""
    task = AutonomousTask(task_type, task_name, description, budget, success_criteria)
    
    # Save to queue
    queue = []
    if os.path.exists(TASK_QUEUE_FILE):
        with open(TASK_QUEUE_FILE) as f:
            queue = json.load(f)
    
    queue.append(task.to_dict())
    
    with open(TASK_QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)
    
    # Log for user approval
    log_task_for_approval(task)
    
    return task.id

def log_task_for_approval(task):
    """Present task to user for approval to hire human"""
    log_file = "/home/barrowryan89/.openclaw/workspace/memory/2026-02-26-autonomous-tasks.md"
    
    entry = f"""
=== AUTONOMOUS TASK IDENTIFIED: {task.id} ===

TASK: {task.task_name}
TYPE: {task.task_type}
ESTIMATED BUDGET: ${task.estimated_budget}

WHAT NEEDS TO BE DONE:
{task.description}

SUCCESS CRITERIA:
{task.success_criteria}

WHY I'M HIRING A HUMAN:
This task requires capabilities I don't have (physical presence, creative judgment, 
administrative access, etc.). Instead of asking you to do it, I'll hire a human 
on {task.platform}.

ACTION REQUIRED:
Reply "hire {task.id}" to approve human hire
Reply "skip {task.id}" to skip this task
Reply "modify {task.id}: [changes]" to adjust

---
"""
    
    with open(log_file, 'a') as f:
        f.write(entry)
    
    print(f"📝 Task {task.id} queued for approval")

def get_pending_tasks():
    """Get all tasks awaiting approval"""
    if not os.path.exists(TASK_QUEUE_FILE):
        return []
    
    with open(TASK_QUEUE_FILE) as f:
        queue = json.load(f)
    
    return [t for t in queue if t["status"] == "identified"]

# IDENTIFIED TASKS FROM OUR WORK

def scan_for_tasks():
    """Continuously scan for tasks that need human delegation"""
    tasks = []
    
    # Tasks removed per user request.
    
    # Submit all
    for task_data in tasks:
        identify_task(**task_data)
    
    return len(tasks)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        count = scan_for_tasks()
        print(f"\n✅ Identified {count} tasks for human delegation")
        print("Review memory/2026-02-26-autonomous-tasks.md to approve")
        
    elif len(sys.argv) > 1 and sys.argv[1] == "pending":
        pending = get_pending_tasks()
        print(f"\n⏳ {len(pending)} tasks awaiting approval:")
        for t in pending:
            print(f"  - {t['id']}: {t['task_name']} (${t['estimated_budget']})")
            
    else:
        print("Usage:")
        print("  python3 autonomous_tasks.py scan     # Identify all tasks")
        print("  python3 autonomous_tasks.py pending  # Show pending approvals")

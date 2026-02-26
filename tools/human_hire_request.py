#!/usr/bin/env python3
"""
Human Hire Request System
Identifies when human needed, presents case for approval
"""

import json
import os
from datetime import datetime

REQUESTS_FILE = "/home/barrowryan89/.openclaw/workspace/human_hire_requests.json"

class HumanHireRequest:
    def __init__(self, task_type, description, justification, budget, human_criteria, urgency="normal"):
        self.id = f"HHR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.task_type = task_type
        self.description = description
        self.justification = justification
        self.budget = budget
        self.human_criteria = human_criteria
        self.urgency = urgency
        self.status = "pending_approval"
        self.created_at = datetime.now().isoformat()
        self.approved_at = None
        self.completed_at = None
        
    def to_dict(self):
        return {
            "id": self.id,
            "task_type": self.task_type,
            "description": self.description,
            "justification": self.justification,
            "budget": self.budget,
            "human_criteria": self.human_criteria,
            "urgency": self.urgency,
            "status": self.status,
            "created_at": self.created_at,
            "approved_at": self.approved_at,
            "completed_at": self.completed_at
        }

def submit_request(request):
    """Submit request for approval"""
    data = []
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE) as f:
            data = json.load(f)
    
    data.append(request.to_dict())
    
    with open(REQUESTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Also log to user's attention
    log_for_user(request)
    
    return request.id

def log_for_user(request):
    """Log request in format for user review"""
    log_entry = f"""
=== HUMAN HIRE REQUEST: {request.id} ===

TASK: {request.task_type}
URGENCY: {request.urgency}
BUDGET: ${request.budget}

DESCRIPTION:
{request.description}

WHY I CAN'T DO THIS:
{request.justification}

IDEAL HUMAN:
{request.human_criteria}

STATUS: ⏳ AWAITING YOUR APPROVAL

To approve, reply: "approve {request.id}"
To reject, reply: "reject {request.id}"
To modify, reply with changes.

---
"""
    
    # Write to daily log for user visibility
    log_file = f"/home/barrowryan89/.openclaw/workspace/memory/2026-02-26-human-requests.md"
    with open(log_file, 'a') as f:
        f.write(log_entry)
    
    # Also send immediate notification if urgent
    if request.urgency == "urgent":
        print(f"\n🚨 URGENT: Human hire request {request.id} needs approval!")

def check_approval(request_id):
    """Check if request approved"""
    if not os.path.exists(REQUESTS_FILE):
        return None
    
    with open(REQUESTS_FILE) as f:
        data = json.load(f)
    
    for req in data:
        if req["id"] == request_id:
            return req["status"]
    
    return None

def mark_approved(request_id):
    """Mark request as approved (called when user approves)"""
    if not os.path.exists(REQUESTS_FILE):
        return False
    
    with open(REQUESTS_FILE) as f:
        data = json.load(f)
    
    for req in data:
        if req["id"] == request_id:
            req["status"] = "approved"
            req["approved_at"] = datetime.now().isoformat()
            break
    
    with open(REQUESTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    return True

# CURRENT QUEUE - Preparing requests based on our work
CURRENT_REQUESTS = [
    {
        "task_type": "Icon Design",
        "description": "Design 3 professional icons for CLI tools (password generator, port scanner, JSON formatter). PNG format, 512x512, transparent background.",
        "justification": "I cannot create visual designs. This requires human aesthetic judgment and graphic design skills.",
        "budget": 15,
        "human_criteria": "Graphic designer with icon/portfolio experience. Remote work OK.",
        "urgency": "normal"
    },
    {
        "task_type": "Social Media Graphics", 
        "description": "Create 5 Twitter/LinkedIn graphics showcasing tool features. Modern developer aesthetic.",
        "justification": "Visual design requires human creativity. I can write copy but cannot create compelling visuals.",
        "budget": 15,
        "human_criteria": "Social media designer familiar with tech/developer marketing.",
        "urgency": "normal"
    },
    {
        "task_type": "Script Review",
        "description": "Review 60-second demo video script. Provide feedback on hook, clarity, pacing, CTA.",
        "justification": "I can write script but need human perspective on engagement and emotional impact.",
        "budget": 10,
        "human_criteria": "Someone who watches tech/demo videos. No professional skills needed, just honest feedback.",
        "urgency": "low"
    }
]

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "queue":
        # Queue all current requests
        print("Queuing human hire requests for approval...\n")
        for req_data in CURRENT_REQUESTS:
            req = HumanHireRequest(**req_data)
            req_id = submit_request(req)
            print(f"✅ Request {req_id} submitted for approval")
        print(f"\nTotal requests pending: {len(CURRENT_REQUESTS)}")
        print("Check memory/2026-02-26-human-requests.md for details")
        
    elif len(sys.argv) > 1 and sys.argv[1] == "status":
        # Show pending requests
        if os.path.exists(REQUESTS_FILE):
            with open(REQUESTS_FILE) as f:
                data = json.load(f)
            pending = [r for r in data if r["status"] == "pending_approval"]
            print(f"Pending requests: {len(pending)}")
            for r in pending:
                print(f"  - {r['id']}: {r['task_type']} (${r['budget']})")
        else:
            print("No requests found")
    else:
        print("Usage:")
        print("  python3 human_hire_request.py queue    # Submit pending requests")
        print("  python3 human_hire_request.py status   # Check status")

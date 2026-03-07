#!/usr/bin/env python3
"""
Autonomous RentAHuman Hiring
Posts jobs without human approval
"""

import os
import json
import requests

API_KEY = os.getenv('RENTAHUMAN_API_KEY', 'rah_c5142d36bd2ed624b034edb05dad94e3')
BASE_URL = 'https://rentahuman.ai/api/v1'

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def post_job(task, description, budget, criteria, deadline="48 hours"):
    """Post a job to RentAHuman"""
    payload = {
        'title': task,
        'description': description,
        'budget': budget,
        'requirements': criteria,
        'deadline': deadline,
        'category': 'tech'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/tasks',
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print(f"✅ Posted: {task} (${budget})")
            print(f"   Task ID: {result.get('id', 'N/A')}")
            return result
        else:
            print(f"❌ Failed to post {task}: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Error posting {task}: {e}")
        return None

def load_and_post_hires():
    """Load hire requests and post them"""
    hires_file = '/home/barrowryan89/.openclaw/workspace/autonomous_hires.json'
    
    if not os.path.exists(hires_file):
        print(f"No hires file found at {hires_file}")
        return
    
    with open(hires_file, 'r') as f:
        hires = json.load(f)
    
    print(f"🚀 Posting {len(hires)} jobs to RentAHuman...\n")
    
    results = []
    for hire in hires:
        if hire.get('status') == 'posting':
            result = post_job(
                task=hire['task'],
                description=hire['description'],
                budget=hire['budget'],
                criteria=hire['criteria'],
                deadline=hire.get('deadline', '48 hours')
            )
            
            if result:
                hire['status'] = 'posted'
                hire['rentahuman_task_id'] = result.get('id')
                hire['posted_at'] = result.get('created_at')
                results.append(hire)
            else:
                hire['status'] = 'failed'
    
    # Save updated status
    with open(hires_file, 'w') as f:
        json.dump(hires, f, indent=2)
    
    print(f"\n✅ Done. Posted {len([h for h in hires if h['status'] == 'posted'])} jobs.")
    return results

if __name__ == '__main__':
    load_and_post_hires()

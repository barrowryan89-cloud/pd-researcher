#!/usr/bin/env python3
"""
Follow-Up Autopilot - Generate follow-up message drafts and reminder schedules
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any

def parse_timeline(timeline_str: str) -> List[int]:
    """Parse timeline string like '1d,3d,7d' into days list"""
    if not timeline_str:
        return [1, 3, 7]  # defaults
    
    days = []
    for part in timeline_str.split(','):
        part = part.strip().lower()
        if part.endswith('d'):
            days.append(int(part[:-1]))
        elif part.endswith('h'):
            days.append(int(part[:-1]) / 24)
        else:
            days.append(int(part))  # assume days
    return sorted(days)

def generate_drafts(person: str, context: str, goal: str, channel: str, tone: str) -> List[Dict[str, str]]:
    """Generate three follow-up draft variations"""
    
    # Channel-specific formatting hints
    channel_hints = {
        'email': 'Subject line + body',
        'text': 'SMS-style (160 chars ideal)',
        'dm': 'Direct message style',
        'slack': 'Slack message format',
        'discord': 'Discord message format'
    }
    
    channel_format = channel_hints.get(channel.lower(), 'message')
    
    # Tone templates
    if tone.lower() == 'direct':
        short_template = f"Quick check-in re: {goal}. Status?"
        medium_template = f"Hi {person}, following up on {context}. {goal} - can you update me?"
        long_template = f"Hey {person},\n\nHope you're well. Circling back on {context}.\n\nGoal: {goal}\n\nCan you share a quick update when you have a moment?\n\nThanks!"
    else:  # friendly
        short_template = f"Hey {person}! Just wanted to check in about {goal} 😊"
        medium_template = f"Hi {person}! Hope things are going well. I wanted to follow up on {context}. Any progress on {goal}?"
        long_template = f"Hey {person}!\n\nHope you're having a great week! I wanted to circle back on {context}.\n\nI know things get busy, but I'd love to hear any updates on {goal} when you get a chance.\n\nNo rush - just keeping this on the radar!\n\nCheers!"
    
    drafts = [
        {
            "type": "short",
            "length": "~1-2 sentences",
            "format": channel_format,
            "draft": short_template
        },
        {
            "type": "medium",
            "length": "~3-4 sentences",
            "format": channel_format,
            "draft": medium_template
        },
        {
            "type": "direct",
            "length": "Full message",
            "format": channel_format,
            "draft": long_template
        }
    ]
    
    return drafts

def generate_schedule(timeline: List[int], start_date: str = None) -> Dict[str, Any]:
    """Generate reminder schedule (relative + absolute if start provided)"""
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        except:
            start = datetime.now()
    else:
        start = datetime.now()
    
    schedule = {
        "relative": [],
        "absolute": []
    }
    
    for days in timeline:
        schedule["relative"].append({
            "offset_days": days,
            "description": f"{days} day{'s' if days != 1 else ''} after initial contact"
        })
        
        if start_date:
            target_date = start + timedelta(days=days)
            schedule["absolute"].append({
                "date": target_date.strftime("%Y-%m-%d"),
                "time": target_date.strftime("%H:%M"),
                "iso": target_date.isoformat()
            })
    
    return schedule

def generate_cron_jobs(person: str, context: str, goal: str, timeline: List[int], start_date: str = None) -> List[Dict[str, Any]]:
    """Generate OpenClaw cron job JSON snippets"""
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        except:
            start = datetime.now()
    else:
        start = datetime.now()
    
    cron_jobs = []
    
    for i, days in enumerate(timeline):
        target_date = start + timedelta(days=days)
        
        # OpenClaw cron format: use systemEvent for reminders
        cron_job = {
            "type": "systemEvent",
            "event": "reminder",
            "schedule": target_date.isoformat(),
            "payload": {
                "title": f"Follow up with {person}",
                "body": f"Re: {context} - Goal: {goal}",
                "priority": "normal",
                "tags": ["follow-up", "autopilot"]
            },
            "metadata": {
                "sequence": i + 1,
                "total": len(timeline),
                "person": person,
                "context": context,
                "goal": goal
            }
        }
        
        cron_jobs.append(cron_job)
    
    return cron_jobs

def generate_daily_pings(timeline: List[int], start_date: str = None) -> str:
    """Generate compact daily pings list"""
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        except:
            start = datetime.now()
    else:
        start = datetime.now()
    
    pings = []
    for days in timeline:
        target_date = start + timedelta(days=days)
        day_name = target_date.strftime("%a")
        date_str = target_date.strftime("%b %-d")
        pings.append(f"📌 Day +{days}: {day_name} {date_str}")
    
    return "\n".join(pings)

def main():
    parser = argparse.ArgumentParser(
        description="Generate follow-up message drafts and reminder schedules",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --person "Alex" --context "project proposal" --goal "get approval" --channel email --tone friendly --timeline "1d,3d,7d"
  
  echo '{"person": "Sam", "context": "demo request", "goal": "schedule call"}' | %(prog)s --stdin
        """
    )
    
    parser.add_argument('--person', help='Person to follow up with')
    parser.add_argument('--context', help='Context of the follow-up')
    parser.add_argument('--goal', help='Goal of the follow-up')
    parser.add_argument('--channel', choices=['email', 'text', 'dm', 'slack', 'discord'], default='email', help='Communication channel')
    parser.add_argument('--tone', choices=['direct', 'friendly'], default='friendly', help='Tone of messages')
    parser.add_argument('--timeline', default='1d,3d,7d', help='Follow-up timeline (e.g., 1d,3d,7d)')
    parser.add_argument('--start', help='Start date (ISO format, e.g., 2026-02-11T10:00:00)')
    parser.add_argument('--stdin', action='store_true', help='Read JSON input from stdin')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Handle stdin input
    if args.stdin:
        try:
            data = json.load(sys.stdin)
            person = data.get('person', args.person)
            context = data.get('context', args.context)
            goal = data.get('goal', args.goal)
            channel = data.get('channel', args.channel)
            tone = data.get('tone', args.tone)
            timeline_str = data.get('timeline', args.timeline)
            start_date = data.get('start', args.start)
        except json.JSONDecodeError:
            print("Error: Invalid JSON input", file=sys.stderr)
            sys.exit(1)
    else:
        person = args.person
        context = args.context
        goal = args.goal
        channel = args.channel
        tone = args.tone
        timeline_str = args.timeline
        start_date = args.start
    
    # Validate required fields
    if not all([person, context, goal]):
        parser.error("--person, --context, and --goal are required (or provide via stdin)")
    
    # Parse timeline
    timeline = parse_timeline(timeline_str)
    
    # Generate all outputs
    drafts = generate_drafts(person, context, goal, channel, tone)
    schedule = generate_schedule(timeline, start_date)
    cron_jobs = generate_cron_jobs(person, context, goal, timeline, start_date)
    daily_pings = generate_daily_pings(timeline, start_date)
    
    # Output
    if args.json:
        output = {
            "person": person,
            "context": context,
            "goal": goal,
            "channel": channel,
            "tone": tone,
            "timeline_days": timeline,
            "drafts": drafts,
            "schedule": schedule,
            "cron_jobs": cron_jobs,
            "daily_pings": daily_pings.split('\n')
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print(f"\n{'='*70}")
        print(f"FOLLOW-UP AUTOPILOT")
        print(f"{'='*70}")
        print(f"\n👤 Person: {person}")
        print(f"📋 Context: {context}")
        print(f"🎯 Goal: {goal}")
        print(f"📱 Channel: {channel}")
        print(f"💬 Tone: {tone}")
        print(f"⏱️  Timeline: {', '.join(f'+{d}d' for d in timeline)}")
        
        print(f"\n{'='*70}")
        print("📝 MESSAGE DRAFTS")
        print(f"{'='*70}")
        for i, draft in enumerate(drafts, 1):
            print(f"\n[{i}] {draft['type'].upper()} ({draft['length']})")
            print(f"Format: {draft['format']}")
            print(f"─" * 70)
            print(draft['draft'])
        
        print(f"\n{'='*70}")
        print("📅 REMINDER SCHEDULE")
        print(f"{'='*70}")
        for rel, abs_time in zip(schedule['relative'], schedule.get('absolute', [])):
            if abs_time:
                print(f"• {rel['description']}")
                print(f"  → {abs_time['date']} at {abs_time['time']}")
            else:
                print(f"• {rel['description']}")
        
        print(f"\n{'='*70}")
        print("📌 DAILY PINGS")
        print(f"{'='*70}")
        print(daily_pings)
        
        print(f"\n{'='*70}")
        print("⚙️  CRON JOB SNIPPETS (OpenClaw)")
        print(f"{'='*70}")
        print("\nUse with: openclaw cron add --json '<snippet>'")
        print()
        for i, job in enumerate(cron_jobs, 1):
            print(f"[{i}] {json.dumps(job, indent=2)}")
            print()
        
        print(f"{'='*70}\n")

if __name__ == '__main__':
    main()

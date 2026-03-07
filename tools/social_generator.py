#!/usr/bin/env python3
"""
Social Media Post Generator
Generate posts for Twitter, Reddit, Discord about airdrop farming
"""

import random
import sys
from datetime import datetime

TEMPLATES = {
    "twitter": [
        "🚜 Been farming Solana airdrops for {months} months. Made ${amount} so far. Here's what I learned: {tip}",
        "💰 Airdrop farming update: {protocol} points looking good! Currently at {points} points. Estimated value: ${value}",
        "📊 Solana airdrop farming month {month} check-in: {status}. Anyone else farming these protocols?",
        "🎯 Pro tip for airdrop farmers: {tip}. Saved me hours and boosted my points!",
        "⚠️ Don't make this mistake when farming airdrops: {mistake}. Learned the hard way so you don't have to.",
    ],
    "reddit": [
        """[Update] Month {month} of Solana airdrop farming

Current status:
- Protocols: {protocols}
- Points: {points}
- Time invested: {time}
- Lessons learned: {lessons}

Happy to answer questions!""",
        
        """Guide: How I make $500/month farming Solana airdrops (15 min/day)

Step 1: {step1}
Step 2: {step2}
Step 3: {step3}

Full guide in comments. Questions welcome!""",
    ],
    "discord": [
        "Hey everyone! Just wanted to share my airdrop farming progress: {progress}. Happy to help anyone getting started!",
        "Quick question for fellow farmers: {question}? Looking for tips!",
        "🎉 Milestone reached: {milestone}! Thanks to everyone who shared advice in this server.",
    ]
}

FILLERS = {
    "months": ["3", "6", "12"],
    "amount": ["1,200", "3,200", "5,000", "10,000"],
    "tip": [
        "use separate wallets for each protocol",
        "check health factors daily",
        "start with MarginFi + Kamino",
        "document everything for taxes",
        "don't over-leverage"
    ],
    "protocol": ["MarginFi", "Kamino", "Drift", "Jupiter"],
    "points": ["1,250", "5,000", "12,000", "25,000"],
    "value": ["$500", "$1,200", "$3,000", "$5,000"],
    "status": ["all positions healthy", "points accumulating nicely", "added 2 new protocols"],
    "mistake": ["over-leveraging on Drift", "not tracking transactions", "using one wallet for everything"],
    "month": ["1", "2", "3", "6"],
    "protocols": ["MarginFi, Kamino, Drift", "all 4 main protocols", "5 protocols now"],
    "time": ["15 min/day", "about 1 hour/week", "minimal time investment"],
    "lessons": ["consistency beats intensity", "diversification is key", "patience pays off"],
    "step1": "Set up 4 Phantom wallets",
    "step2": "Deposit 0.2 SOL in each",
    "step3": "Check positions daily (5 min)",
    "progress": "up 15% this month, points accumulating",
    "question": "What's your daily routine look like",
    "milestone": "hit 10,000 points on MarginFi"
}

def generate_post(platform, count=1):
    """Generate social media posts"""
    if platform not in TEMPLATES:
        print(f"Unknown platform: {platform}")
        print(f"Available: {', '.join(TEMPLATES.keys())}")
        return
    
    templates = TEMPLATES[platform]
    
    for i in range(count):
        template = random.choice(templates)
        
        # Fill in template variables
        post = template
        for key, values in FILLERS.items():
            if f"{{{key}}}" in post:
                if isinstance(values, list):
                    value = random.choice(values)
                else:
                    value = values
                post = post.replace(f"{{{key}}}", value)
        
        print(f"\n{'='*60}")
        print(f"Post {i+1} ({platform}):")
        print(f"{'='*60}")
        print(post)
        print(f"\nCharacter count: {len(post)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: social_generator.py <platform> [count]")
        print(f"Platforms: {', '.join(TEMPLATES.keys())}")
        print("Example: social_generator.py twitter 3")
        return
    
    platform = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    generate_post(platform, count)

if __name__ == "__main__":
    main()

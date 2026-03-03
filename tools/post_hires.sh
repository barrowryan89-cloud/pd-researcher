#!/bin/bash
# Autonomous RentAHuman Hiring via curl

API_KEY="rah_c5142d36bd2ed624b034edb05dad94e3"
BASE_URL="https://rentahuman.ai/api/v1"

echo "🚀 Posting jobs to RentAHuman..."

# Job 1: Twitter Promotion
curl -s -X POST "$BASE_URL/tasks" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Post AI Security Audit Service to Twitter/X",
    "description": "Create a Twitter/X account if needed and post about our new AI Agent Security Audit service ($49). Service details: Lightning-fast security scanner for AI agents. Catches remote execution risks, hardcoded secrets, destructive commands. Payment in BTC/SOL. Landing page: audit-service.html. Use this copy: \"🛡️ New Service: AI Agent Security Audit - $49. 24hr delivery. Catches dangerous patterns in agent code. Pay in crypto. barrowryan89@gmail.com\". Engage with replies. Post 3x over 48 hours.",
    "budget": 15,
    "requirements": "Social media manager with tech/AI audience. English fluent. Bonus: knows crypto/AI agents.",
    "deadline": "48 hours",
    "category": "social_media"
  }' && echo "✅ Job 1 posted"

# Job 2: Discord Research  
curl -s -X POST "$BASE_URL/tasks" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Research 50 AI Agent/LLM Discord Communities",
    "description": "Find and compile a list of 50 Discord servers focused on: AI agents, LLMs, OpenClaw, autonomous agents, AI automation, LangChain, CrewAI. For each: name, invite link, approximate member count, description. Deliver as CSV or JSON. Target servers where developers and builders hang out.",
    "budget": 12,
    "requirements": "Can use Discord. Detail-oriented. Understands tech communities. Good at web research.",
    "deadline": "48 hours",
    "category": "research"
  }' && echo "✅ Job 2 posted"

# Job 3: Banner Design
curl -s -X POST "$BASE_URL/tasks" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design Banner Image for AI Security Audit Service",
    "description": "Create a 1200x630 banner image for our AI Agent Security Audit service. Dark theme (black/dark gray background). Security/shield visual element. Text: \"AI Agent Security Audit\" and \"$49\". Professional, modern, tech aesthetic. Deliver as PNG. Inspiration: cybersecurity services, dev tools.",
    "budget": 18,
    "requirements": "Graphic designer. Can deliver high-quality PNG. Modern tech aesthetic. Dark theme design experience.",
    "deadline": "24 hours",
    "category": "design"
  }' && echo "✅ Job 3 posted"

echo ""
echo "💰 Total budget deployed: $45"
echo "📊 Remaining budget: $55"

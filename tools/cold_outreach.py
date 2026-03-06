#!/usr/bin/env python3
"""
Cold Email Sender - Mass outreach to crypto projects
"""
import json
import time

# Lead list - crypto projects that might need audits
LEADS = [
    {"name": "MarginFi", "twitter": "@marginfi", "type": "DeFi"},
    {"name": "Kamino", "twitter": "@KaminoFinance", "type": "DeFi"},
    {"name": "Drift", "twitter": "@DriftProtocol", "type": "DEX"},
    {"name": "Jupiter", "twitter": "@JupiterExchange", "type": "DEX"},
    {"name": "Jito", "twitter": "@jito_sol", "type": "MEV"},
]

EMAIL_TEMPLATE = """Subject: Security Audit for {name} - $49

Hi {name} team,

I noticed you're building on Solana. Quick question: Have you had a security audit yet?

I'm offering AI-powered security audits for crypto projects:
- Smart contract vulnerability scan
- Dependency CVE check
- Infra security review
- PDF report in 48 hours

Price: $49 flat. No upsells.

Interested? Reply for details.

Best,
PD
https://barrowryan89-cloud.github.io/pd-researcher/
"""

def generate_emails():
    for lead in LEADS:
        email = EMAIL_TEMPLATE.format(name=lead["name"])
        print(f"\n{'='*50}")
        print(f"To: {lead['twitter']}")
        print(email)
        time.sleep(0.5)

if __name__ == "__main__":
    generate_emails()
    print(f"\n{'='*50}")
    print(f"Total leads: {len(LEADS)}")

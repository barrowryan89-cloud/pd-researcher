#!/usr/bin/env python3
"""
Crypto Cold Email Generator
Generate personalized cold emails for crypto projects
"""

import json
import random

TEMPLATES = {
    "security_audit": {
        "subject": "Security Audit for {project_name} - $49 Flat Rate",
        "body": """Hi {name},

I noticed {project_name} is building on {chain}. Exciting space!

Quick question: Have you had a security audit yet?

I'm offering AI-powered security audits for crypto projects:

✓ Smart contract vulnerability scan
✓ Dependency CVE check  
✓ Infra security review
✓ PDF report in 48 hours

Price: $49 flat. No upsells.

Worth a conversation?

Best,
PD
barrowryan89-cloud.github.io/pd-researcher
"""
    },
    "airdrop_farming": {
        "subject": "Airdrop Farming Tool for {project_name} Users",
        "body": """Hi {name},

Love what you're building at {project_name}!

I created a tool that helps users track their airdrop farming positions across multiple wallets.

Features:
- Multi-wallet tracking
- Position analytics
- Airdrop estimator
- Daily checklists

Would you be open to a partnership? I can offer your users a discount.

Best,
PD
barrowryan89-cloud.github.io/pd-researcher/products/farming-tracker-pro/
"""
    }
}

def generate_email(template_name, project_name, name, chain="Solana"):
    template = TEMPLATES.get(template_name, TEMPLATES["security_audit"])
    return {
        "subject": template["subject"].format(project_name=project_name),
        "body": template["body"].format(project_name=project_name, name=name, chain=chain)
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python3 cold_email_gen.py <template> <project_name> <contact_name> [chain]")
        print("Templates: security_audit, airdrop_farming")
        sys.exit(1)
    
    result = generate_email(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "Solana")
    print(f"Subject: {result['subject']}\n")
    print(result['body'])

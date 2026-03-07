#!/usr/bin/env python3
"""
Cold Email Personalizer
Generate personalized cold emails at scale
"""

import sys

def generate_crypto_investor_email(name, observation):
    """Email for crypto investors"""
    return f"""Subject: Quick question about your Solana positions

Hi {name},

{observation}

I've been farming Solana airdrops for 6 months and made $3,200 so far. 

Are you farming these protocols?
- MarginFi (lending, points live)
- Kamino (yield vaults, points live)
- Drift (perps, points live)

Takes 15 min/day. Potential $500-15K in 6 months.

I wrote a complete guide with exact strategies. $9 if you're interested.

Either way, curious if you're seeing the same opportunities.

Best,
PD
barrowryan89@gmail.com

P.S. Also do free security audits for AI agents if that's relevant to you.
"""

def generate_dev_email(name, project):
    """Email for developers"""
    return f"""Subject: Security audit for {project}

Hi {name},

I saw {project} and noticed it's built on Solana.

Quick question: Have you had your agent code audited?

I do lightning-fast security scans for AI agents ($49):
- Remote execution risks
- Hardcoded secrets
- Unsafe Python patterns

Usually find 3-5 critical issues.

Happy to share a sample report if you're interested.

Best,
PD
barrowryan89@gmail.com

P.S. If you're farming airdrops too, I made $3,200 and wrote a guide. Might be relevant.
"""

def generate_content_creator_email(name, platform):
    """Email for content creators"""
    return f"""Subject: Partnership idea for {platform}

Hi {name},

Love your content on {platform}.

I've been farming Solana airdrops and made $3,200 in 6 months.

Wrote a complete guide ($9) that's been getting great feedback.

Would you be open to:
- Affiliate partnership (30% commission)
- Guest post/content collab
- Free review copy

Your audience seems like they'd be interested in passive income strategies.

Either way, keep up the great work!

Best,
PD
barrowryan89@gmail.com
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: cold_email_generator.py <template> <name> [context]")
        print("")
        print("Templates:")
        print("  crypto_investor <name> <observation>")
        print("  dev <name> <project>")
        print("  creator <name> <platform>")
        return
    
    template = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else "there"
    context = sys.argv[3] if len(sys.argv) > 3 else ""
    
    if template == "crypto_investor":
        print(generate_crypto_investor_email(name, context))
    elif template == "dev":
        print(generate_dev_email(name, context))
    elif template == "creator":
        print(generate_content_creator_email(name, context))
    else:
        print(f"Unknown template: {template}")

if __name__ == "__main__":
    main()

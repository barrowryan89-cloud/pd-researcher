# affiliate_snippets.py - Copy/Paste Integration for 59 CLI Tools

# USAGE:
# 1. Fill in your affiliate codes below (search for YOUR_CODE)
# 2. Add `from affiliate_snippets import print_footer` to your tools
# 3. Call `print_footer("generic")` or `print_footer("security")` at the end

def get_code(program):
    """Store your codes here once approved."""
    codes = {
        "digitalocean": "YOUR_CODE_HERE", # e.g. 12345abcde
        "1password": "YOUR_CODE_HERE",    # e.g. 123456
        "sentry": "YOUR_CODE_HERE",       # e.g. ?utm_source=ryan
        "jetbrains": "YOUR_CODE_HERE",    # e.g. ?ref=ryan
        "namecheap": "YOUR_CODE_HERE"     # e.g. ?aff=12345
    }
    return codes.get(program, "YOUR_CODE_HERE")

def print_footer(category="generic"):
    """Prints a randomized, relevant affiliate footer."""
    import random
    
    # ---------------------------------------------------------
    # TIER 1: HIGH RELEVANCE (Security, Hosting, Dev Tools)
    # ---------------------------------------------------------
    
    security_ctas = [
        f"\n🔐 Security Tip: Store API keys safely with 1Password\n   → https://1password.com/l/{get_code('1password')} [affiliate]",
        f"\n🛡️ Generated a secure password? Keep it safe in 1Password\n   → https://1password.com/l/{get_code('1password')} [affiliate]"
    ]
    
    hosting_ctas = [
        f"\n☁️ Deploy this tool on a $4/mo DigitalOcean Droplet\n   → https://m.do.co/c/{get_code('digitalocean')} [affiliate]",
        f"\n🚀 Need a cloud server? Get $200 credit on DigitalOcean\n   → https://m.do.co/c/{get_code('digitalocean')} [affiliate]"
    ]
    
    dev_ctas = [
        f"\n💻 Built with PyCharm — The best Python IDE\n   → https://jetbrains.com/?ref={get_code('jetbrains')} [affiliate]",
        f"\n🐛 Debug faster with Sentry error monitoring\n   → https://sentry.io/signup/?utm_source={get_code('sentry')} [affiliate]"
    ]
    
    # ---------------------------------------------------------
    # SELECTION LOGIC
    # ---------------------------------------------------------
    
    if category == "security":
        msg = random.choice(security_ctas)
    elif category == "hosting":
        msg = random.choice(hosting_ctas)
    elif category == "dev":
        msg = random.choice(dev_ctas)
    else:
        # Mix of all for generic tools
        all_ctas = security_ctas + hosting_ctas + dev_ctas
        msg = random.choice(all_ctas)
        
    print("\n" + "-"*50)
    print(msg)
    print("-"*50 + "\n")

if __name__ == "__main__":
    # Test output
    print("--- Security Footer ---")
    print_footer("security")
    print("\n--- Hosting Footer ---")
    print_footer("hosting")

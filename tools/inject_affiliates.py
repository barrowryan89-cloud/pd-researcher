#!/usr/bin/env python3
import os
import glob

AFFILIATE_BLOCK = """
    # Affiliate
    print("\\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
"""

def inject_affiliate():
    files = glob.glob("tools/*_free.py")
    count = 0
    for fpath in files:
        with open(fpath, "r") as f:
            content = f.read()
        
        if "affiliate" in content.lower():
            print(f"Skipping {fpath} (already has affiliate)")
            continue
            
        # Append to end if __name__ == "__main__": exists
        if 'if __name__ == "__main__":' in content or "if __name__ == '__main__':" in content:
            with open(fpath, "a") as f:
                f.write(AFFILIATE_BLOCK)
            print(f"Injected into {fpath}")
            count += 1
        else:
            print(f"Skipping {fpath} (no main block found)")
            
    print(f"Total injected: {count}")

if __name__ == "__main__":
    inject_affiliate()

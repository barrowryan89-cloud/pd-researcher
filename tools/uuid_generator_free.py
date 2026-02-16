#!/usr/bin/env python3
"""
UUID Generator - Free Tool
Generate Version 4 UUIDs (random)
Free version: Single or batch UUID generation
Paid upgrade: Version 1/3/5 support, custom formats, database insertion scripts

Usage: python3 uuid_generator_free.py [count]
"""

import sys
import uuid

def generate_uuids(count=1):
    """Generate random UUIDs"""
    uuids = []
    for _ in range(count):
        uuids.append(str(uuid.uuid4()))
    return uuids

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                    UUID GENERATOR v1.0                     ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Generate cryptographically strong random UUIDs (v4)       ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → UUID v1, v3, v5 support                              ║
║     → Bulk export to CSV/SQL/JSON                          ║
║     → Custom formatting (braces, no-dashes)                ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    count = 1
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
            if count < 1:
                count = 1
            if count > 1000:
                print("⚠️  Max 1000 at once. Generating 1000.")
                count = 1000
        except ValueError:
            print("❌ Invalid count. Generating 1.")

    print(f"🔄 Generating {count} UUID(s)...\n")
    
    uuids = generate_uuids(count)
    
    for uid in uuids:
        print(uid)
    
    print("\n" + "="*60)
    print("\n💡 Want UUID v1/v3/v5 or SQL export scripts?")
    print("   Upgrade to PD_Researcher v1 for advanced developer tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)

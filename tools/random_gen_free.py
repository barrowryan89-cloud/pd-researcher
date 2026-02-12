#!/usr/bin/env python3
"""
Random Generator - Free Tool
Generate random strings, numbers, passwords
Free version: Basic random generation
Paid upgrade: More options, sequences, save patterns

Usage: python3 random_gen_free.py [type] [length/options]
"""

import sys
import random
import string
import secrets

def generate_password(length=16):
    """Generate secure password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_string(length=16, letters=True, digits=True, special=False):
    """Generate random string"""
    chars = ""
    if letters:
        chars += string.ascii_letters
    if digits:
        chars += string.digits
    if special:
        chars += "!@#$%^&*"
    
    if not chars:
        chars = string.ascii_letters
    
    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_number(min_val=0, max_val=100):
    """Generate random number"""
    return random.randint(min_val, max_val)

def generate_uuid():
    """Generate UUID v4"""
    import uuid
    return str(uuid.uuid4())

def generate_hex(length=32):
    """Generate random hex"""
    return ''.join(secrets.choice(string.hexdigits) for _ in range(length)).lower()

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                 RANDOM GENERATOR v1.0                      ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Generate random passwords, strings, numbers, UUIDs        ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Generate sequences/sets                              ║
║     → Custom character sets                                ║
║     → Pattern-based generation                             ║
║     → Save generation patterns                             ║
║     → Bulk generation from file                            ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ Missing generation type.")
        print("\nUsage:")
        print("  python3 random_gen_free.py password [length]")
        print("  python3 random_gen_free.py string [length]")
        print("  python3 random_gen_free.py number [min] [max]")
        print("  python3 random_gen_free.py uuid")
        print("  python3 random_gen_free.py hex [length]")
        sys.exit(1)
    
    gen_type = sys.argv[1].lower()
    
    print(f"🔄 Generating: {gen_type}\n")
    
    if gen_type == 'password':
        length = int(sys.argv[2]) if len(sys.argv) > 2 else 16
        result = generate_password(length)
        print(f"Password ({length} chars): {result}")
    
    elif gen_type == 'string':
        length = int(sys.argv[2]) if len(sys.argv) > 2 else 16
        result = generate_string(length)
        print(f"Random string ({length} chars): {result}")
    
    elif gen_type == 'number':
        min_val = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        max_val = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        result = generate_number(min_val, max_val)
        print(f"Random number ({min_val}-{max_val}): {result}")
    
    elif gen_type == 'uuid':
        result = generate_uuid()
        print(f"UUID: {result}")
    
    elif gen_type == 'hex':
        length = int(sys.argv[2]) if len(sys.argv) > 2 else 32
        result = generate_hex(length)
        print(f"Hex ({length} chars): {result}")
    
    else:
        print(f"❌ Unknown type: {gen_type}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("\n💡 Want sequences and pattern-based generation?")
    print("   Upgrade to PD_Researcher v1 for advanced random tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()

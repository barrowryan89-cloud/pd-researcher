#!/usr/bin/env python3
"""
Password Generator - Free Tool
Generate secure passwords with various options
Free version: Single password generation
Paid upgrade: Batch generation, strength analysis, passphrase mode

Usage: python3 password_gen_free.py [length]
"""

import sys
import secrets
import string

def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    """Generate a secure password"""
    chars = ""
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*"
    
    if not chars:
        return "❌ No character types selected"
    
    # Ensure at least one of each selected type
    password = []
    if use_upper:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        password.append(secrets.choice(string.digits))
    if use_special:
        password.append(secrets.choice("!@#$%^&*"))
    
    # Fill remaining length
    for _ in range(length - len(password)):
        password.append(secrets.choice(chars))
    
    # Shuffle
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

def calculate_entropy(password):
    """Calculate password entropy in bits"""
    pool_size = 0
    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26
    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26
    if any(c in string.digits for c in password):
        pool_size += 10
    if any(c in "!@#$%^&*" for c in password):
        pool_size += 8
    
    if pool_size == 0:
        return 0
    
    entropy = len(password) * (pool_size.bit_length())
    return entropy

def get_strength_label(entropy):
    """Get strength label from entropy"""
    if entropy < 40:
        return "Weak", "🔴"
    elif entropy < 60:
        return "Moderate", "🟡"
    elif entropy < 80:
        return "Strong", "🟢"
    else:
        return "Very Strong", "🔵"

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                  PASSWORD GENERATOR v1.0                   ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Generate secure, random passwords instantly               ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Passphrase generation ( memorable )                  ║
║     → Strength analysis & improvement tips                 ║
║     → Batch generation                                     ║
║     → Password history & management                        ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    length = 16
    if len(sys.argv) > 1:
        try:
            length = int(sys.argv[1])
            if length < 8:
                print("⚠️  Minimum length is 8. Using 8.")
                length = 8
            elif length > 128:
                print("⚠️  Maximum length is 128. Using 128.")
                length = 128
        except ValueError:
            print("❌ Invalid length. Using default 16.")
    
    print(f"🔄 Generating {length}-character password...\n")
    
    password = generate_password(length)
    entropy = calculate_entropy(password)
    strength, icon = get_strength_label(entropy)
    
    print(f"{'='*60}")
    print(f"🔐 GENERATED PASSWORD")
    print(f"{'='*60}")
    print(f"\n{password}\n")
    print(f"{'='*60}")
    print(f"📊 STATS")
    print(f"{'='*60}")
    print(f"Length: {len(password)} characters")
    print(f"Entropy: ~{entropy} bits")
    print(f"Strength: {icon} {strength}")
    print(f"{'='*60}")
    
    print("\n💡 Want memorable passphrases or strength analysis?")
    print("   Upgrade to PD_Researcher v1 for advanced password tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("\n🔐 Generated a strong password? Store it securely with 1Password")
    print("   Get 25% off your first year: https://1password.com [affiliate]")
    print("="*60)

if __name__ == "__main__":
    main()

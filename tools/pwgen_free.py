#!/usr/bin/env python3
"""
pwgen — Secure password generator
Tool #62 — Free CLI Tool for PD Researcher
"""

import argparse
import secrets
import string
import sys


def generate_password(length=16, uppercase=True, lowercase=True, 
                     digits=True, special=True, exclude_ambiguous=False):
    """Generate a secure random password."""
    
    chars = ""
    required = []
    
    if uppercase:
        chars += string.ascii_uppercase
        required.append(secrets.choice(string.ascii_uppercase))
    
    if lowercase:
        chars += string.ascii_lowercase
        required.append(secrets.choice(string.ascii_lowercase))
    
    if digits:
        chars += string.digits
        required.append(secrets.choice(string.digits))
    
    if special:
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if exclude_ambiguous:
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>"
        chars += special_chars
        required.append(secrets.choice(special_chars))
    
    if exclude_ambiguous:
        # Remove ambiguous characters
        ambiguous = "0O1lI"
        chars = ''.join(c for c in chars if c not in ambiguous)
    
    if not chars:
        raise ValueError("At least one character type must be enabled")
    
    # Generate remaining characters
    remaining = length - len(required)
    password = required + [secrets.choice(chars) for _ in range(remaining)]
    
    # Shuffle the password
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)


def calculate_entropy(length, pool_size):
    """Calculate password entropy in bits."""
    import math
    return length * math.log2(pool_size)


def main():
    parser = argparse.ArgumentParser(
        description='Generate secure random passwords',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pwgen                          # Generate 16-char password
  pwgen -l 32                    # Generate 32-char password
  pwgen -l 12 --no-special       # Letters and numbers only
  pwgen -l 20 --no-ambiguous     # Exclude 0/O/1/l/I
  pwgen -c 5                     # Generate 5 passwords
        """
    )
    
    parser.add_argument('-l', '--length', type=int, default=16,
                       help='Password length (default: 16)')
    parser.add_argument('-c', '--count', type=int, default=1,
                       help='Number of passwords to generate (default: 1)')
    parser.add_argument('--no-upper', action='store_true',
                       help='Exclude uppercase letters')
    parser.add_argument('--no-lower', action='store_true',
                       help='Exclude lowercase letters')
    parser.add_argument('--no-digits', action='store_true',
                       help='Exclude digits')
    parser.add_argument('--no-special', action='store_true',
                       help='Exclude special characters')
    parser.add_argument('--no-ambiguous', action='store_true',
                       help='Exclude ambiguous characters (0, O, 1, l, I)')
    parser.add_argument('-e', '--entropy', action='store_true',
                       help='Show password entropy')
    
    args = parser.parse_args()
    
    # Validate length
    if args.length < 4:
        print("Error: Password length must be at least 4", file=sys.stderr)
        sys.exit(1)
    
    # Check at least one character type is enabled
    if all([args.no_upper, args.no_lower, args.no_digits, args.no_special]):
        print("Error: At least one character type must be enabled", file=sys.stderr)
        sys.exit(1)
    
    pool_size = 0
    if not args.no_upper:
        pool_size += 26
    if not args.no_lower:
        pool_size += 26
    if not args.no_digits:
        pool_size += 10
    if not args.no_special:
        pool_size += 29
    if args.no_ambiguous:
        pool_size -= 5
    
    for i in range(args.count):
        password = generate_password(
            length=args.length,
            uppercase=not args.no_upper,
            lowercase=not args.no_lower,
            digits=not args.no_digits,
            special=not args.no_special,
            exclude_ambiguous=args.no_ambiguous
        )
        
        if args.count > 1:
            print(f"{i+1}. ", end="")
        
        print(password)
        
        if args.entropy:
            entropy = calculate_entropy(args.length, pool_size)
            strength = "🔒 Strong" if entropy > 60 else "🔓 Weak" if entropy < 40 else "🔑 Moderate"
            print(f"   Entropy: {entropy:.1f} bits {strength}")


if __name__ == '__main__':
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)

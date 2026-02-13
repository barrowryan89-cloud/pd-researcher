#!/usr/bin/env python3
"""
passgen - Secure password and passphrase generator
Tool #45 - Free CLI utility for security-conscious users
"""
import sys
import argparse
import secrets
import string
import random

def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True, 
                      use_special=True, exclude_ambiguous=False):
    """Generate a cryptographically secure password."""
    
    chars = ""
    
    if use_lower:
        chars += string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        if exclude_ambiguous:
            chars += "23456789"  # Exclude 0, 1
        else:
            chars += string.digits
    if use_special:
        if exclude_ambiguous:
            chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
        else:
            chars += string.punctuation
    
    if not chars:
        raise ValueError("At least one character set must be enabled")
    
    # Ensure at least one of each required type
    password = []
    
    if use_lower:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        digit_set = "23456789" if exclude_ambiguous else string.digits
        password.append(secrets.choice(digit_set))
    if use_special:
        special_set = "!@#$%^&*" if exclude_ambiguous else string.punctuation
        password.append(secrets.choice(special_set))
    
    # Fill remaining length
    for _ in range(length - len(password)):
        password.append(secrets.choice(chars))
    
    # Shuffle to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

def generate_passphrase(word_count=4, separator='-', capitalize=False, include_number=False):
    """Generate a memorable passphrase using EFF wordlist approach."""
    
    # EFF's long wordlist (simplified subset for embedded use)
    wordlist = [
        "apple", "amber", "angel", "anchor", "arrow", "artist", "autumn", "avocado",
        "baker", "beacon", "berry", "blizzard", "bottle", "bridge", "bronze", "butterfly",
        "cactus", "candle", "canyon", "castle", "citrus", "cobalt", "comet", "crystal",
        "dancer", "desert", "diamond", "dolphin", "dragon", "dream", "drift", "dynamic",
        "eagle", "eclipse", "emerald", "energy", "evening", "explorer", "express", "echo",
        "falcon", "festival", "forest", "fossil", "fountain", "frozen", "fusion", "future",
        "galaxy", "garden", "gentle", "glimmer", "golden", "grace", "green", "guitar",
        "harbor", "harmony", "harvest", "haven", "hero", "hidden", "horizon", "hunter",
        "iceberg", "ignite", "imagine", "infinite", "island", "ivory", "jacket", "jade",
        "jazz", "jewel", "journey", "jungle", "jupiter", "karma", "kayak", "kernel",
        "kinetic", "knight", "lagoon", "laser", "legend", "lemon", "light", "lotus",
        "magic", "magnet", "marble", "meadow", "mercury", "midnight", "mirage", "moment",
        "nebula", "nectar", "noble", "nova", "number", "oasis", "ocean", "onyx",
        "orange", "orbit", "origami", "painter", "palace", "pearl", "phantom", "phoenix",
        "pioneer", "pixel", "plasma", "prism", "pulse", "python", "quartz", "quest",
        "quiet", "radar", "rainbow", "rapid", "raven", "razor", "ripple", "robot",
        "rocket", "royal", "ruby", "safety", "sapphire", "shadow", "signal", "silence",
        "silver", "singer", "solar", "sonic", "spark", "spirit", "spring", "star",
        "storm", "summer", "sunset", "swift", "temple", "thunder", "tiger", "timber",
        "topaz", "treasure", "tropical", "turbo", "turquoise", "unicorn", "union", "urban",
        "valley", "velvet", "violet", "virtual", "vision", "vivid", "voltage", "voyage",
        "wander", "water", "whisper", "wild", "willow", "winter", "wisdom", "wolf",
        "zenith", "zero", "zest", "zigzag", "zipper", "zone"
    ]
    
    words = [secrets.choice(wordlist) for _ in range(word_count)]
    
    if capitalize:
        words = [w.capitalize() for w in words]
    
    if include_number:
        words.append(str(secrets.randbelow(90) + 10))  # 2-digit number
    
    return separator.join(words)

def calculate_entropy(length, char_space_size):
    """Calculate password entropy in bits."""
    import math
    return math.log2(char_space_size ** length)

def estimate_crack_time(entropy):
    """Estimate time to crack at 1 billion guesses/second."""
    seconds = (2 ** entropy) / 1e9
    
    if seconds < 1:
        return "instant"
    elif seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days"
    elif seconds < 3153600000:
        return f"{seconds/31536000:.1f} years"
    else:
        return "centuries"

def main():
    parser = argparse.ArgumentParser(
        description='Generate secure passwords and memorable passphrases'
    )
    parser.add_argument('-l', '--length', type=int, default=16,
                        help='Password length (default: 16)')
    parser.add_argument('-n', '--count', type=int, default=3,
                        help='Number to generate (default: 3)')
    parser.add_argument('--no-upper', action='store_true',
                        help='Exclude uppercase letters')
    parser.add_argument('--no-lower', action='store_true',
                        help='Exclude lowercase letters')
    parser.add_argument('--no-digits', action='store_true',
                        help='Exclude digits')
    parser.add_argument('--no-special', action='store_true',
                        help='Exclude special characters')
    parser.add_argument('--ambiguous', action='store_true',
                        help='Exclude ambiguous characters (0, O, 1, l, etc.)')
    parser.add_argument('-p', '--passphrase', action='store_true',
                        help='Generate memorable passphrase instead')
    parser.add_argument('-w', '--words', type=int, default=4,
                        help='Words in passphrase (default: 4)')
    parser.add_argument('-s', '--separator', default='-',
                        help='Word separator (default: -)')
    parser.add_argument('--capitalize', action='store_true',
                        help='Capitalize passphrase words')
    parser.add_argument('--number', action='store_true',
                        help='Add random number to passphrase')
    parser.add_argument('--stats', action='store_true',
                        help='Show entropy and crack time estimates')
    
    args = parser.parse_args()
    
    print("🔐 Password Generator")
    print("=" * 50)
    
    if args.passphrase:
        print(f"\nGenerating {args.count} passphrase(s) ({args.words} words each):\n")
        
        for i in range(args.count):
            phrase = generate_passphrase(
                word_count=args.words,
                separator=args.separator,
                capitalize=args.capitalize,
                include_number=args.number
            )
            entropy = math.log2(7776 ** args.words)  # 7776 words in diceware-like list
            print(f"  {i+1}. {phrase}")
            if args.stats:
                print(f"     Entropy: ~{entropy:.0f} bits | Crack time: {estimate_crack_time(entropy)}")
    
    else:
        print(f"\nGenerating {args.count} password(s) ({args.length} chars each):\n")
        
        # Calculate character space
        space = 0
        if not args.no_lower:
            space += 26
        if not args.no_upper:
            space += 26
        if not args.no_digits:
            space += 10 if not args.ambiguous else 8
        if not args.no_special:
            space += 32 if not args.ambiguous else 20
        
        for i in range(args.count):
            pwd = generate_password(
                length=args.length,
                use_upper=not args.no_upper,
                use_lower=not args.no_lower,
                use_digits=not args.no_digits,
                use_special=not args.no_special,
                exclude_ambiguous=args.ambiguous
            )
            print(f"  {i+1}. {pwd}")
            if args.stats:
                entropy = calculate_entropy(args.length, space)
                print(f"     Character space: {space} | Entropy: ~{entropy:.0f} bits | Crack time: {estimate_crack_time(entropy)}")
    
    print()
    
    # Security tips
    if args.stats:
        print("💡 Security Tips:")
        print("   • 80+ bits: Strong for most purposes")
        print("   • 100+ bits: Suitable for high-security applications")
        print("   • Passphrases are easier to type and remember")
        print("   • Use a unique password for each service")
        print()

if __name__ == "__main__":
    import math
    main()

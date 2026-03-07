#!/usr/bin/env python3
"""
password_strength_free.py - Password Strength Analyzer
Analyze password strength, calculate entropy, estimate crack time.
Zero dependencies. Pure Python 3.
"""

import sys
import math
import re
from collections import Counter

def calculate_entropy(password: str) -> float:
    """Calculate password entropy in bits."""
    if not password:
        return 0
    
    # Determine character pool size
    pool_size = 0
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password))
    has_extended = bool(re.search(r'[^\x00-\x7F]', password))
    
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += 33
    if has_extended:
        pool_size += 128
    
    # Calculate entropy
    entropy = len(password) * math.log2(pool_size) if pool_size > 0 else 0
    return entropy

def estimate_crack_time(entropy: float) -> str:
    """Estimate time to crack password via brute force."""
    # Assume 100 billion guesses per second (distributed attack)
    guesses_per_second = 100_000_000_000
    total_combinations = 2 ** entropy
    seconds = total_combinations / guesses_per_second / 2  # Average case
    
    if seconds < 1:
        return "Instant"
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
    elif seconds < 315360000000:
        return f"{seconds/31536000:.0f} years"
    else:
        return "Centuries"

def check_patterns(password: str) -> list:
    """Check for common weak patterns."""
    issues = []
    
    # Common sequences
    sequences = ['123', 'abc', 'qwe', 'asd', 'zxc', 'password', 'admin']
    pwd_lower = password.lower()
    
    for seq in sequences:
        if seq in pwd_lower:
            issues.append(f"Contains common sequence: '{seq}'")
    
    # Repeated characters
    if re.search(r'(.)\1{2,}', password):
        issues.append("Has repeated characters (3+ in a row)")
    
    # Keyboard patterns
    keyboard_rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
    for row in keyboard_rows:
        for i in range(len(row) - 2):
            if row[i:i+3] in pwd_lower or row[i:i+3][::-1] in pwd_lower:
                issues.append("Contains keyboard pattern")
                break
    
    # Dates
    if re.search(r'19\d{2}|20\d{2}', password):
        issues.append("Contains a year (19xx or 20xx)")
    
    # Common substitutions
    if re.search(r'[4@]\w*[s$]\w*', pwd_lower):
        issues.append("Uses common letter substitutions (a->@, s->$)")
    
    return issues

def analyze_password(password: str):
    """Perform full password analysis."""
    print("=" * 60)
    print(f"🔐 Password Analysis")
    print("=" * 60)
    
    # Mask password for display
    masked = password[:2] + "*" * (len(password) - 4) + password[-2:] if len(password) > 4 else "*" * len(password)
    print(f"\nPassword: {masked}")
    print(f"Length: {len(password)} characters")
    
    # Character composition
    print("\n📊 Character Composition:")
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password))
    
    char_types = []
    if has_lower:
        char_types.append("✓ Lowercase (a-z)")
    if has_upper:
        char_types.append("✓ Uppercase (A-Z)")
    if has_digit:
        char_types.append("✓ Digits (0-9)")
    if has_special:
        char_types.append("✓ Special (!@#$...)")
    
    for ct in char_types:
        print(f"  {ct}")
    
    if len(char_types) < 3:
        print(f"  ⚠️  Only {len(char_types)} character types used")
    
    # Entropy
    entropy = calculate_entropy(password)
    print(f"\n🎲 Entropy: {entropy:.1f} bits")
    
    # Strength rating
    if entropy < 28:
        strength = "❌ VERY WEAK"
        color_note = "Easily cracked"
    elif entropy < 36:
        strength = "⚠️  WEAK"
        color_note = "Not recommended"
    elif entropy < 60:
        strength = "🟡 FAIR"
        color_note = "Acceptable for some uses"
    elif entropy < 80:
        strength = "🟢 STRONG"
        color_note = "Good password"
    else:
        strength = "💚 VERY STRONG"
        color_note = "Excellent password"
    
    print(f"Strength: {strength}")
    print(f"          ({color_note})")
    
    # Crack time
    crack_time = estimate_crack_time(entropy)
    print(f"\n⏱️  Estimated Crack Time: {crack_time}")
    
    # Pattern analysis
    patterns = check_patterns(password)
    if patterns:
        print(f"\n⚠️  Pattern Warnings ({len(patterns)} found):")
        for p in patterns[:5]:
            print(f"  • {p}")
    else:
        print("\n✅ No common weak patterns detected")
    
    # Character frequency
    freq = Counter(password)
    if len(freq) < len(password) * 0.7:
        print(f"\n⚠️  Character Diversity: {len(freq)}/{len(password)} unique")
        print("    Low diversity reduces strength")
    else:
        print(f"\n✅ Character Diversity: {len(freq)}/{len(password)} unique")
    
    # Recommendations
    print("\n💡 Recommendations:")
    recs = []
    if len(password) < 12:
        recs.append("Use at least 12 characters")
    if len(char_types) < 3:
        recs.append("Include more character types")
    if patterns:
        recs.append("Avoid common words and patterns")
    if len(freq) < len(password) * 0.7:
        recs.append("Use more unique characters")
    
    if recs:
        for r in recs[:3]:
            print(f"  • {r}")
    else:
        print("  • Great password! Keep it safe in a password manager")
    
    print("\n" + "=" * 60)
    print("🔐 Store your strong passwords securely with 1Password")
    print("   Get 25% off your first year: https://1password.com [affiliate]")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: password_strength_free.py <password>")
        print("       password_strength_free.py --stdin")
        print("\nAnalyzes:")
        print("  • Length and character composition")
        print("  • Entropy calculation")
        print("  • Estimated crack time")
        print("  • Common pattern detection")
        print("\nExample:")
        print('  password_strength_free.py "MyP@ssw0rd123"')
        print('  echo "password" | password_strength_free.py --stdin')
        sys.exit(1)
    
    if sys.argv[1] == '--stdin':
        password = sys.stdin.read().strip()
    else:
        password = sys.argv[1]
    
    if not password:
        print("Error: No password provided")
        sys.exit(1)
    
    analyze_password(password)

if __name__ == "__main__":
    main()

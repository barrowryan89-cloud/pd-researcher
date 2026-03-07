#!/usr/bin/env python3
"""
Password Analyzer — Free Tool #32
Generate strong passwords and analyze their entropy/strength.
Part of the PD_Researcher free tools collection.
https://github.com/barrowryan89-cloud/pd-researcher
"""

import argparse
import math
import random
import re
import string
import sys


def calculate_entropy(password):
    """Calculate password entropy in bits."""
    charset_size = 0
    
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'\d', password):
        charset_size += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        charset_size += 32  # Approximate for special chars
    
    if charset_size == 0:
        return 0
    
    entropy = len(password) * math.log2(charset_size)
    return entropy


def get_strength_rating(entropy):
    """Get human-readable strength rating."""
    if entropy < 28:
        return ("VERY WEAK", "🔴", "Instantly crackable")
    elif entropy < 36:
        return ("WEAK", "🟠", "Few seconds to crack")
    elif entropy < 60:
        return ("MODERATE", "🟡", "Minutes to hours")
    elif entropy < 80:
        return ("STRONG", "🟢", "Days to years")
    elif entropy < 100:
        return ("VERY STRONG", "🔵", "Years to centuries")
    else:
        return ("EXCELLENT", "💎", "Centuries+ with current tech")


def analyze_password(password):
    """Comprehensive password analysis."""
    analysis = {
        "length": len(password),
        "has_lower": bool(re.search(r'[a-z]', password)),
        "has_upper": bool(re.search(r'[A-Z]', password)),
        "has_digit": bool(re.search(r'\d', password)),
        "has_special": bool(re.search(r'[^a-zA-Z0-9]', password)),
        "unique_chars": len(set(password)),
        "consecutive": False,
        "repeated": False,
        "common_patterns": []
    }
    
    # Check for consecutive characters (abc, 123, etc.)
    for i in range(len(password) - 2):
        if (password[i:i+3] in string.ascii_lowercase or 
            password[i:i+3] in string.ascii_uppercase or
            password[i:i+3] in string.digits):
            analysis["consecutive"] = True
            break
    
    # Check for repeated characters (aaa, 111, etc.)
    if re.search(r'(.)\1{2,}', password):
        analysis["repeated"] = True
    
    # Common patterns
    common = ["password", "123456", "qwerty", "admin", "letmein", "welcome"]
    pwd_lower = password.lower()
    for pattern in common:
        if pattern in pwd_lower:
            analysis["common_patterns"].append(pattern)
    
    # Calculate entropy
    analysis["entropy"] = calculate_entropy(password)
    rating, icon, time = get_strength_rating(analysis["entropy"])
    analysis["rating"] = rating
    analysis["rating_icon"] = icon
    analysis["crack_time"] = time
    
    return analysis


def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    """Generate a strong password."""
    charset = ""
    required = []
    
    if use_lower:
        charset += string.ascii_lowercase
        required.append(random.choice(string.ascii_lowercase))
    if use_upper:
        charset += string.ascii_uppercase
        required.append(random.choice(string.ascii_uppercase))
    if use_digits:
        charset += string.digits
        required.append(random.choice(string.digits))
    if use_special:
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        charset += special
        required.append(random.choice(special))
    
    if not charset:
        raise ValueError("At least one character type must be selected")
    
    # Fill remaining length
    remaining = length - len(required)
    password_chars = required + [random.choice(charset) for _ in range(remaining)]
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password_chars)
    
    return ''.join(password_chars)


def print_analysis(analysis, verbose=False):
    """Print formatted analysis."""
    print(f"\n{'='*60}")
    print(f"{analysis['rating_icon']}  STRENGTH: {analysis['rating']}")
    print(f"{'='*60}")
    print(f"\n📊 Entropy: {analysis['entropy']:.1f} bits")
    print(f"⏱️  Crack Time: {analysis['crack_time']}")
    print(f"📏 Length: {analysis['length']} characters")
    print(f"🔤 Unique Characters: {analysis['unique_chars']}/{analysis['length']}")
    
    print(f"\n✓ Character Types:")
    print(f"  {'✓' if analysis['has_lower'] else '✗'} Lowercase (a-z)")
    print(f"  {'✓' if analysis['has_upper'] else '✗'} Uppercase (A-Z)")
    print(f"  {'✓' if analysis['has_digit'] else '✗'} Digits (0-9)")
    print(f"  {'✓' if analysis['has_special'] else '✗'} Special chars (!@#$...)")
    
    warnings = []
    if analysis['consecutive']:
        warnings.append("Contains sequential characters (abc, 123)")
    if analysis['repeated']:
        warnings.append("Contains repeated characters (aaa, 111)")
    if analysis['common_patterns']:
        warnings.append(f"Contains common patterns: {', '.join(analysis['common_patterns'])}")
    if analysis['length'] < 12:
        warnings.append("Length is less than 12 characters")
    
    if warnings:
        print(f"\n⚠️  Warnings:")
        for warning in warnings:
            print(f"  • {warning}")
    
    if verbose:
        print(f"\n💡 Recommendations:")
        print(f"  • Use at least 12-16 characters")
        print(f"  • Mix all character types")
        print(f"  • Avoid dictionary words")
        print(f"  • Avoid predictable patterns")
        print(f"  • Use a unique password for each service")
    
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Password Analyzer — Generate and analyze password strength",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a password
  python password_analyzer.py -a "MyP@ssw0rd123"
  
  # Generate a strong password (default 16 chars)
  python password_analyzer.py -g
  
  # Generate with specific length
  python password_analyzer.py -g -l 24
  
  # Generate without special characters
  python password_analyzer.py -g --no-special
  
  # Generate multiple passwords
  python password_analyzer.py -g -c 5
        """
    )
    
    parser.add_argument("-a", "--analyze", metavar="PASSWORD",
                       help="Analyze password strength")
    parser.add_argument("-g", "--generate", action="store_true",
                       help="Generate a strong password")
    parser.add_argument("-l", "--length", type=int, default=16,
                       help="Password length for generation (default: 16)")
    parser.add_argument("-c", "--count", type=int, default=1,
                       help="Number of passwords to generate (default: 1)")
    parser.add_argument("--no-lower", action="store_true",
                       help="Exclude lowercase letters")
    parser.add_argument("--no-upper", action="store_true",
                       help="Exclude uppercase letters")
    parser.add_argument("--no-digits", action="store_true",
                       help="Exclude digits")
    parser.add_argument("--no-special", action="store_true",
                       help="Exclude special characters")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output with recommendations")
    parser.add_argument("--json", action="store_true",
                       help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.analyze:
        analysis = analyze_password(args.analyze)
        
        if args.json:
            import json
            print(json.dumps(analysis, indent=2))
        else:
            print(f"\nPassword: {'*' * len(args.analyze)}")
            print_analysis(analysis, args.verbose)
        
        # Exit with error code for weak passwords
        if analysis["entropy"] < 50:
            sys.exit(1)
            
    elif args.generate:
        for i in range(args.count):
            password = generate_password(
                length=args.length,
                use_lower=not args.no_lower,
                use_upper=not args.no_upper,
                use_digits=not args.no_digits,
                use_special=not args.no_special
            )
            
            if args.json:
                import json
                analysis = analyze_password(password)
                print(json.dumps({"password": password, **analysis}, indent=2))
            else:
                analysis = analyze_password(password)
                print(f"\n🔑 Generated Password {i+1}:")
                print(f"   {password}")
                print(f"   {analysis['rating_icon']} {analysis['rating']} ({analysis['entropy']:.1f} bits)")
        
        if not args.json:
            print()
            print("🔒 Generated a strong password? Store it securely:")
            print("   1Password — The password manager developers trust")
            print("   → https://1password.com [affiliate link]")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

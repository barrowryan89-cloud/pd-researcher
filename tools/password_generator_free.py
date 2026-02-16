#!/usr/bin/env python3
"""
Tool #61: Password Generator & Strength Checker
Generate secure passwords and analyze password strength

Features:
- Generate random passwords with customizable length and character sets
- Analyze password strength (entropy, crack time estimation)
- Check against common weak passwords
- Generate passphrases (Diceware-style)
- Hash passwords (bcrypt, SHA256 for reference)
- Copy to clipboard option
"""

import argparse
import secrets
import string
import math
import sys
import re
import hashlib
from typing import Tuple, Optional

# Common weak passwords to check against
COMMON_PASSWORDS = {
    'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', 'letmein',
    'dragon', '111111', 'baseball', 'iloveyou', 'trustno1', 'sunshine',
    'princess', 'admin', 'welcome', 'shadow', 'ashley', 'football', 'jesus',
    'michael', 'ninja', 'mustang', 'password1', '123456789', 'adobe123',
    'admin123', 'root', 'toor', 'guest', 'default', 'master', 'access',
    'superuser', 'supervisor', 'operator', 'service', 'backup', 'password123',
    'qwerty123', 'lovely', 'whatever', 'starwars', 'passw0rd', 'hacker',
    'hunter2', 'correcthorsebatterystaple'
}

# Diceware wordlist (simplified - 100 common words)
PASSPHRASE_WORDS = [
    'apple', 'river', 'mountain', 'thunder', 'crystal', 'silent', 'winter',
    'dragon', 'forest', 'silver', 'golden', 'purple', 'shadow', 'bright',
    'gentle', 'fierce', 'rapid', 'calm', 'storm', 'ocean', 'desert', 'flame',
    'frost', 'earth', 'cloud', 'stone', 'steel', 'iron', 'copper', 'bronze',
    'diamond', 'emerald', 'sapphire', 'ruby', 'pearl', 'jade', 'amber',
    'wolf', 'tiger', 'eagle', 'falcon', 'raven', 'bear', 'lynx', 'hawk',
    'dolphin', 'whale', 'shark', 'jaguar', 'leopard', 'panther', 'cobra',
    'python', 'viper', 'octopus', 'spider', 'scorpion', 'crimson', 'azure',
    'verdant', 'golden', 'obsidian', 'marble', 'granite', 'quartz', 'opal',
    'nebula', 'cosmos', 'galaxy', 'comet', 'meteor', 'solar', 'lunar',
    'stellar', 'aurora', 'zenith', 'vertex', 'apex', 'summit', 'crown',
    'throne', 'scepter', 'chalice', 'orb', 'shield', 'sword', 'arrow',
    'shield', 'armor', 'helmet', 'scroll', 'tome', 'rune', 'sigil', 'token'
]


def generate_password(length: int = 16, 
                      use_upper: bool = True,
                      use_lower: bool = True,
                      use_digits: bool = True,
                      use_symbols: bool = True,
                      exclude_ambiguous: bool = False) -> str:
    """Generate a cryptographically secure random password."""
    
    chars = ''
    required_chars = []
    
    if use_upper:
        chars += string.ascii_uppercase
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        chars += string.ascii_lowercase
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        chars += string.digits
        required_chars.append(secrets.choice(string.digits))
    if use_symbols:
        symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        if exclude_ambiguous:
            symbols = symbols.replace('l', '').replace('I', '').replace('1', '').replace('0', '').replace('O', '')
        chars += symbols
        required_chars.append(secrets.choice(symbols))
    
    if not chars:
        raise ValueError("At least one character set must be enabled")
    
    # Generate remaining characters
    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(chars) for _ in range(remaining_length)]
    
    # Shuffle to avoid predictable positions for required characters
    secrets.SystemRandom().shuffle(password_chars)
    
    return ''.join(password_chars)


def generate_passphrase(num_words: int = 4, separator: str = '-') -> str:
    """Generate a Diceware-style passphrase."""
    words = [secrets.choice(PASSPHRASE_WORDS) for _ in range(num_words)]
    return separator.join(words)


def calculate_entropy(password: str) -> float:
    """Calculate password entropy in bits."""
    pool_size = 0
    
    if re.search(r'[a-z]', password):
        pool_size += 26
    if re.search(r'[A-Z]', password):
        pool_size += 26
    if re.search(r'\d', password):
        pool_size += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        pool_size += 32
    
    if pool_size == 0:
        return 0
    
    entropy = len(password) * math.log2(pool_size)
    return entropy


def estimate_crack_time(entropy: float, guesses_per_second: float = 1e9) -> Tuple[float, str]:
    """Estimate time to crack password via brute force."""
    combinations = 2 ** entropy
    seconds = combinations / guesses_per_second
    
    if seconds < 1:
        return seconds, "instantly"
    elif seconds < 60:
        return seconds, f"{int(seconds)} seconds"
    elif seconds < 3600:
        return seconds, f"{int(seconds / 60)} minutes"
    elif seconds < 86400:
        return seconds, f"{int(seconds / 3600)} hours"
    elif seconds < 31536000:
        return seconds, f"{int(seconds / 86400)} days"
    elif seconds < 3153600000:
        return seconds, f"{int(seconds / 31536000)} years"
    else:
        return seconds, "centuries"


def analyze_strength(password: str) -> dict:
    """Comprehensive password strength analysis."""
    
    entropy = calculate_entropy(password)
    crack_seconds, crack_time = estimate_crack_time(entropy)
    
    # Check various factors
    length_ok = len(password) >= 12
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[^a-zA-Z0-9]', password))
    
    # Determine strength rating
    if entropy < 40 or password.lower() in COMMON_PASSWORDS:
        strength = "VERY WEAK"
        score = 1
    elif entropy < 60:
        strength = "WEAK"
        score = 2
    elif entropy < 80:
        strength = "MODERATE"
        score = 3
    elif entropy < 100:
        strength = "STRONG"
        score = 4
    else:
        strength = "VERY STRONG"
        score = 5
    
    # Check patterns
    patterns_found = []
    if re.search(r'(.)\1{2,}', password):
        patterns_found.append("Repeated characters")
    if re.search(r'123|abc|qwe|asd|zxc', password.lower()):
        patterns_found.append("Sequential characters")
    if re.search(r'^(19|20)\d{2}', password):
        patterns_found.append("Year/date pattern")
    if password.lower() in COMMON_PASSWORDS:
        patterns_found.append("Common password")
    
    return {
        'password': password,
        'entropy': entropy,
        'crack_time': crack_time,
        'crack_seconds': crack_seconds,
        'strength': strength,
        'score': score,
        'length': len(password),
        'length_ok': length_ok,
        'has_upper': has_upper,
        'has_lower': has_lower,
        'has_digit': has_digit,
        'has_symbol': has_symbol,
        'patterns_found': patterns_found,
        'is_common': password.lower() in COMMON_PASSWORDS
    }


def hash_password(password: str, algorithm: str = 'sha256') -> str:
    """Generate password hash (for reference/verification purposes)."""
    if algorithm == 'sha256':
        return hashlib.sha256(password.encode()).hexdigest()
    elif algorithm == 'md5':
        return hashlib.md5(password.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard if possible."""
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        # Try using system clipboard
        import subprocess
        try:
            subprocess.run(['xclip', '-selection', 'clipboard'], 
                          input=text.encode(), check=True)
            return True
        except:
            try:
                subprocess.run(['pbcopy'], input=text.encode(), check=True)
                return True
            except:
                return False


def print_strength_analysis(analysis: dict):
    """Print formatted strength analysis."""
    colors = {
        1: '\033[91m',  # Red
        2: '\033[93m',  # Yellow
        3: '\033[93m',  # Yellow
        4: '\033[92m',  # Green
        5: '\033[92m',  # Green
        'reset': '\033[0m'
    }
    
    c = colors.get(analysis['score'], colors['reset'])
    reset = colors['reset']
    
    print(f"\n{c}═══════════════════════════════════════════════════{reset}")
    print(f"  Password Strength: {c}{analysis['strength']}{reset}")
    print(f"{c}═══════════════════════════════════════════════════{reset}")
    
    print(f"\n  📊 Metrics:")
    print(f"     • Length: {analysis['length']} characters {'✓' if analysis['length_ok'] else '✗'}")
    print(f"     • Entropy: {analysis['entropy']:.1f} bits")
    print(f"     • Crack time: {analysis['crack_time']}")
    
    print(f"\n  🔐 Character Types:")
    print(f"     • Lowercase: {'✓' if analysis['has_lower'] else '✗'}")
    print(f"     • Uppercase: {'✓' if analysis['has_upper'] else '✗'}")
    print(f"     • Digits: {'✓' if analysis['has_digit'] else '✗'}")
    print(f"     • Symbols: {'✓' if analysis['has_symbol'] else '✗'}")
    
    if analysis['patterns_found']:
        print(f"\n  ⚠️  Warnings:")
        for pattern in analysis['patterns_found']:
            print(f"     • {pattern}")
    
    if analysis['is_common']:
        print(f"\n  🚨 CRITICAL: This is a commonly used password!")
    
    # Progress bar for visual
    print(f"\n  {'█' * analysis['score']}{'░' * (5 - analysis['score'])}  {analysis['score']}/5")


def main():
    parser = argparse.ArgumentParser(
        description='Password Generator & Strength Checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate                    # Generate 16-char password
  %(prog)s generate -l 32              # Generate 32-char password
  %(prog)s generate -p                 # Generate passphrase
  %(prog)s check "myPassword123"       # Check password strength
  %(prog)s generate -c                 # Generate and copy to clipboard
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', aliases=['gen', 'g'], 
                                        help='Generate a password')
    gen_parser.add_argument('-l', '--length', type=int, default=16,
                           help='Password length (default: 16)')
    gen_parser.add_argument('--no-upper', action='store_true',
                           help='Exclude uppercase letters')
    gen_parser.add_argument('--no-lower', action='store_true',
                           help='Exclude lowercase letters')
    gen_parser.add_argument('--no-digits', action='store_true',
                           help='Exclude digits')
    gen_parser.add_argument('--no-symbols', action='store_true',
                           help='Exclude symbols')
    gen_parser.add_argument('--exclude-ambiguous', action='store_true',
                           help='Exclude ambiguous characters (l, I, 1, 0, O)')
    gen_parser.add_argument('-p', '--passphrase', action='store_true',
                           help='Generate passphrase instead of password')
    gen_parser.add_argument('-w', '--words', type=int, default=4,
                           help='Number of words for passphrase (default: 4)')
    gen_parser.add_argument('-s', '--separator', default='-',
                           help='Word separator for passphrase (default: -)')
    gen_parser.add_argument('-c', '--copy', action='store_true',
                           help='Copy generated password to clipboard')
    gen_parser.add_argument('--hash', choices=['sha256', 'md5'],
                           help='Also output password hash')
    
    # Check command
    check_parser = subparsers.add_parser('check', aliases=['c', 'analyze', 'a'],
                                          help='Check password strength')
    check_parser.add_argument('password', nargs='?',
                             help='Password to analyze (or use stdin)')
    check_parser.add_argument('--hash', choices=['sha256', 'md5'],
                             help='Also output password hash')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    if args.command in ['generate', 'gen', 'g']:
        if args.passphrase:
            password = generate_passphrase(args.words, args.separator)
            print(f"\n📝 Generated Passphrase:")
        else:
            password = generate_password(
                length=args.length,
                use_upper=not args.no_upper,
                use_lower=not args.no_lower,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols,
                exclude_ambiguous=args.exclude_ambiguous
            )
            print(f"\n🔑 Generated Password:")
        
        print(f"   {password}")
        
        if args.copy:
            if copy_to_clipboard(password):
                print("   📋 Copied to clipboard!")
            else:
                print("   ⚠️  Could not copy to clipboard (install pyperclip or xclip)")
        
        if args.hash:
            print(f"\n   #{args.hash.upper()}: {hash_password(password, args.hash)}")
        
        # Always show strength analysis
        analysis = analyze_strength(password)
        print_strength_analysis(analysis)
        print()
    
    elif args.command in ['check', 'c', 'analyze', 'a']:
        password = args.password
        if not password:
            if not sys.stdin.isatty():
                password = sys.stdin.read().strip()
            else:
                # Prompt securely
                import getpass
                password = getpass.getpass("Enter password: ")
        
        if not password:
            print("Error: No password provided", file=sys.stderr)
            sys.exit(1)
        
        analysis = analyze_strength(password)
        print_strength_analysis(analysis)
        
        if args.hash:
            print(f"\n   #{args.hash.upper()}: {hash_password(password, args.hash)}")
        print()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
PD Free Tool #59: JWT Decoder & Validator
Parse, decode, and validate JSON Web Tokens
Part of the PD_Researcher Free Tools Collection
"""

import argparse
import base64
import json
import sys
import hmac
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any

__version__ = "1.0.0"

def base64url_decode(data: str) -> bytes:
    """Decode base64url encoded string"""
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)

def base64url_encode(data: bytes) -> str:
    """Encode bytes to base64url string"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def decode_jwt(token: str) -> Optional[Dict[str, Any]]:
    """Decode a JWT token without verification"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        header = json.loads(base64url_decode(parts[0]))
        payload = json.loads(base64url_decode(parts[1]))
        signature = parts[2]
        
        return {
            'header': header,
            'payload': payload,
            'signature': signature,
            'raw_header': parts[0],
            'raw_payload': parts[1]
        }
    except Exception as e:
        return None

def verify_signature(token: str, secret: str, algorithm: str = 'HS256') -> bool:
    """Verify JWT signature with secret"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return False
        
        message = f"{parts[0]}.{parts[1]}"
        
        if algorithm == 'HS256':
            expected_sig = base64url_encode(
                hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
            )
        elif algorithm == 'HS384':
            expected_sig = base64url_encode(
                hmac.new(secret.encode(), message.encode(), hashlib.sha384).digest()
            )
        elif algorithm == 'HS512':
            expected_sig = base64url_encode(
                hmac.new(secret.encode(), message.encode(), hashlib.sha512).digest()
            )
        else:
            return False
        
        # Compare signatures (constant time)
        return hmac.compare_digest(expected_sig, parts[2])
    except Exception:
        return False

def format_timestamp(ts: int) -> str:
    """Format Unix timestamp to human readable"""
    try:
        dt = datetime.fromtimestamp(ts)
        now = datetime.now()
        diff = dt - now
        
        if diff.total_seconds() > 0:
            status = f"expires in {diff.days}d {diff.seconds//3600}h"
        else:
            status = "EXPIRED"
        
        return f"{dt.isoformat()} ({status})"
    except:
        return str(ts)

def colorize(text: str, color: str) -> str:
    """Add color to terminal output"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def print_token_info(token_data: Dict[str, Any], verified: Optional[bool] = None):
    """Pretty print JWT information"""
    print()
    print(colorize("═" * 60, 'blue'))
    print(colorize("  🔐 JWT DECODER & VALIDATOR", 'bold'))
    print(colorize("═" * 60, 'blue'))
    
    # Header Section
    print(colorize("\n┌─ HEADER ─────────────────────────────────────────────────┐", 'cyan'))
    header = token_data['header']
    for key, value in header.items():
        print(f"│  {colorize(key, 'yellow'):15} {str(value)[:40]:43} │")
    print("└──────────────────────────────────────────────────────────┘")
    
    # Payload Section
    print(colorize("\n┌─ PAYLOAD ────────────────────────────────────────────────┐", 'green'))
    payload = token_data['payload']
    
    # Handle standard claims with special formatting
    standard_claims = ['iss', 'sub', 'aud', 'exp', 'nbf', 'iat', 'jti']
    
    for key in standard_claims:
        if key in payload:
            value = payload[key]
            if key in ['exp', 'nbf', 'iat'] and isinstance(value, (int, float)):
                formatted = format_timestamp(int(value))
                color = 'red' if key == 'exp' and 'EXPIRED' in formatted else 'green'
                print(f"│  {colorize(key, 'yellow'):15} {formatted:43} │"[:75])
            else:
                print(f"│  {colorize(key, 'yellow'):15} {str(value)[:43]:43} │")
    
    # Custom claims
    for key, value in payload.items():
        if key not in standard_claims:
            val_str = str(value)[:43]
            if len(str(value)) > 43:
                val_str += "..."
            print(f"│  {colorize(key, 'yellow'):15} {val_str:43} │")
    
    print("└──────────────────────────────────────────────────────────┘")
    
    # Verification status
    if verified is not None:
        print()
        if verified:
            print(colorize("  ✅ SIGNATURE VALID", 'green'))
        else:
            print(colorize("  ❌ SIGNATURE INVALID", 'red'))
    
    # Security warnings
    print()
    alg = token_data['header'].get('alg', 'none')
    if alg == 'none':
        print(colorize("  ⚠️  WARNING: Algorithm 'none' - Token is unsigned!", 'red'))
    elif alg in ['HS256', 'HS384', 'HS512']:
        print(colorize(f"  ℹ️  HMAC Algorithm: {alg}", 'blue'))
    
    # Expiration check
    exp = payload.get('exp')
    if exp:
        now = datetime.now().timestamp()
        if exp < now:
            print(colorize("  ⚠️  WARNING: Token has EXPIRED", 'red'))
        else:
            days_left = int((exp - now) / 86400)
            print(colorize(f"  ℹ️  Token valid for {days_left} more days", 'green'))
    
    print(colorize("\n" + "═" * 60, 'blue'))

def main():
    parser = argparse.ArgumentParser(
        description="🔐 JWT Decoder & Validator - Parse and verify JSON Web Tokens",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "eyJhbGciOiJIUzI1NiIs..."
  %(prog)s token.txt --secret mykey
  echo "$JWT_TOKEN" | %(prog)s --secret mykey

Part of PD_Researcher Free Tools: https://barrowryan89-cloud.github.io/pd-researcher/
        """
    )
    
    parser.add_argument('token', nargs='?', help='JWT token string or file containing token')
    parser.add_argument('-s', '--secret', help='Secret key for signature verification')
    parser.add_argument('-a', '--algorithm', default='HS256', 
                       choices=['HS256', 'HS384', 'HS512'],
                       help='Algorithm for verification (default: HS256)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    # Get token from args, file, or stdin
    token = args.token
    if not token:
        if not sys.stdin.isatty():
            token = sys.stdin.read().strip()
        else:
            parser.print_help()
            sys.exit(1)
    
    # Check if token is a file
    import os
    if os.path.isfile(token):
        with open(token, 'r') as f:
            token = f.read().strip()
    
    # Decode token
    token_data = decode_jwt(token)
    
    if not token_data:
        print(colorize("❌ Error: Invalid JWT token format", 'red'), file=sys.stderr)
        sys.exit(1)
    
    # Verify signature if secret provided
    verified = None
    if args.secret:
        alg = token_data['header'].get('alg', 'HS256')
        if alg in ['HS256', 'HS384', 'HS512']:
            verified = verify_signature(token, args.secret, alg)
    
    # JSON output
    if args.json:
        output = {
            'header': token_data['header'],
            'payload': token_data['payload'],
            'signature_valid': verified
        }
        result = json.dumps(output, indent=2)
    else:
        # Capture pretty print output
        import io
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        print_token_info(token_data, verified)
        sys.stdout = old_stdout
        result = buffer.getvalue()
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"Output written to: {args.output}")
    else:
        print(result)
    
    # Exit with error code if signature verification failed
    if verified is False:
        sys.exit(2)
    
    print("\n" + "="*60)
    print("🔐 Managing secrets? Use 1Password for secure team sharing")
    print("   Developer-friendly, CLI available: https://1password.com [affiliate]")
    print("="*60)

if __name__ == '__main__':
    main()

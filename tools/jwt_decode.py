#!/usr/bin/env python3
"""
jwt_decode - JWT Token Inspector CLI
Quickly decode and validate JWT tokens without sending them anywhere.
"""

import argparse
import base64
import json
import sys
from datetime import datetime, timezone

def decode_base64(data):
    """Decode base64url encoded data."""
    # Add padding if needed
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    try:
        return base64.urlsafe_b64decode(data)
    except Exception:
        return None

def format_json(data):
    """Pretty print JSON."""
    return json.dumps(data, indent=2, ensure_ascii=False)

def parse_timestamp(ts):
    """Convert Unix timestamp to readable date."""
    try:
        dt = datetime.fromtimestamp(ts)
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return str(ts)

def colorize(text, color):
    """Add color to text."""
    colors = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'bold': '\033[1m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def decode_jwt(token, verbose=False, no_color=False):
    """Decode a JWT token."""
    
    def c(text, color):
        return text if no_color else colorize(text, color)
    
    # Split token
    parts = token.split('.')
    
    if len(parts) != 3:
        print(c("❌ Invalid JWT format - expected 3 parts (header.payload.signature)", 'red'))
        sys.exit(1)
    
    header_b64, payload_b64, signature_b64 = parts
    
    # Decode header
    header_bytes = decode_base64(header_b64)
    if not header_bytes:
        print(c("❌ Failed to decode header", 'red'))
        sys.exit(1)
    
    try:
        header = json.loads(header_bytes)
    except json.JSONDecodeError:
        print(c("❌ Header is not valid JSON", 'red'))
        sys.exit(1)
    
    # Decode payload
    payload_bytes = decode_base64(payload_b64)
    if not payload_bytes:
        print(c("❌ Failed to decode payload", 'red'))
        sys.exit(1)
    
    try:
        payload = json.loads(payload_bytes)
    except json.JSONDecodeError:
        print(c("❌ Payload is not valid JSON", 'red'))
        sys.exit(1)
    
    # Print results
    print()
    print(c("🔓 JWT Token Decoded", 'bold'))
    print(c("=" * 50, 'blue'))
    
    # Header section
    print(c("\n📋 HEADER (Algorithm & Token Type)", 'cyan'))
    print(c("-" * 40, 'blue'))
    print(format_json(header))
    
    alg = header.get('alg', 'unknown')
    print(c(f"\n   Algorithm: {alg}", 'yellow'))
    
    if alg == 'none':
        print(c("   ⚠️  WARNING: Algorithm is 'none' - token is not signed!", 'red'))
    elif alg in ['HS256', 'HS384', 'HS512']:
        print(c("   ℹ️  HMAC SHA-based signing", 'blue'))
    elif alg in ['RS256', 'RS384', 'RS512']:
        print(c("   ℹ️  RSA-based signing", 'blue'))
    elif alg in ['ES256', 'ES384', 'ES512']:
        print(c("   ℹ️  ECDSA-based signing", 'blue'))
    
    # Payload section
    print(c("\n📦 PAYLOAD (Claims & Data)", 'cyan'))
    print(c("-" * 40, 'blue'))
    print(format_json(payload))
    
    # Standard claims analysis
    print(c("\n🔍 Standard Claims Analysis:", 'cyan'))
    print(c("-" * 40, 'blue'))
    
    now = datetime.now(timezone.utc).timestamp()
    
    # Expiration
    if 'exp' in payload:
        exp = payload['exp']
        exp_str = parse_timestamp(exp)
        if exp < now:
            print(c(f"   ❌ exp (Expiry):      {exp_str} - TOKEN EXPIRED", 'red'))
        else:
            remaining = int(exp - now)
            hours = remaining // 3600
            mins = (remaining % 3600) // 60
            print(c(f"   ✅ exp (Expiry):      {exp_str} - Valid for {hours}h {mins}m", 'green'))
    
    # Issued at
    if 'iat' in payload:
        print(c(f"   🕐 iat (Issued):      {parse_timestamp(payload['iat'])}", 'blue'))
    
    # Not before
    if 'nbf' in payload:
        nbf = payload['nbf']
        if nbf > now:
            print(c(f"   ⏳ nbf (Not Before):  {parse_timestamp(nbf)} - NOT YET VALID", 'yellow'))
        else:
            print(c(f"   ✅ nbf (Not Before):  {parse_timestamp(nbf)}", 'green'))
    
    # Issuer
    if 'iss' in payload:
        print(c(f"   🏢 iss (Issuer):      {payload['iss']}", 'blue'))
    
    # Subject
    if 'sub' in payload:
        print(c(f"   👤 sub (Subject):     {payload['sub']}", 'blue'))
    
    # Audience
    if 'aud' in payload:
        aud = payload['aud']
        if isinstance(aud, list):
            print(c(f"   🎯 aud (Audience):    {', '.join(aud)}", 'blue'))
        else:
            print(c(f"   🎯 aud (Audience):    {aud}", 'blue'))
    
    # JWT ID
    if 'jti' in payload:
        print(c(f"   🆔 jti (Token ID):    {payload['jti']}", 'blue'))
    
    # Signature info
    print(c("\n🔐 SIGNATURE", 'cyan'))
    print(c("-" * 40, 'blue'))
    print(f"   Length: {len(signature_b64)} chars (base64url)")
    print(c("   ⚠️  Note: Signature validation requires secret/key", 'yellow'))
    
    if verbose:
        print(c("\n📊 RAW TOKEN PARTS", 'cyan'))
        print(c("-" * 40, 'blue'))
        print(f"   Header:    {header_b64[:50]}..." if len(header_b64) > 50 else f"   Header:    {header_b64}")
        print(f"   Payload:   {payload_b64[:50]}..." if len(payload_b64) > 50 else f"   Payload:   {payload_b64}")
        print(f"   Signature: {signature_b64[:50]}..." if len(signature_b64) > 50 else f"   Signature: {signature_b64}")
    
    print()
    print("🔐 Working with authentication? Secure your secrets:")
    print("   → Store API keys with 1Password: https://1password.com [affiliate]")
    print()

def main():
    parser = argparse.ArgumentParser(
        description='🔓 Decode and inspect JWT tokens locally',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jwt_decode eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  jwt_decode $MY_TOKEN --verbose
  echo "$TOKEN" | jwt_decode -

Note: This tool decodes only. It cannot verify signatures without the secret.
        """
    )
    parser.add_argument('token', help='JWT token to decode (or "-" to read from stdin)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    
    args = parser.parse_args()
    
    # Read token
    if args.token == '-':
        token = sys.stdin.read().strip()
    else:
        token = args.token
    
    # Remove "Bearer " prefix if present
    if token.startswith('Bearer '):
        token = token[7:]
    
    decode_jwt(token, args.verbose, args.no_color)

if __name__ == '__main__':
    main()

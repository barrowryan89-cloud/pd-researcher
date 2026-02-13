#!/usr/bin/env python3
"""
jwt_decoder.py - Tool #53: JWT Token Decoder & Validator
Quickly decode and inspect JWT tokens without sending them anywhere.
Part of the 50+ Essential Python CLI Tools collection.
"""

import argparse
import base64
import json
import sys
from datetime import datetime, timezone
from typing import Optional

def decode_base64(data: str) -> bytes:
    """Decode base64url encoded data."""
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)

def format_timestamp(ts: int) -> str:
    """Format Unix timestamp to readable date."""
    try:
        dt = datetime.fromtimestamp(ts)
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return str(ts)

def decode_jwt(token: str) -> tuple[dict, dict, str]:
    """Decode JWT token into header, payload, and signature."""
    parts = token.split('.')
    
    if len(parts) != 3:
        raise ValueError("Invalid JWT format: expected 3 parts separated by dots")
    
    # Decode header
    header_json = decode_base64(parts[0])
    header = json.loads(header_json)
    
    # Decode payload
    payload_json = decode_base64(parts[1])
    payload = json.loads(payload_json)
    
    # Return signature as-is (it's binary)
    signature = parts[2]
    
    return header, payload, signature

def check_expiration(payload: dict) -> Optional[str]:
    """Check if token is expired and return status."""
    now = datetime.now(timezone.utc).timestamp()
    
    exp = payload.get('exp')
    iat = payload.get('iat')
    nbf = payload.get('nbf')
    
    status_lines = []
    
    if exp:
        exp_time = format_timestamp(exp)
        if now > exp:
            status_lines.append(f"❌ EXPIRED (was valid until {exp_time})")
        else:
            remaining = exp - now
            hours = remaining / 3600
            if hours < 24:
                status_lines.append(f"⏰ EXPIRES SOON: {exp_time} ({hours:.1f} hours)")
            else:
                days = hours / 24
                status_lines.append(f"✅ VALID until {exp_time} ({days:.1f} days)")
    
    if iat:
        status_lines.append(f"📅 Issued at: {format_timestamp(iat)}")
    
    if nbf:
        nbf_time = format_timestamp(nbf)
        if now < nbf:
            status_lines.append(f"⏳ Not valid before: {nbf_time}")
        else:
            status_lines.append(f"✅ Valid from: {nbf_time}")
    
    return '\n'.join(status_lines) if status_lines else None

def print_colored_json(data: dict) -> None:
    """Print JSON with basic terminal colors."""
    json_str = json.dumps(data, indent=2)
    
    # Simple color highlighting
    lines = json_str.split('\n')
    for line in lines:
        if ':' in line:
            key_part = line.split(':', 1)[0]
            val_part = line[len(key_part)+1:]
            print(f"\033[36m{key_part}\033[0m:{val_part}")
        else:
            print(line)

def main():
    parser = argparse.ArgumentParser(
        description='🔓 JWT Token Decoder & Validator - Inspect tokens locally',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s eyJhbGciOiJIUzI1NiIs...
  %(prog)s "eyJhbGciOiJIUzI1NiIs..." --pretty
  echo $JWT_TOKEN | %(prog)s -

Note: This tool only DECODES tokens (base64). It does NOT verify signatures.
        """
    )
    parser.add_argument('token', help='JWT token to decode (or "-" for stdin)')
    parser.add_argument('--pretty', '-p', action='store_true', 
                        help='Pretty print with colors')
    parser.add_argument('--raw', '-r', action='store_true',
                        help='Output raw JSON only (for piping)')
    
    args = parser.parse_args()
    
    # Read token
    if args.token == '-':
        token = sys.stdin.read().strip()
    else:
        token = args.token.strip()
    
    # Remove "Bearer " prefix if present
    if token.startswith('Bearer '):
        token = token[7:]
    
    # Remove quotes if present
    token = token.strip('"\'')
    
    try:
        header, payload, signature = decode_jwt(token)
    except ValueError as e:
        print(f"\033[31mError: {e}\033[0m", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\033[31mError decoding JWT: {e}\033[0m", file=sys.stderr)
        sys.exit(1)
    
    if args.raw:
        print(json.dumps({'header': header, 'payload': payload}))
        return
    
    # Print output
    print("\n" + "="*60)
    print("🔓 JWT TOKEN DECODER")
    print("="*60)
    
    # Header section
    print("\n📋 HEADER (Algorithm & Token Type):")
    print("-"*40)
    if args.pretty:
        print_colored_json(header)
    else:
        print(json.dumps(header, indent=2))
    
    # Show algorithm warning
    alg = header.get('alg', 'unknown')
    if alg == 'none':
        print("\n\033[31m⚠️  WARNING: Algorithm is 'none' - token is unverified!\033[0m")
    elif alg in ['HS256', 'HS384', 'HS512']:
        print(f"\n🔐 Algorithm: {alg} (HMAC SHA-based)")
    elif alg in ['RS256', 'RS384', 'RS512']:
        print(f"\n🔐 Algorithm: {alg} (RSA-based)")
    elif alg in ['ES256', 'ES384', 'ES512']:
        print(f"\n🔐 Algorithm: {alg} (ECDSA-based)")
    
    # Payload section
    print("\n📦 PAYLOAD (Claims & Data):")
    print("-"*40)
    if args.pretty:
        print_colored_json(payload)
    else:
        print(json.dumps(payload, indent=2))
    
    # Expiration check
    print("\n⏱️  TOKEN STATUS:")
    print("-"*40)
    status = check_expiration(payload)
    if status:
        print(status)
    else:
        print("ℹ️  No expiration data found in token")
    
    # Common claims summary
    print("\n📝 CLAIMS SUMMARY:")
    print("-"*40)
    claims_map = {
        'sub': 'Subject (user ID)',
        'iss': 'Issuer',
        'aud': 'Audience',
        'jti': 'JWT ID',
        'typ': 'Token type',
        'azp': 'Authorized party',
        'scope': 'Scopes/permissions',
        'permissions': 'Permissions',
        'role': 'Role',
        'roles': 'Roles',
        'email': 'Email',
        'name': 'Name',
    }
    
    found_claims = []
    for claim, desc in claims_map.items():
        if claim in payload:
            val = payload[claim]
            if isinstance(val, list):
                val = ', '.join(str(v) for v in val)
            found_claims.append(f"  • {desc}: {val}")
    
    if found_claims:
        print('\n'.join(found_claims))
    else:
        print("  No standard claims found")
    
    # Signature info
    print("\n🔏 SIGNATURE:")
    print("-"*40)
    print(f"  Length: {len(signature)} characters")
    print(f"  Preview: {signature[:20]}...")
    print("\n\033[33m⚠️  Note: Signature verification requires the secret key.\033[0m")
    print("\033[33m   This tool decodes only — it cannot verify authenticity.\033[0m")
    
    print("\n" + "="*60)
    print(f"Decoded {len(token)} characters successfully")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

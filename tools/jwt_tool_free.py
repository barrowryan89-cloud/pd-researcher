#!/usr/bin/env python3
"""
jwt_tool_free.py - JWT Token Decoder
Decode and inspect JSON Web Tokens. No verification (just decoding).
Zero dependencies. Pure Python 3.
"""

import sys
import base64
import json
from datetime import datetime

def base64url_decode(data: str) -> bytes:
    """Decode base64url encoded string."""
    # Add padding if necessary
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)

def decode_jwt(token: str) -> dict:
    """Decode JWT token without verification."""
    parts = token.split('.')
    
    if len(parts) != 3:
        raise ValueError("Invalid JWT format. Expected 3 parts separated by dots.")
    
    header_b64, payload_b64, signature_b64 = parts
    
    try:
        header = json.loads(base64url_decode(header_b64))
    except Exception as e:
        raise ValueError(f"Invalid header: {e}")
    
    try:
        payload = json.loads(base64url_decode(payload_b64))
    except Exception as e:
        raise ValueError(f"Invalid payload: {e}")
    
    signature = base64url_decode(signature_b64) if signature_b64 else None
    
    return {
        'header': header,
        'payload': payload,
        'signature': signature,
        'raw': {
            'header': header_b64,
            'payload': payload_b64,
            'signature': signature_b64
        }
    }

def format_timestamp(ts):
    """Format Unix timestamp to human readable."""
    try:
        dt = datetime.utcfromtimestamp(ts)
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return str(ts)

def analyze_jwt(token: str):
    """Analyze and display JWT token."""
    print(f"🔐 JWT Token Analysis")
    print("=" * 60)
    
    # Show masked token
    parts = token.split('.')
    if len(parts) == 3:
        masked = f"{parts[0][:20]}...{parts[1][:20]}...{parts[2][:20]}"
        print(f"\nToken: {masked}")
    
    try:
        decoded = decode_jwt(token)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return
    
    # Header
    print(f"\n📋 Header:")
    print(json.dumps(decoded['header'], indent=2))
    
    # Explain algorithm
    alg = decoded['header'].get('alg', 'none')
    print(f"\n  Algorithm: {alg}", end="")
    if alg == 'none':
        print(" ⚠️  Unsigned token!")
    elif alg == 'HS256':
        print(" (HMAC-SHA256)")
    elif alg == 'RS256':
        print(" (RSA-SHA256)")
    elif alg == 'ES256':
        print(" (ECDSA-SHA256)")
    else:
        print("")
    
    # Payload
    print(f"\n📦 Payload:")
    print(json.dumps(decoded['payload'], indent=2))
    
    # Common claims
    print(f"\n🎫 Standard Claims:")
    claims = decoded['payload']
    
    if 'sub' in claims:
        print(f"  Subject (sub): {claims['sub']}")
    if 'iss' in claims:
        print(f"  Issuer (iss): {claims['iss']}")
    if 'aud' in claims:
        print(f"  Audience (aud): {claims['aud']}")
    if 'exp' in claims:
        exp_time = format_timestamp(claims['exp'])
        now = datetime.utcnow().timestamp()
        status = "✅ Valid" if claims['exp'] > now else "❌ Expired"
        print(f"  Expires (exp): {exp_time} ({status})")
    if 'iat' in claims:
        print(f"  Issued (iat): {format_timestamp(claims['iat'])}")
    if 'nbf' in claims:
        print(f"  Not Before (nbf): {format_timestamp(claims['nbf'])}")
    if 'jti' in claims:
        print(f"  JWT ID (jti): {claims['jti']}")
    
    # Security notes
    print(f"\n⚠️  Security Notes:")
    print(f"  • Token is NOT verified (this tool only decodes)")
    if alg == 'none':
        print(f"  • WARNING: Algorithm is 'none' - token is not signed!")
    print(f"  • Always verify signature on server side")
    print(f"  • Never trust client-side token validation")
    
    print("\n" + "=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: jwt_tool_free.py <token>")
        print("       jwt_tool_free.py --stdin")
        print("       echo '<token>' | jwt_tool_free.py --stdin")
        print("\nDecodes JWT tokens (Header.Payload.Signature)")
        print("Note: This tool only decodes - it does NOT verify signatures")
        sys.exit(1)
    
    if sys.argv[1] == '--stdin':
        token = sys.stdin.read().strip()
    else:
        token = sys.argv[1]
    
    # Remove 'Bearer ' prefix if present
    if token.lower().startswith('bearer '):
        token = token[7:].strip()
    
    if not token:
        print("Error: No token provided")
        sys.exit(1)
    
    analyze_jwt(token)

if __name__ == "__main__":
    main()

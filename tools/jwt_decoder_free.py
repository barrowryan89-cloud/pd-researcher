#!/usr/bin/env python3
"""
JWT Decoder - Free CLI Tool #40
Decode and inspect JSON Web Tokens without validation
Zero dependencies, single file, MIT licensed
https://github.com/barrowryan89-cloud/pd-researcher
"""

import base64
import json
import sys
import argparse

__version__ = "1.0.0"

def base64_url_decode(data):
    """Decode base64url encoded data."""
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    try:
        return base64.urlsafe_b64decode(data)
    except Exception:
        return None

def decode_jwt(token):
    """Decode a JWT token without verifying signature."""
    parts = token.split('.')
    
    if len(parts) != 3:
        return None, "Invalid JWT format (expected 3 parts)"
    
    header_b64, payload_b64, signature = parts
    
    header_json = base64_url_decode(header_b64)
    payload_json = base64_url_decode(payload_b64)
    
    if not header_json:
        return None, "Failed to decode header"
    if not payload_json:
        return None, "Failed to decode payload"
    
    try:
        header = json.loads(header_json)
        payload = json.loads(payload_json)
    except json.JSONDecodeError as e:
        return None, f"JSON decode error: {e}"
    
    return {
        'header': header,
        'payload': payload,
        'signature': signature[:20] + '...' if len(signature) > 20 else signature
    }, None

def format_timestamp(ts):
    """Format Unix timestamp to human readable."""
    from datetime import datetime
    try:
        dt = datetime.fromtimestamp(ts)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ts)

def analyze_token(data):
    """Analyze token payload for common claims."""
    payload = data['payload']
    analysis = []
    
    now = __import__('time').time()
    
    if 'exp' in payload:
        exp = payload['exp']
        status = "EXPIRED" if exp < now else "VALID"
        analysis.append(f"  exp: {format_timestamp(exp)} ({status})")
    
    if 'iat' in payload:
        analysis.append(f"  iat: {format_timestamp(payload['iat'])}")
    
    if 'nbf' in payload:
        analysis.append(f"  nbf: {format_timestamp(payload['nbf'])}")
    
    if 'iss' in payload:
        analysis.append(f"  iss: {payload['iss']}")
    
    if 'sub' in payload:
        analysis.append(f"  sub: {payload['sub']}")
    
    if 'aud' in payload:
        aud = payload['aud']
        if isinstance(aud, list):
            analysis.append(f"  aud: {', '.join(aud)}")
        else:
            analysis.append(f"  aud: {aud}")
    
    return analysis

def main():
    parser = argparse.ArgumentParser(
        description="🔓 JWT Decoder - Inspect JSON Web Tokens",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  %(prog)s --file token.txt
  echo "$TOKEN" | %(prog)s --stdin

⚠️  This tool decodes only - it does NOT verify signatures
        """
    )
    parser.add_argument('token', nargs='?', help='JWT token string')
    parser.add_argument('--file', '-f', help='Read token from file')
    parser.add_argument('--stdin', '-s', action='store_true', help='Read token from stdin')
    parser.add_argument('--raw', '-r', action='store_true', help='Output raw JSON only')
    parser.add_argument('--version', '-v', action='version', version=f"%(prog)s {__version__}")
    
    args = parser.parse_args()
    
    token = None
    
    if args.stdin:
        token = sys.stdin.read().strip()
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                token = f.read().strip()
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.token:
        token = args.token.strip()
    else:
        parser.print_help()
        sys.exit(1)
    
    data, error = decode_jwt(token)
    
    if error:
        print(f"❌ {error}", file=sys.stderr)
        sys.exit(1)
    
    if args.raw:
        print(json.dumps(data, indent=2))
    else:
        print("═" * 60)
        print("🔓 JWT Decoder")
        print("═" * 60)
        
        print("\n📋 HEADER:")
        print(json.dumps(data['header'], indent=2))
        
        print("\n📦 PAYLOAD:")
        print(json.dumps(data['payload'], indent=2))
        
        analysis = analyze_token(data)
        if analysis:
            print("\n⏰ TIMESTAMPS & CLAIMS:")
            for line in analysis:
                print(line)
        
        print(f"\n🔏 SIGNATURE: {data['signature']}")
        print("═" * 60)
        print("\n💡 Pro Tip: Need JWT validation, key management, or automation?")
        print("   Check out PD_Researcher Pro → https://10links.blue")
        print("═" * 60)

if __name__ == '__main__':
    main()

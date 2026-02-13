#!/usr/bin/env python3
"""
ssl_cert.py — SSL Certificate Inspector
Analyze TLS certificates for any hostname: expiry, issuer, cipher strength, vulnerabilities

Usage:
  ssl_cert <hostname> [port]
  ssl_cert google.com
  ssl_cert api.example.com 443 --verbose

Features:
- Certificate chain validation
- Expiry date detection with color-coded warnings
- Issuer and subject details
- TLS version and cipher info
- Common vulnerability checks (expired, self-signed, weak ciphers)
- JSON output for automation
- SNI support for multi-tenant servers

Exit codes:
  0 = Valid certificate
  1 = Expired or invalid
  2 = Connection/verification error

Part of PD's Free Developer Tools: https://barrowryan89-cloud.github.io/pd-researcher/
"""

import ssl
import socket
import sys
import json
import argparse
from datetime import datetime, timezone
from urllib.parse import urlparse

# ANSI colors for terminal output
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'cyan': '\033[96m',
    'gray': '\033[90m'
}

def color(name, text):
    """Apply color to text if stdout is a TTY"""
    if sys.stdout.isatty():
        return f"{COLORS.get(name, '')}{text}{COLORS['reset']}"
    return text

def parse_host_port(host_input, default_port=443):
    """Parse hostname and port from input"""
    # Remove protocol if present
    if '://' in host_input:
        parsed = urlparse(host_input)
        host = parsed.hostname
        port = parsed.port or default_port
    elif ':' in host_input:
        parts = host_input.rsplit(':', 1)
        host = parts[0]
        try:
            port = int(parts[1])
        except ValueError:
            port = default_port
    else:
        host = host_input
        port = default_port
    
    return host, port

def get_certificate_info(hostname, port=443, timeout=10):
    """Fetch and parse SSL certificate information"""
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()
                
                return {
                    'certificate': cert,
                    'cipher': cipher,
                    'tls_version': version,
                    'hostname': hostname,
                    'port': port
                }
    except ssl.SSLCertVerificationError as e:
        return {'error': 'verification_failed', 'message': str(e), 'hostname': hostname, 'port': port}
    except socket.timeout:
        return {'error': 'timeout', 'message': f'Connection to {hostname}:{port} timed out', 'hostname': hostname, 'port': port}
    except socket.gaierror:
        return {'error': 'dns_error', 'message': f'Could not resolve {hostname}', 'hostname': hostname, 'port': port}
    except ConnectionRefusedError:
        return {'error': 'connection_refused', 'message': f'Connection refused to {hostname}:{port}', 'hostname': hostname, 'port': port}
    except Exception as e:
        return {'error': 'unknown', 'message': str(e), 'hostname': hostname, 'port': port}

def parse_cert_date(date_str):
    """Parse certificate date string to datetime"""
    if not date_str:
        return None
    try:
        # Handle both formats: 'Mar 15 12:00:00 2024 GMT' and ISO format
        for fmt in ['%b %d %H:%M:%S %Y %Z', '%Y-%m-%d %H:%M:%S']:
            try:
                return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
    except Exception:
        pass
    return None

def days_until(date):
    """Calculate days until a date"""
    if not date:
        return None
    now = datetime.now(timezone.utc)
    delta = date - now
    return delta.days

def get_cert_status(days):
    """Determine certificate status based on days until expiry"""
    if days is None:
        return 'unknown'
    if days < 0:
        return 'expired'
    if days <= 7:
        return 'critical'
    if days <= 30:
        return 'warning'
    return 'valid'

def status_emoji(status):
    """Get emoji for status"""
    return {'valid': '✅', 'warning': '⚠️', 'critical': '🚨', 'expired': '❌', 'unknown': '❓'}.get(status, '❓')

def status_color(status):
    """Get color for status"""
    return {'valid': 'green', 'warning': 'yellow', 'critical': 'red', 'expired': 'red', 'unknown': 'gray'}.get(status, 'gray')

def analyze_certificate(data):
    """Analyze certificate and return structured info"""
    if 'error' in data:
        return data
    
    cert = data['certificate']
    cipher = data['cipher']
    
    not_before = parse_cert_date(cert.get('notBefore'))
    not_after = parse_cert_date(cert.get('notAfter'))
    days_remaining = days_until(not_after)
    status = get_cert_status(days_remaining)
    
    # Check for weak ciphers
    weak_ciphers = ['RC4', 'DES', '3DES', 'MD5', 'NULL']
    cipher_issues = [w for w in weak_ciphers if cipher and w in str(cipher)]
    
    # Check TLS version
    tls_warnings = []
    if data['tls_version'] in ['TLSv1', 'TLSv1.1']:
        tls_warnings.append('Deprecated TLS version')
    
    return {
        'hostname': data['hostname'],
        'port': data['port'],
        'subject': cert.get('subject'),
        'issuer': cert.get('issuer'),
        'not_before': cert.get('notBefore'),
        'not_after': cert.get('notAfter'),
        'days_remaining': days_remaining,
        'status': status,
        'serial_number': cert.get('serialNumber'),
        'version': cert.get('version'),
        'sans': cert.get('subjectAltName', []),
        'tls_version': data['tls_version'],
        'cipher_suite': cipher[0] if cipher else None,
        'cipher_bits': cipher[2] if cipher else None,
        'warnings': cipher_issues + tls_warnings,
        'is_valid': status in ['valid', 'warning']
    }

def extract_cert_fields(cert_field):
    """Extract key-value pairs from certificate subject/issuer fields"""
    fields = {}
    if isinstance(cert_field, tuple):
        # Format: ((('commonName', 'value'),), (('orgName', 'value'),))
        for outer in cert_field:
            if isinstance(outer, tuple):
                for inner in outer:
                    if isinstance(inner, tuple) and len(inner) == 2:
                        key, val = inner
                        fields[key] = val
    elif isinstance(cert_field, list):
        for item in cert_field:
            if isinstance(item, tuple) and len(item) == 2:
                key, val = item
                fields[key] = val
    elif isinstance(cert_field, dict):
        fields = cert_field
    return fields

def print_certificate_info(info, verbose=False):
    """Print formatted certificate information"""
    if 'error' in info:
        print(color('red', f"❌ Error: {info['message']}"))
        return 2
    
    status = info['status']
    emoji = status_emoji(status)
    
    print()
    print("=" * 60)
    print(color('bold', f"🔒 SSL CERTIFICATE INSPECTOR"))
    print("=" * 60)
    
    # Target
    print(f"\n📍 {color('cyan', 'Target:')} {info['hostname']}:{info['port']}")
    
    # Status
    status_text = status.upper()
    if status == 'expired':
        status_text = f"EXPIRED ({abs(info['days_remaining'])} days ago)"
    elif info['days_remaining'] is not None:
        status_text = f"{status.upper()} ({info['days_remaining']} days remaining)"
    
    print(f"\n{emoji} {color(status_color(status), color('bold', f'Status: {status_text}'))}")
    
    # Subject
    print(f"\n{color('bold', '📋 Subject:')}")
    subject_fields = extract_cert_fields(info['subject'])
    if subject_fields:
        for k, v in subject_fields.items():
            print(f"   {k}: {v}")
    else:
        print(f"   {color('gray', 'No subject information available')}")
    
    # Issuer
    print(f"\n{color('bold', '🏢 Issuer:')}")
    issuer_fields = extract_cert_fields(info['issuer'])
    if issuer_fields:
        for k, v in issuer_fields.items():
            print(f"   {k}: {v}")
    else:
        print(f"   {color('gray', 'No issuer information available')}")
    
    # Validity
    print(f"\n{color('bold', '📅 Validity:')}")
    print(f"   Not Before: {info['not_before'] or 'Unknown'}")
    print(f"   Not After:  {info['not_after'] or 'Unknown'}")
    
    # TLS Info
    print(f"\n{color('bold', '🔐 Connection:')}")
    print(f"   TLS Version: {info['tls_version'] or 'Unknown'}")
    print(f"   Cipher:      {info['cipher_suite'] or 'Unknown'}")
    if info['cipher_bits']:
        print(f"   Key Size:    {info['cipher_bits']} bits")
    
    # Subject Alternative Names
    if info['sans'] and verbose:
        print(f"\n{color('bold', '🌐 Subject Alternative Names:')}")
        for san_type, san_value in info['sans'][:10]:
            print(f"   {san_type}: {san_value}")
        if len(info['sans']) > 10:
            print(f"   ... and {len(info['sans']) - 10} more")
    
    # Warnings
    if info['warnings']:
        print(f"\n{color('red', color('bold', '⚠️  Warnings:'))}")
        for warning in info['warnings']:
            print(f"   • {warning}")
    
    print()
    print("=" * 60)
    print(color('gray', "Part of PD's Free Developer Tools"))
    print(color('gray', "https://barrowryan89-cloud.github.io/pd-researcher/"))
    print(f"\n🔒 Need SSL certificates? Get affordable domains + SSL at Namecheap:")
    print("   https://namecheap.pxf.io/pdresearcher [affiliate]")
    print("=" * 60)
    print()
    
    return 0 if info['is_valid'] else 1

def main():
    parser = argparse.ArgumentParser(
        description='SSL Certificate Inspector - Analyze TLS certificates',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ssl_cert google.com              # Basic check
  ssl_cert api.example.com 8443    # Custom port
  ssl_cert site.com --verbose      # Detailed output
  ssl_cert site.com --json         # JSON for scripts

Exit codes:
  0 = Valid certificate
  1 = Expired or invalid certificate
  2 = Connection/verification error
        """
    )
    
    parser.add_argument('hostname', help='Hostname to check (e.g., google.com)')
    parser.add_argument('port', nargs='?', type=int, default=443, help='Port (default: 443)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed information')
    parser.add_argument('-j', '--json', action='store_true', help='Output as JSON')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Connection timeout in seconds')
    
    args = parser.parse_args()
    
    # Parse hostname and port
    hostname, port = parse_host_port(args.hostname, args.port)
    
    # Get certificate info
    raw_data = get_certificate_info(hostname, port, args.timeout)
    analyzed = analyze_certificate(raw_data)
    
    # Output
    if args.json:
        print(json.dumps(analyzed, indent=2, default=str))
        sys.exit(0 if analyzed.get('is_valid') else 1)
    else:
        exit_code = print_certificate_info(analyzed, args.verbose)
        sys.exit(exit_code)

if __name__ == '__main__':
    main()

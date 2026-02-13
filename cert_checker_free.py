#!/usr/bin/env python3
"""
cert_checker_free.py - SSL Certificate Inspector
Check SSL/TLS certificates for any domain. Shows expiry, issuer, and validity.
Zero dependencies. Pure Python 3.
"""

import sys
import socket
import ssl
from datetime import datetime

def check_cert(hostname: str, port: int = 443):
    """Check SSL certificate for a hostname."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()
                
                # Parse dates
                not_after = cert.get('notAfter')
                not_before = cert.get('notBefore')
                
                def parse_asn1_time(t):
                    return datetime.strptime(t, '%b %d %H:%M:%S %Y %Z')
                
                expiry = parse_asn1_time(not_after)
                issued = parse_asn1_time(not_before)
                days_left = (expiry - datetime.utcnow()).days
                
                # Get subject info
                subject = dict(x[0] for x in cert.get('subject', []))
                issuer = dict(x[0] for x in cert.get('issuer', []))
                
                # Get SANs
                san = cert.get('subjectAltName', [])
                sans = [x[1] for x in san if x[0] == 'DNS']
                
                print(f"🔒 SSL Certificate for {hostname}:{port}")
                print("=" * 50)
                print(f"\n📋 Subject:")
                print(f"   Common Name: {subject.get('commonName', 'N/A')}")
                print(f"\n🔐 Issuer:")
                print(f"   Organization: {issuer.get('organizationName', 'N/A')}")
                print(f"   Common Name: {issuer.get('commonName', 'N/A')}")
                print(f"\n📅 Validity:")
                print(f"   Issued: {issued.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                print(f"   Expires: {expiry.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                print(f"   Days Left: {days_left}", end="")
                if days_left < 7:
                    print(" ⚠️  EXPIRING SOON!")
                elif days_left < 30:
                    print(" ⚡ Less than 30 days")
                else:
                    print(" ✅ Valid")
                print(f"\n🔧 Connection:")
                print(f"   TLS Version: {version}")
                print(f"   Cipher: {cipher[0]}")
                print(f"\n🌐 Subject Alternative Names:")
                for san in sans[:10]:
                    print(f"   • {san}")
                if len(sans) > 10:
                    print(f"   ... and {len(sans) - 10} more")
                    
    except socket.gaierror:
        print(f"❌ Error: Could not resolve hostname '{hostname}'")
        sys.exit(1)
    except socket.timeout:
        print(f"❌ Error: Connection timeout to {hostname}:{port}")
        sys.exit(1)
    except ssl.SSLError as e:
        print(f"❌ SSL Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: cert_checker_free.py <hostname> [port]")
        print("Example: cert_checker_free.py google.com")
        print("         cert_checker_free.py api.example.com 8443")
        sys.exit(1)
    
    hostname = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 443
    
    check_cert(hostname, port)

if __name__ == "__main__":
    main()

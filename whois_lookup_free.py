#!/usr/bin/env python3
"""
whois_lookup_free.py - Domain WHOIS Lookup
Get domain registration information. Shows registrar, creation date, expiry.
Zero dependencies. Pure Python 3.
Note: Uses system whois command if available, falls back to basic info.
"""

import sys
import socket
import subprocess
from datetime import datetime

def get_basic_domain_info(domain: str):
    """Get basic domain information via DNS and socket."""
    info = {
        'domain': domain,
        'ip_addresses': [],
        'has_dns': False,
        'dns_status': ''
    }
    
    # Check DNS resolution
    try:
        ip = socket.gethostbyname(domain)
        info['ip_addresses'].append(ip)
        info['has_dns'] = True
        info['dns_status'] = '✅ Resolves'
    except socket.gaierror:
        info['dns_status'] = '❌ No DNS record'
    
    # Try IPv6
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET6)
        for r in results:
            ip6 = r[4][0]
            if ip6 not in info['ip_addresses']:
                info['ip_addresses'].append(ip6)
    except:
        pass
    
    return info

def run_whois(domain: str):
    """Run whois command if available."""
    try:
        result = subprocess.run(
            ['whois', domain],
            capture_output=True,
            text=True,
            timeout=15
        )
        return result.stdout
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        return "Timeout"
    except Exception as e:
        return f"Error: {e}"

def parse_whois(whois_text: str):
    """Parse key fields from whois output."""
    if not whois_text:
        return {}
    
    data = {}
    lines = whois_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if ':' in line and not line.startswith('%') and not line.startswith('#'):
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            
            if key in ['registrar', 'registrant', 'creation date', 'created',
                      'expiration date', 'expires', 'expiry date', 'updated date',
                      'modified', 'status', 'name server', 'nserver']:
                if key not in data:
                    data[key] = []
                if value and value not in data[key]:
                    data[key].append(value)
    
    return data

def lookup_domain(domain: str):
    """Perform WHOIS lookup."""
    print(f"🔍 WHOIS Lookup for {domain}")
    print("=" * 60)
    
    # Get basic info
    basic = get_basic_domain_info(domain)
    print(f"\n📍 Domain: {basic['domain']}")
    print(f"   DNS Status: {basic['dns_status']}")
    
    if basic['ip_addresses']:
        print(f"   IP Addresses:")
        for ip in basic['ip_addresses'][:5]:
            print(f"      {ip}")
        if len(basic['ip_addresses']) > 5:
            print(f"      ... and {len(basic['ip_addresses']) - 5} more")
    
    # Try WHOIS
    print("\n📋 Registration Information:")
    whois_text = run_whois(domain)
    
    if whois_text is None:
        print("   ⚠️  System 'whois' command not found")
        print("   Install: apt install whois  (Debian/Ubuntu)")
        print("             brew install whois (macOS)")
    elif whois_text == "Timeout":
        print("   ⚠️  WHOIS query timed out")
    elif whois_text.startswith("Error:"):
        print(f"   ❌ {whois_text}")
    else:
        data = parse_whois(whois_text)
        
        if 'registrar' in data:
            print(f"   Registrar: {data['registrar'][0]}")
        
        if 'creation date' in data:
            print(f"   Created: {data['creation date'][0]}")
        elif 'created' in data:
            print(f"   Created: {data['created'][0]}")
        
        if 'expiration date' in data:
            print(f"   Expires: {data['expiration date'][0]}")
        elif 'expires' in data:
            print(f"   Expires: {data['expires'][0]}")
        elif 'expiry date' in data:
            print(f"   Expires: {data['expiry date'][0]}")
        
        if 'updated date' in data:
            print(f"   Updated: {data['updated date'][0]}")
        elif 'modified' in data:
            print(f"   Updated: {data['modified'][0]}")
        
        if 'status' in data:
            print(f"   Status: {', '.join(data['status'][:3])}")
        
        if 'name server' in data or 'nserver' in data:
            ns = data.get('name server', []) + data.get('nserver', [])
            if ns:
                print(f"   Name Servers:")
                for server in ns[:4]:
                    print(f"      {server}")
    
    print("\n" + "=" * 60)
    print("💡 Tip: For full WHOIS details, run: whois " + domain)

def main():
    if len(sys.argv) < 2:
        print("Usage: whois_lookup_free.py <domain>")
        print("Example: whois_lookup_free.py google.com")
        print("\nShows: DNS info, registrar, dates, status")
        print("Note: Requires 'whois' command for full details")
        sys.exit(1)
    
    domain = sys.argv[1].lower().strip()
    # Remove protocol if present
    domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
    
    try:
        lookup_domain(domain)
    except KeyboardInterrupt:
        print("\n\n⚠️  Lookup interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

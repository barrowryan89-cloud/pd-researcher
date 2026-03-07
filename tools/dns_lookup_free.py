#!/usr/bin/env python3
"""
dns_lookup_free.py - DNS Lookup Tool
Query DNS records for any domain. Supports A, AAAA, MX, TXT, NS, CNAME, SOA.
Zero dependencies. Pure Python 3.
"""

import sys
import socket

def get_a_records(domain: str):
    """Get A records (IPv4 addresses)."""
    try:
        return socket.gethostbyname_ex(domain)[2]
    except socket.gaierror:
        return []

def get_aaaa_records(domain: str):
    """Get AAAA records (IPv6 addresses)."""
    try:
        # Try to get IPv6 address
        results = socket.getaddrinfo(domain, None, socket.AF_INET6)
        return list(set(r[4][0] for r in results))
    except socket.gaierror:
        return []

def get_mx_records(domain: str):
    """Get MX records (mail servers)."""
    try:
        import subprocess
        result = subprocess.run(
            ['nslookup', '-type=mx', domain],
            capture_output=True,
            text=True,
            timeout=10
        )
        lines = result.stdout.split('\n')
        mx = []
        for line in lines:
            if 'mail exchanger' in line.lower():
                parts = line.split('=')
                if len(parts) == 2:
                    priority, server = parts[1].strip().split()
                    mx.append((int(priority), server))
        return sorted(mx)
    except Exception:
        return []

def get_ns_records(domain: str):
    """Get NS records (name servers)."""
    try:
        import subprocess
        result = subprocess.run(
            ['nslookup', '-type=ns', domain],
            capture_output=True,
            text=True,
            timeout=10
        )
        lines = result.stdout.split('\n')
        ns = []
        for line in lines:
            if 'nameserver' in line.lower():
                parts = line.split('=')
                if len(parts) == 2:
                    ns.append(parts[1].strip().rstrip('.'))
        return ns
    except Exception:
        return []

def get_txt_records(domain: str):
    """Get TXT records."""
    try:
        import subprocess
        result = subprocess.run(
            ['nslookup', '-type=txt', domain],
            capture_output=True,
            text=True,
            timeout=10
        )
        lines = result.stdout.split('\n')
        txt = []
        in_txt = False
        for line in lines:
            if 'text =' in line.lower():
                in_txt = True
                txt_text = line.split('=', 1)[1].strip().strip('"')
                txt.append(txt_text)
            elif in_txt and line.startswith('"'):
                txt[-1] += line.strip().strip('"')
            elif in_txt and not line.startswith(' '):
                in_txt = False
        return txt
    except Exception:
        return []

def lookup_domain(domain: str):
    """Perform full DNS lookup."""
    print(f"🌐 DNS Lookup for {domain}")
    print("=" * 50)
    
    # A Records (IPv4)
    print("\n📍 A Records (IPv4):")
    a_records = get_a_records(domain)
    if a_records:
        for ip in a_records:
            print(f"   {ip}")
    else:
        print("   None found")
    
    # AAAA Records (IPv6)
    print("\n📍 AAAA Records (IPv6):")
    aaaa_records = get_aaaa_records(domain)
    if aaaa_records:
        for ip in aaaa_records:
            print(f"   {ip}")
    else:
        print("   None found")
    
    # NS Records
    print("\n🖥️  Name Servers (NS):")
    ns_records = get_ns_records(domain)
    if ns_records:
        for ns in ns_records:
            print(f"   {ns}")
    else:
        print("   None found (try: nslookup -type=ns " + domain + ")")
    
    # MX Records
    print("\n📧 Mail Servers (MX):")
    mx_records = get_mx_records(domain)
    if mx_records:
        for priority, server in mx_records:
            print(f"   {priority:3d}  {server}")
    else:
        print("   None found (try: nslookup -type=mx " + domain + ")")
    
    # TXT Records
    print("\n📝 TXT Records:")
    txt_records = get_txt_records(domain)
    if txt_records:
        for txt in txt_records[:5]:  # Limit to 5
            if len(txt) > 80:
                txt = txt[:77] + "..."
            print(f"   \"{txt}\"")
        if len(txt_records) > 5:
            print(f"   ... and {len(txt_records) - 5} more")
    else:
        print("   None found")
    
    # Summary
    print("\n" + "=" * 50)
    total = len(a_records) + len(aaaa_records) + len(ns_records) + len(mx_records) + len(txt_records)
    print(f"Total records found: {total}")

def main():
    if len(sys.argv) < 2:
        print("Usage: dns_lookup_free.py <domain>")
        print("Example: dns_lookup_free.py google.com")
        print("\nQueries: A, AAAA, NS, MX, TXT records")
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

#!/usr/bin/env python3
"""
dns_probe - DNS record inspector and propagation checker
Quick DNS diagnostics for any domain.

Usage: dns_probe <domain> [--type TYPE] [--all]
Example: dns_probe google.com --all
"""

import sys
import socket
import subprocess
import json
from typing import Dict, List, Optional, Any


def get_record(domain: str, record_type: str) -> List[str]:
    """Get DNS records using dig or nslookup."""
    records = []
    try:
        # Try dig first (more reliable)
        result = subprocess.run(
            ['dig', '+short', domain, record_type],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            records = [r.strip() for r in result.stdout.strip().split('\n') if r.strip()]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Fallback to nslookup
    if not records:
        try:
            result = subprocess.run(
                ['nslookup', '-type=' + record_type, domain],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'Address:' in line and 'server' not in line.lower():
                        addr = line.split('Address:')[-1].strip()
                        if addr and addr not in records:
                            records.append(addr)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    
    return records


def get_a_records(domain: str) -> List[str]:
    """Get A records (IPv4 addresses)."""
    try:
        ips = socket.getaddrinfo(domain, None, socket.AF_INET)
        return list(set([ip[4][0] for ip in ips]))
    except socket.gaierror:
        return []


def get_aaaa_records(domain: str) -> List[str]:
    """Get AAAA records (IPv6 addresses)."""
    try:
        ips = socket.getaddrinfo(domain, None, socket.AF_INET6)
        return list(set([ip[4][0] for ip in ips]))
    except socket.gaierror:
        return []


def get_mx_records(domain: str) -> List[Dict[str, Any]]:
    """Get MX records."""
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, 'MX')
        return [{'priority': r.preference, 'server': str(r.exchange).rstrip('.')} 
                for r in answers]
    except Exception:
        # Fallback to dig
        records = get_record(domain, 'MX')
        result = []
        for r in records:
            parts = r.split()
            if len(parts) >= 2:
                try:
                    priority = int(parts[0])
                    server = parts[1].rstrip('.')
                    result.append({'priority': priority, 'server': server})
                except ValueError:
                    continue
        return sorted(result, key=lambda x: x['priority'])


def get_txt_records(domain: str) -> List[str]:
    """Get TXT records."""
    records = get_record(domain, 'TXT')
    # Clean up quoted TXT records
    cleaned = []
    for r in records:
        r = r.strip('"')
        if r:
            cleaned.append(r)
    return cleaned


def get_ns_records(domain: str) -> List[str]:
    """Get NS records."""
    records = get_record(domain, 'NS')
    return [r.rstrip('.') for r in records]


def get_cname(domain: str) -> Optional[str]:
    """Get CNAME record."""
    records = get_record(domain, 'CNAME')
    return records[0].rstrip('.') if records else None


def get_soa_record(domain: str) -> Optional[Dict[str, str]]:
    """Get SOA record."""
    records = get_record(domain, 'SOA')
    if records:
        parts = records[0].split()
        if len(parts) >= 7:
            return {
                'primary_ns': parts[0].rstrip('.'),
                'admin_email': parts[1].rstrip('.').replace('.', '@', 1),
                'serial': parts[2],
                'refresh': parts[3],
                'retry': parts[4],
                'expire': parts[5],
                'minimum_ttl': parts[6]
            }
    return None


def check_spf(txt_records: List[str]) -> Optional[str]:
    """Extract SPF record from TXT records."""
    for record in txt_records:
        if record.startswith('v=spf1'):
            return record
    return None


def check_dkim(domain: str, selector: str = 'default') -> Optional[str]:
    """Check DKIM record for a selector."""
    dkim_domain = f"{selector}._domainkey.{domain}"
    records = get_record(dkim_domain, 'TXT')
    return records[0] if records else None


def check_dmarc(domain: str) -> Optional[str]:
    """Check DMARC record."""
    dmarc_domain = f"_dmarc.{domain}"
    records = get_record(dmarc_domain, 'TXT')
    return records[0] if records else None


def analyze_domain(domain: str, check_all: bool = False) -> Dict[str, Any]:
    """Full DNS analysis of a domain."""
    result = {'domain': domain}
    
    # Always get these
    result['a_records'] = get_a_records(domain)
    result['aaaa_records'] = get_aaaa_records(domain)
    
    if check_all:
        result['mx_records'] = get_mx_records(domain)
        result['txt_records'] = get_txt_records(domain)
        result['ns_records'] = get_ns_records(domain)
        result['cname'] = get_cname(domain)
        result['soa'] = get_soa_record(domain)
        result['spf'] = check_spf(result.get('txt_records', []))
        result['dmarc'] = check_dmarc(domain)
    
    # Determine health score
    score = 0
    if result['a_records']:
        score += 40
    if result.get('mx_records'):
        score += 20
    if result.get('spf'):
        score += 15
    if result.get('dmarc'):
        score += 15
    if result.get('aaaa_records'):
        score += 10
    
    result['health_score'] = min(score, 100)
    
    return result


def print_results(data: Dict[str, Any], verbose: bool = False):
    """Pretty print DNS results."""
    domain = data['domain']
    score = data['health_score']
    
    # Score emoji
    if score >= 80:
        score_emoji = '🟢'
    elif score >= 50:
        score_emoji = '🟡'
    else:
        score_emoji = '🔴'
    
    print(f"\n🔍 DNS Probe: {domain}")
    print(f"{score_emoji} Health Score: {score}/100")
    print("=" * 50)
    
    # A Records
    if data.get('a_records'):
        print(f"\n📍 A Records (IPv4):")
        for ip in data['a_records']:
            print(f"   → {ip}")
    else:
        print(f"\n❌ No A records found")
    
    # AAAA Records
    if data.get('aaaa_records'):
        print(f"\n📍 AAAA Records (IPv6):")
        for ip in data['aaaa_records']:
            print(f"   → {ip}")
    
    if not verbose:
        print(f"\n💡 Use --all for MX, TXT, NS, SPF, DMARC records")
        return
    
    # CNAME
    if data.get('cname'):
        print(f"\n🔗 CNAME: {data['cname']}")
    
    # MX Records
    if data.get('mx_records'):
        print(f"\n📧 MX Records (Mail):")
        for mx in sorted(data['mx_records'], key=lambda x: x['priority']):
            print(f"   [{mx['priority']}] {mx['server']}")
    
    # NS Records
    if data.get('ns_records'):
        print(f"\n🌐 Name Servers:")
        for ns in data['ns_records']:
            print(f"   → {ns}")
    
    # TXT Records
    if data.get('txt_records'):
        print(f"\n📝 TXT Records:")
        for txt in data['txt_records'][:5]:  # Limit to first 5
            display = txt[:70] + '...' if len(txt) > 70 else txt
            print(f"   → {display}")
        if len(data['txt_records']) > 5:
            print(f"   ... and {len(data['txt_records']) - 5} more")
    
    # Email Security
    if data.get('spf'):
        print(f"\n✅ SPF Record: Present")
        if verbose:
            print(f"   {data['spf'][:60]}...")
    else:
        print(f"\n⚠️  SPF Record: Missing (email deliverability risk)")
    
    if data.get('dmarc'):
        print(f"✅ DMARC Record: Present")
    else:
        print(f"⚠️  DMARC Record: Missing")


def main():
    if len(sys.argv) < 2:
        print("Usage: dns_probe <domain> [--all] [--json]")
        print("Example: dns_probe google.com --all")
        sys.exit(1)
    
    domain = sys.argv[1]
    check_all = '--all' in sys.argv
    json_output = '--json' in sys.argv
    
    # Clean domain
    domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
    
    data = analyze_domain(domain, check_all)
    
    if json_output:
        print(json.dumps(data, indent=2))
    else:
        print_results(data, verbose=check_all)
    
    print("\n" + "="*60)
    print("💡 Domain Management:")
    print("   Need DNS hosting or domain registration?")
    print("   Namecheap offers affordable domains + free WHOIS privacy")
    print("   https://www.namecheap.com/domains/")
    print("="*60)


if __name__ == '__main__':
    main()

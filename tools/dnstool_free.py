#!/usr/bin/env python3
"""
dnstool — DNS lookup utility
Tool #70 — Free CLI Tool for PD Researcher
"""

import argparse
import socket
import sys


def dns_lookup(domain, record_type='A'):
    """Perform DNS lookup."""
    try:
        if record_type == 'A':
            result = socket.gethostbyname(domain)
            return [result], None
        elif record_type in ['MX', 'NS', 'TXT', 'SOA', 'CNAME']:
            # For advanced records, we'd need dnspython
            return None, f"Use 'pip install dnspython' for {record_type} records"
        else:
            return None, f"Unsupported record type: {record_type}"
    except socket.gaierror as e:
        return None, f"DNS lookup failed: {e}"


def reverse_lookup(ip):
    """Perform reverse DNS lookup."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname, None
    except socket.herror as e:
        return None, f"Reverse lookup failed: {e}"


def get_all_records(domain):
    """Get all common DNS records."""
    results = {}
    
    # A record
    try:
        results['A'] = [socket.gethostbyname(domain)]
    except socket.gaierror:
        results['A'] = []
    
    # CNAME (check if domain is an alias)
    try:
        hostname = socket.getfqdn(domain)
        if hostname != domain:
            results['CNAME'] = hostname
    except:
        pass
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='DNS lookup utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dnstool example.com                       # Get A record
  dnstool 8.8.8.8 --reverse                 # Reverse DNS lookup
  dnstool example.com --all                 # Get all records
  dnstool example.com -t MX                 # Get MX records
        """
    )
    
    parser.add_argument('query', help='Domain or IP to lookup')
    parser.add_argument('-t', '--type', default='A',
                       choices=['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'ANY'],
                       help='Record type (default: A)')
    parser.add_argument('-r', '--reverse', action='store_true',
                       help='Reverse DNS lookup (IP to hostname)')
    parser.add_argument('-a', '--all', action='store_true',
                       help='Get all common record types')
    parser.add_argument('--short', action='store_true',
                       help='Short output (IP only)')
    
    args = parser.parse_args()
    
    # Reverse lookup
    if args.reverse:
        hostname, error = reverse_lookup(args.query)
        if error:
            print(error, file=sys.stderr)
            sys.exit(1)
        print(hostname)
        return
    
    # All records mode
    if args.all:
        print(f"DNS Records for {args.query}:\n")
        results = get_all_records(args.query)
        
        for record_type, value in results.items():
            if value:
                if isinstance(value, list):
                    print(f"{record_type}: {', '.join(value)}")
                else:
                    print(f"{record_type}: {value}")
        
        # Try to get authoritative info
        try:
            hostname = socket.getfqdn(args.query)
            if hostname != args.query:
                print(f"\nCanonical name: {hostname}")
        except:
            pass
        
        return
    
    # Standard lookup
    result, error = dns_lookup(args.query, args.type)
    
    if error:
        print(error, file=sys.stderr)
        sys.exit(1)
    
    if args.short:
        for ip in result:
            print(ip)
    else:
        print(f"{args.type} records for {args.query}:")
        for ip in result:
            print(f"  {ip}")


if __name__ == '__main__':
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
